const express = require('express');

const cors = require('cors');

const UDPServer = require('./UDPServer')

const FlowController = require('./Controllers/FlowController')

const App = express()

App.use(cors({

	origin : true,
	credentials: true,
}));

App.get('/', (req, res, next) => {

	return res.json({

		hichem : 'brahim'
	});
});

App.listen(4000, () => {

	console.log('sdn monitor server is running on port 4000...')
})