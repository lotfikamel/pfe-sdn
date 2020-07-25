<template lang="html">
	<div id="navbar" class="uk-background-default">
		<div class="uk-container uk-container-xlarge"> 
			<nav uk-navbar>
				<a href="#" class="uk-navbar-item uk-logo">SDN-Monitor</a>
			    <div class="uk-navbar-right">
			        <ul class="uk-navbar-nav">
			        		<li class="uk-active"><router-link to='/'>Flux</router-link></li>
			        		<li class="uk-active"><router-link to='/topology'>topologie</router-link></li>
			        		<li class="uk-active"><router-link to='/bw'>bande passante</router-link></li>
			        </ul>
			    </div>
			</nav>
		</div>
	</div>
</template>

<script>
	
export default {

	name : 'Navbar'
}

</script>

<style lang="css" scoped>

#navbar {

	position: fixed;
	top: 0;
	left: 0;
	right: 0;
	box-shadow: 0 2px 2px 0 rgba(0,0,0,0.14), 0 3px 1px -2px rgba(0,0,0,0.12), 0 1px 5px 0 rgba(0,0,0,0.2);
	z-index: 1000
}

</style>