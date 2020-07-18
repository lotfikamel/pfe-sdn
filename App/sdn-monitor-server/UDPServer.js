const dgram = require('dgram')

const server = dgram.createSocket('udp4')

server.on('listening', () => {

	console.log('udp server started on port 4001')
})

server.on('message', (msg, info) => {

	console.log('new message', JSON.parse(msg.toString()))
});

server.bind(4001)

server.send('GET_FLOWS_NODE', 6000, '127.0.0.1', () => {

	console.log('message sent')
})

module.exports = server;