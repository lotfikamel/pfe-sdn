import socketIO from 'socket.io-client'

import Store from '@/Store/index'

const socket = socketIO('http://localhost:4000', {

	autoConnect : false
})

socket.on('connect', () => {

	console.log('connected !')
})

socket.on('GET_FLOWS', (data) => {

	Store.dispatch('getFlows', data)
});

socket.on('GET_FINAL_PREDICTION', (data) => {

	Store.dispatch('finalPredictions', data)
})

socket.on('GET_TOPOLOGY', (data) => {

	Store.dispatch('getTopology', data)
})

export default socket