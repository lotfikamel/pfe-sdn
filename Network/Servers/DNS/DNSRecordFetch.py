from scapy.all import *

import json

from DNSDomains import supported_domain_names

supported_query_types = ['A', 'TXT']

records = {}

GOOGLE_DNS_PUBLIC_SERVER = '8.8.8.8'

def fetch_dns_records () :

	for domain in supported_domain_names :

		records[domain] = {}

		for query_type in supported_query_types :

			packet = IP(dst=GOOGLE_DNS_PUBLIC_SERVER) / UDP(dport=53) / DNS(qd=DNSQR(qname=domain, qtype=query_type))

			response = sr1(packet)

			records[domain][query_type] = []

			for i in range(response[DNS].ancount) :

				rdata = response[DNS].an[i].rdata

				if type(rdata).__name__ == 'list' :

					rdata = [ d.decode('utf-8') for d in rdata ]

				records[domain][query_type].append({

					'rrname' : response[DNS].an[i].rrname.decode('utf-8'),
					'type' : response[DNS].an[i].type,
					'ttl' : response[DNS].an[i].ttl,
					'rclass' : response[DNS].an[i].rclass,
					'rdlen' : response[DNS].an[i].rdlen,
					'rdata': rdata,
				})

				response[DNS].an[i].show()

	file = open('./dns_records.json', 'w')

	json.dump(records, file, indent=3)

fetch_dns_records()
