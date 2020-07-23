<template lang="html">
	<div id="topology-page">
		<h2>Hôtes</h2>
		<HostsTable/>
		<h2 class="uk-margin-remove-top">Switches</h2>
		<SwitchesTable/>
	</div>
</template>

<script>
	
import HostsTable from './HostsTable'

import SwitchesTable from './SwitchesTable'

export default {

	name : 'TopologyPage',

	components : {

		HostsTable,
		SwitchesTable
	}
}

</script>

<style lang="css"></style>