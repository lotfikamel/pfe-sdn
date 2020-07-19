<template lang="html">
	<div id="app">
		<Navbar/>
		<div class="uk-container uk-container-xlarge">
			<router-view></router-view>
		</div>
	</div>
</template>

<script>

import Navbar from '@/Components/Navbar'

import socket from '@/System/Socket'

export default {

	name : 'App',

	components : {

		Navbar
	},

	created () {

		socket.open()
	}
}	

</script>


<style lang="css">
	
html, body {

	height: 100%
}


body {

	padding-top: 100px;
}

</style>