<template lang="html">
	<div id="app">
		<Navbar/>
		<div class="uk-container">
			<router-view></router-view>
		</div>
	</div>
</template>

<script>

import Navbar from '@/Components/Navbar'

import http from '@/Config/Http'

export default {

	name : 'App',

	components : {

		Navbar
	},

	created () {

		http.get('/').then(res => {

			console.log(res.data)
		})
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