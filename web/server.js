#!/usr/bin/env node

var WebSocketSocketServer = require('websocket').server;
var http = require('http');
var express = require('express');

var app = express();

// var server = http.createServer(function(request, response){
//     console.log((new Date()) + ' Received request for ' + request.url);
//     response.writeHead(404);
//     response.end();
// });

app.get('*', function (req, res) {
    console.log((new Date()) + ' routing');
    console.log(__dirname);
    res.sendFile(__dirname + '/index.html');
});

var server = http.createServer(app);
server.listen(8080, function () {
    console.log((new Date()) + ' Server is listening on port 8080');
});

wsServer = new WebSocketSocketServer({
    httpServer: server,
    autoAcceptConnections: false
});

wsServer.on('request', function (request) {
    var connection = request.accept('echo-protocol', request.origin);
    console.log((new Date()) + ' Connection accepted.');

    connection.on('message', function (message) {
        head = 'data:image/jpeg;base64,';
        console.log('Server received: ' + message.utf8Data);
        connection.send('From server');
    });
    connection.on('close', function (reasonCode, description) {
        console.log((new Date()) + ' Peer ' + connection.remoteAddress + ' disconneted.');
    })
});

