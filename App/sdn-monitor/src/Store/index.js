import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

import http from '@/System/Http'

export default new Vuex.Store({

	state: {

		data : {

			flows : {

				header : [],

				values : []
			}
		}
	},

	mutations: {

		SET_FLOW_HEADER (state, header) {

			state.data.flows.header = header
		},

		SET_FLOW_VALUES (state, values) {

			state.data.flows.values = values
		}
	},

	actions: {

		getFlows ({ commit }, data) {

			commit('SET_FLOW_HEADER', data.flowsHeader);

			commit('SET_FLOW_VALUES', data.flowsValues);
		}
	}
})
