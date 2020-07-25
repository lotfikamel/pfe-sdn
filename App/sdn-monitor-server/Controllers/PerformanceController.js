const UDPServer = require('../UDPServer')

const Event = require('../System/Event')

function runTest (socket) {

	return (data) => {

		console.log('from client', data);

		UDPServer.send(JSON.stringify({ event : 'TEST_BANDWIDTH', data}), 1000, '127.0.0.1')
	}
}

function sendBwResult (io) {

	return (data) => {

		console.log(data)

		io.emit('TEST_BANDWIDTH', data)
	}
}

module.exports = {

	sendBwResult,
	runTest
}