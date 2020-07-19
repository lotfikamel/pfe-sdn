<template lang="html">
	<div id="flow-page">
		<h2>Flux</h2>
		<FlowTable/>
	</div>
</template>

<script>

import FlowTable from './FlowTable'

import socket from '@/System/Socket'

export default {

	name : 'FlowPage',
	components : {

		FlowTable
	},

	created () {

		socket.emit('GET_FLOWS')
	}
}	

</script>

<style lang="css" scoped>
	

</style>