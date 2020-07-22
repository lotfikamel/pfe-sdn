<template lang="html">
	<div id="app">
		<Navbar/>
		<div class="uk-container uk-container-xlarge">
			<Alert/>
			<router-view></router-view>
		</div>
	</div>
</template>

<script>

import Navbar from '@/Components/Navbar'

import Alert from '@/Components/Alert'

import socket from '@/System/Socket'

export default {

	name : 'App',

	components : {

		Navbar,
		Alert
	},

	created () {

		socket.open()
	}
}	

</script>


<style lang="css">
	
body {

	padding-top: 100px;
}

</style>