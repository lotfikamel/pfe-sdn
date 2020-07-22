<template>
	<div class="uk-overflow-auto">
		<table class="uk-table uk-table-striped uk-table-small">
		    <thead>
		        <tr>
		            <th v-for="(h, index) in header" v-bind:key="index" style="font-size: 0.85rem; color: #262626">{{ h }}</th>
		        </tr>
		    </thead>
		    <tbody>
		        <tr v-for="(flow, index) in values" v-bind:class="{'ddos' : isDDOS(flow)}">
		            <td v-for="(v, index) in flow" style="font-size: 0.85rem">{{ v }}</td>
		        </tr>
		    </tbody>
		</table>
	</div>
</template>

<script>

export default {

	name : 'FlowTable',

	computed : {

		header () {

			return this.$store.state.data.flows.header
		},

		values () {

			return this.$store.state.data.flows.values
		},

		predictions () {

			return this.$store.state.data.flows.predictions
		}
	},

	methods : {

		isDDOS (flow) {

			return flow[0] in this.predictions && this.predictions[flow[0]].prediction == 'DrDoS'
		}
	}
}	

</script>

<style lang="css" scoped>
	
.ddos {

	background: #e8441c !important;
	color: #fff
}

</style>