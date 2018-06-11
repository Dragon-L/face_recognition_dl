import cv2
import dlib
import numpy as np
import os

NUMBER_OF_TIMES_TO_UPSAMPLE = 1  # How many times to re-sample the face when calculating encoding. Higher is more accurate, but slower (i.e. 100 is 100x slower)
BOX_COLOR = (0, 0, 255)
FONT_COLOR = (255, 255, 255)


def mmodrect_to_tuple(mmodrect):
    # Convert dlib rectangles object to a tuple in (top, right, bottom, left) order
    return mmodrect.top(), mmodrect.right(), mmodrect.bottom(), mmodrect.left()


def mmodrect_to_rect(mmodrect):
    return dlib.rectangle(mmodrect.left(), mmodrect.top(), mmodrect.right(), mmodrect.bottom())


def compare_faces(known_face_encodings, face_encoding, tolerate=0.6):
    distances = np.linalg.norm((known_face_encodings - face_encoding), axis=1)
    return list(distances <= tolerate)


def get_locations_and_encodings(img, times_to_upsample=NUMBER_OF_TIMES_TO_UPSAMPLE):
    locations_rect, locations_tuple = get_face_locations(img, times_to_upsample)
    landmarks = get_face_landmarks(img, locations_rect)
    encodings = get_face_encodings(img, landmarks, times_to_upsample)
    return locations_tuple, encodings


def get_face_encodings(img, landmarks, times_to_upsample):
    return [np.array(face_encoder.compute_face_descriptor(img, face_landmark, times_to_upsample)) for face_landmark in
            landmarks]


def get_face_landmarks(img, locations_rect):
    return [face_landmark_5_points(img, face_location) for face_location in locations_rect]


def get_face_locations(img, times_to_upsample):
    locations = face_detector(img, times_to_upsample)

    locations_tuple = [mmodrect_to_tuple(face_location.rect) for face_location in locations]
    locations_rect = [mmodrect_to_rect(face_location.rect) for face_location in locations]
    return locations_rect, locations_tuple

dirname = os.path.dirname(__file__)
face_detector = dlib.cnn_face_detection_model_v1(dirname + '/model/mmod_human_face_detector.dat')
face_landmark_5_points = dlib.shape_predictor(dirname + '/model/shape_predictor_5_face_landmarks.dat')
face_encoder = dlib.face_recognition_model_v1(dirname + '/model/dlib_face_recognition_resnet_model_v1.dat')

keep_running = True

guolong_image = cv2.imread(dirname + '/images/guolong.jpg')[:, :, ::-1]
_, guolong_encoding = get_locations_and_encodings(guolong_image)

known_face_encodings = [
    guolong_encoding[0]
]

known_face_names = [
    'Guolong'
]


def face_recognition(frame):
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]

    face_locations, face_encodings = get_locations_and_encodings(rgb_small_frame)
    face_names = []
    for face_encoding in face_encodings:
        matches = compare_faces(known_face_encodings, face_encoding)
        name = known_face_names[matches.index(True)] if True in matches else 'Unknown'
        face_names.append(name)

    for location, name in zip(face_locations, face_names):
        top, right, bottom, left = tuple(i * 4 for i in location)
        cv2.rectangle(frame, (left, top), (right, bottom), BOX_COLOR, 2)

        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), BOX_COLOR, cv2.FILLED)
        cv2.putText(frame, name, (left, bottom), cv2.FONT_HERSHEY_DUPLEX, 1.0, FONT_COLOR, 1)

    return frame
