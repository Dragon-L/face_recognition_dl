#!/usr/bin/env python3
import sys
sys.path.append('..')
import base64
import cv2

import numpy as np
import json

from PIL import Image
from io import BytesIO

from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory
from twisted.internet import task, defer
from twisted.python import log

from face_recognition_webcam import face_recognition

class FaceServerProtocol(WebSocketServerProtocol):
    def __init__(self):
        super(FaceServerProtocol, self).__init__()

    def onConnect(self, request):
        print("Client connecting: {}".format(request.peer))

    def onOpen(self):
        print('Websocket open.')

    def onMessage(self, payload, isBinary):
        # print('Received: {}'.format(payload.decode('utf8')))
        msg = payload.decode('utf8')
        image = self.base64_to_array(msg)
        recognized_image = face_recognition(image)
        print('show')
        cv2.imshow('imgae', recognized_image)
        cv2.waitKey(1)
        msg = self.array_to_base64(recognized_image)
        self.sendMessage(msg)

    def array_to_base64(self, recognized_image):
        image = Image.fromarray(recognized_image)
        io = BytesIO()
        image.save(io, format='jpeg')
        image = base64.b64encode(io.getvalue())
        io.close()
        return image

    def base64_to_array(self, msg):
        head = 'data:image/jpeg;base64,'
        assert (msg.startswith(head))
        img_data = base64.b64decode(msg[len(head):])
        io = BytesIO(img_data)
        image = Image.open(io)
        image = np.fliplr(np.asarray(image))
        io.close()
        return image

    def onClose(self, wasClean, code, reason):
        print('Websocket closed')


def main(reactor):
    log.startLogging(sys.stdout)
    factor = WebSocketServerFactory()
    factor.protocol = FaceServerProtocol
    reactor.listenTCP(8090, factor)
    return defer.Deferred()


task.react(main)