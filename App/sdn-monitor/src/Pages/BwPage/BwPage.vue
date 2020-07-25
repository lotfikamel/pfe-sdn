<template lang="html">
	<div id="bw">
		<form class="uk-width-1-3 uk-margin-auto" v-on:submit.prevent="runTest">
			<div class="uk-card uk-card-default uk-card-body uk-card-small uk-border-rounded" uk-margin>
				<h3>Tester la bande passante entre deux hôtes du réseau</h3>
				<div v-if="bw.length > 0" class="uk-alert uk-alert-primary">
					<div>bande passante du <strong>{{ host1 }} est : {{ bw[0] }}</strong></div>
					<div>bande passante du <strong>{{ host2 }} est : {{ bw[1] }}</strong></div>
				</div>
				<div>
					<label class="uk-form-label">Hôte 1</label>
					<div class="uk-form-controls">
						<input v-model="host1" type="text" placeholder="ex: DNS1" class="uk-input uk-border-rounded">
					</div>
				</div>
				<div>
					<label class="uk-form-label">Hôte 2</label>
					<div class="uk-form-controls">
						<input v-model="host2" type="text" placeholder="ex: DNS2" class="uk-input uk-border-rounded">
					</div>
				</div>
				<div class="uk-margin-top uk-text-right">
					<button class="uk-button uk-button-primary">
						<span>démarer le test</span>
					</button>
				</div>
			</div>
		</form>
	</div>
</template>

<script>

import socket from '@/System/Socket'

export default {

	name : 'Bw',

	data () {

		return {

			host1 : '',
			host2 : ''
		}
	},

	computed : {

		bw () {

			return this.$store.state.data.bw
		}
	},

	methods : {

		runTest () {

			console.log(this.host1, this.host2)

			if (this.host1.trim() != '' && this.host1.trim() != '' && this.host1 != this.host2) {

				this.$store.commit('CLEAR_BW');

				socket.emit('TEST_BANDWIDTH', [this.host1, this.host2])
			}
		}
	}
}	

</script>

<style lang="css" scoped>
	
.uk-card {

	box-shadow: 0 2px 2px 0 rgba(0,0,0,0.14), 0 3px 1px -2px rgba(0,0,0,0.12), 0 1px 5px 0 rgba(0,0,0,0.2);
}

</style>