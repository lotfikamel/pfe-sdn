const dgram = require('dgram')

const server = dgram.createSocket('udp4');

const Event = require('./System/Event')

server.on('message', (msg, info) => {

	let response = JSON.parse(msg.toString())

	Event.emit(response.event, response.data)
})

module.exports = server;