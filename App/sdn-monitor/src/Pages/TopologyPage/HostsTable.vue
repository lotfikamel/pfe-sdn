<template>
	<div v-if="hosts.length > 0" class="uk-overflow-auto">
		<table class="uk-table uk-table-striped uk-table-small">
		    <thead>
		        <tr>
		            <th v-for="(a, index) in attr" v-bind:key="index" style="font-size: 0.85rem; color: #262626">{{ a }}</th>
		        </tr>
		    </thead>
		    <tbody>
		        <tr v-for="(host, index) in hosts">
		            <td v-for="(h, key) in host" style="font-size: 0.85rem">
		            	<span v-if="key == 'name'">{{ h }}</span>
		            	<span v-if="key == 'mac'">{{ h }}</span>
		            	<span v-if="key == 'ipv4'">{{ h[0] }}</span>
		            	<span v-if="key == 'ipv6'">{{ h[1] }}</span>
		            	<div v-if="key == 'port'">
		            		<div v-for="(port, k) in h">{{ k }} : {{ port }}</div>
		            	</div>
		            </td>
		        </tr>
		    </tbody>
		</table>
	</div>
</template>

<script>

export default {

	name : 'HostsTable',

	computed : {

		hosts () {

			return this.$store.state.data.topology.hosts
		},

		attr () {

			return Object.keys(this.hosts[0])
		}
	}
}	

</script>

<style lang="css" scoped>
	
</style>0