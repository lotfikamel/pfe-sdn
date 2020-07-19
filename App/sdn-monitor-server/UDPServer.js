const dgram = require('dgram')

const server = dgram.createSocket('udp4')

server.on('listening', () => {

	console.log('udp server started on port 4001')
})

server.bind(4001)

module.exports = server;