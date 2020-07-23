import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

import http from '@/System/Http'

export default new Vuex.Store({

	state: {

		data : {

			flows : {

				header : [],

				values : [],

				predictions : {}
			},

			topology : {}
		}
	},

	getters : {

		getDDOS (state) {

			let data = [];

			for (let i in state.data.flows.predictions) {

				if (state.data.flows.predictions[i].prediction == 'DrDoS') {

					data.push(state.data.flows.predictions[i].ips)
				}
			}

			return data;
		}
	},

	mutations: {

		SET_FLOW_HEADER (state, header) {

			state.data.flows.header = header
		},

		SET_FLOW_VALUES (state, values) {

			state.data.flows.values = values
		},

		SET_PREDICTIONS (state, predictions) {

			state.data.flows.predictions = predictions
		},

		SET_TOPOLOGY (state, data) {

			state.data.topology = data
		}
	},

	actions: {

		getFlows ({ commit }, data) {

			commit('SET_FLOW_HEADER', data.flowsHeader);

			commit('SET_FLOW_VALUES', data.flowsValues);
		},

		getTopology ({ commit }, data) {

			commit('SET_TOPOLOGY', data);
		},

		finalPredictions ({ commit }, data) {

			commit('SET_PREDICTIONS', data)
		}
	}
})
