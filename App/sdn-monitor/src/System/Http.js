import axios from 'axios'

const http = axios.create({

	baseURL : 'http://localhost:4000/',
	headers : {
		'X-Requested-With' : 'XMLHttpRequest'
	},
	withCredentials : true
});

export default http