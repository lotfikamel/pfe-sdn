const express = require('express');

//load socket.io
const Server = require('socket.io');

//load http module
const http = require('http');

const UDPServer = require('./UDPServer')

const FlowController = require('./Controllers/FlowController')

const App = express()

//create http server
const httpServer = http.createServer(App);

//create new io instance
const io = new Server(httpServer, {

	serveClient : false,
	upgradeTimeout : 20000,
	cookie : false
});

io.on('connection', (socket) => {

	console.log('client connected')

	socket.on('GET_FLOWS', FlowController.getFlows(socket))
})

//listen for requests
httpServer.listen(4000, () => {

	console.log(`monitor server listening on port 4000...`);
});