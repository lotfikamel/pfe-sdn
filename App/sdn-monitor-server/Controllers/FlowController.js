const UDPServer = require('../UDPServer')

const Event = require('../System/Event')

function startFlowScheduler () {

	setInterval(() => {

		UDPServer.send(JSON.stringify({ event : 'GET_FLOWS_MONITOR', data : [] }), 6000, '127.0.0.1')
	}, 1000)
}

function startFlowPredictionsScheduler () {

	setInterval(() => {

		UDPServer.send(JSON.stringify({ event : 'GET_FINAL_PREDICTION', data : [] }), 6000, '127.0.0.1')
	}, 1000)
}

function startTopologyScheduler () {

	setInterval(() => {

		UDPServer.send(JSON.stringify({ event : 'GET_TOPOLOGY', data : [] }), 6000, '127.0.0.1')
	}, 1000)
}

/**
* Get flow From flowCollector Server
* 
*/
function getFlows (socket) {

	return (data) => {

		UDPServer.send(JSON.stringify({ event : 'GET_FLOWS_MONITOR', data : [] }), 6000, '127.0.0.1')
	}
}

function sendFlows (io) {

	return (data) => {

		let flows = data;

		if (flows.length > 0) {

			let flowsHeader = Object.keys(flows[0])

			let flowsValues = flows.map(flow => Object.values(flow))

			io.emit('GET_FLOWS', {

				flowsHeader,
				flowsValues
			})
		}
	}
}

function sendTopology (io) {

	return (data) => {

		io.emit('GET_TOPOLOGY', data)
	}
}

function sendPredictions (io) {

	return (data) => {

		io.emit('GET_FINAL_PREDICTION', data)
	}
}

module.exports = {

	getFlows,
	sendFlows,
	sendPredictions,
	startFlowScheduler,
	startFlowPredictionsScheduler,
	startTopologyScheduler,
	sendTopology
}