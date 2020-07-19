const UDPServer = require('../UDPServer')

/**
* Get flow From flowCollector Server
* 
*/
function getFlows (socket) {

	return (data) => {

		UDPServer.send('GET_FLOWS_MONITOR', 6000, '127.0.0.1')

		UDPServer.on('message', (msg, info) => {

			let response = JSON.parse(msg.toString())

			if (response.event == 'GET_FLOWS_MONITOR') {

				let flows = response.data;

				if (flows.length > 0) {

					let flowsHeader = Object.keys(flows[0])

					let flowsValues = flows.map(flow => Object.values(flow))

					socket.emit('GET_FLOWS', {

						flowsHeader,
						flowsValues
					})
				}
			}
		});
	}
}

module.exports = {

	getFlows
}