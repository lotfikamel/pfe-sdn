<template>
	<div v-if="switches.length > 0" class="uk-overflow-auto">
		<div v-for="sw in switches">
			<h3> switche {{ sw.dpid }}</h3>
			<table class="uk-table uk-table-striped uk-table-small">
			    <thead>
			        <tr>
			            <th v-for="(a, index) in Object.keys(switches[0].ports[0])" v-bind:key="index" style="font-size: 0.85rem; color: #262626">{{ a }}</th>
			        </tr>
			    </thead>
			    <tbody>
			        <tr v-for="(port, index) in sw.ports">
			            <td v-for="(h, key) in port" style="font-size: 0.85rem">
			            	{{ h }}
			            </td>
			        </tr>
			    </tbody>
			</table>
		</div>
	</div>
</template>

<script>

export default {

	name : 'SwitchesTable',

	computed : {

		switches () {

			return this.$store.state.data.topology.switches
		},

		attr () {

			return Object.keys(this.switches[0])
		}
	}
}	

</script>

<style lang="css" scoped>
	
</style>