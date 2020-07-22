<template>
	<div v-if="alerts.length > 0">
		<h2>Alertes</h2>
		<div v-for="(alert, index) in alerts" class="uk-alert uk-alert-danger">
			un flux <strong>{{ proto(alert) }}</strong> malveillant a été détecté
			de l'hôte <strong>{{ alert.ip_src }}:{{ alert.port_src }}</strong> vers l'hôte <strong>{{ alert.ip_dst}}:{{ alert.port_dst }}</strong>
		</div>
	</div>
</template>

<script>
	
export default {

	name : 'Alert',

	data () {

		return {

			protocols : {

				53 : 'DNS',
				123 : 'NTP'
			}
		}
	},

	computed : {

		alerts () {

			return this.$store.getters.getDDOS
		}
	},

	methods : {

		proto (alert) {

			return this.protocols[alert.port_src] || this.protocols[alert.port_dst]
		}
	}
}

</script>