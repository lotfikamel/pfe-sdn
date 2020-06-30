import socket, binascii
import struct
import textwrap

TAB1 = '\t'
TAB2 = '\t\t'
TAB3 = '\t\t\t'

def main():
	
	connection = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))

	while True:

		raw_data, addres = connection.recvfrom(65536)


		dst_mac, src_mac, eth_proto, data = ethernet_unpack(raw_data)


		print('-Ethernet packet \n')
		print(TAB1 + '- source : {} Destination : {} protocol : {} '.format( src_mac,dst_mac, eth_proto))

		if (eth_proto == 8):

			ipv4_unpack_data = ipv4_unpack(data)

			ip_ttl           = ipv4_unpack_data['ttl']
			ip_src           = ipv4_unpack_data['src']
			ip_dst           = ipv4_unpack_data['dst']
			ip_proto         = ipv4_unpack_data['proto']
			ip_data  		 = ipv4_unpack_data['data']
			ip_header_length = ipv4_unpack_data['header_length']
			ip_version       = ipv4_unpack_data['version']

			print(TAB1 + '- IPV4 packet')
			print(TAB2 + '- version: {} TTL : {} header Length : {} '.format(ip_version, ip_ttl, ip_header_length))
			print(TAB2 + '- source : {} Destination : {} protocol : {} '.format(ip_src, ip_dst, ip_proto))

			if (ip_proto == 1):

				icmp_unpack_data = icmp_unpack(ip_data)

				icmp_code      = icmp_unpack_data['code']
				icmp_chucksum  = icmp_unpack_data['chucksum']
				icmp_type 	   = icmp_unpack_data['icmp_type']

				print(TAB1 + '- ICMP packet')
				print(TAB1 + '- icmp type : {} code : {} chucksum : {} '.format(icmp_type, icmp_code, icmp_chucksum))

				print('\n')

			elif (ip_proto == 6):

				tcp_unpack_data = tcp_unpack(ip_data)

				tcp_src_port = tcp_unpack_data['src_port']
				tcp_dst_port = tcp_unpack_data['dst_port']
				tcp_flags    = tcp_unpack_data['flags']
				tcp_sequence = tcp_unpack_data['sequence']
				tcp_ack      = tcp_unpack_data['ack']

				print(TAB1 + '- TCP packet')
				print(TAB2 + '- source port : {} dest port : {}  '.format(tcp_src_port, tcp_dst_port))
				print(TAB2 + '- sequence : {} ACK : {}  '.format(tcp_sequence, tcp_ack))
				print(TAB2 + '- Flags : ')
				print(TAB3 + '- URG : {flag_urg} ACK :  {flag_ack} PSH : {flag_psh} SYN : {flag_syn} FIN :{flag_fin}  '.format(**tcp_flags))

				print('\n')

			elif (ip_proto == 17):

				udp_unpack_data = udp_unpack(ip_data)

				udp_src_port = udp_unpack_data['src_port']
				udp_dst_port = udp_unpack_data['dst_port']
				udp_size     = udp_unpack_data['size']

				print(TAB1 + '- UDP packet')
				print(TAB2 + '- source port : {} dest port : {} size : {} '.format(udp_src_port, udp_dst_port, udp_size))

				print('\n')
		

		

## unpack the ethernet data
def ethernet_unpack(data):

	dst_mac, src_mac, proto = struct.unpack('! 6s 6s H', data[:14])

	return get_mac_addr(dst_mac), get_mac_addr(src_mac), socket.htons(proto), data[14:]

def get_mac_addr(byts_addr):

	byts_str = map('{:02x}'.format, byts_addr)

	mac_addr = ':'.join(byts_str).upper()

	return mac_addr

def ipv4_unpack(data):

	version_header_length = data[0]

	version = version_header_length >> 4

	header_length = (version_header_length & 15) * 4

	ttl,  proto, src, dst = struct.unpack('!8xBB2x4s4s', data[:20])

	ipv4_data = {

		'header_length' : header_length,
		'version' 		: version,
		'ttl' 			: ttl,
		'proto' 		: proto,
		'src' 			: ipv4(src),
		'dst' 			: ipv4(dst),
		'data'          : ipv4(data[header_length:])
	}

	return ipv4_data

def ipv4(addres):

	ipv4_address = '.'.join(map(str, addres))

	return ipv4_address

def icmp_unpack(data):

	icmp_type, code, chucksum = struct.unpack('!BBH', bytes(data[:4],'utf8'))

	icmp_data = {

		'icmp_type' : icmp_type,
		'code'      : code,
		'chucksum'  : chucksum
	}
	return icmp_data

def tcp_unpack(data):

	src_port, dst_port, sequence, ack, offset_reserved_flags = struct.unpack('!2H2LH', bytes(data[:14], 'utf8'))

	offset = (offset_reserved_flags >> 12) * 4
	flag_urg = (offset_reserved_flags >> 32) * 5
	flag_ack = (offset_reserved_flags >> 16) * 4
	flag_psh = (offset_reserved_flags >> 8) * 4
	flag_rst = (offset_reserved_flags >> 4) * 2
	flag_syn = (offset_reserved_flags >> 2) * 1
	flag_fin = offset_reserved_flags >> 1

	flags    = {

		'flag_urg' : flag_urg,
		'flag_ack' : flag_ack,
		'flag_psh' : flag_psh,
		'flag_syn' : flag_syn,
		'flag_fin' : flag_fin
	} 

	tcp_data = {

		'src_port' : src_port,
		'dst_port' : dst_port,
		'sequence' : sequence,
		'flags'    : flags,
		'ack'      : ack,
		'data'     : data[offset:]
	}

	return tcp_data

def udp_unpack(data):

	src_port, dst_port, size = struct.unpack('!HH2xH',bytes(data[:8],'utf8'))

	udp_data = {

		'src_port' : src_port,
		'dst_port' : dst_port,
		'size'     : size,
		'data'     : data[8:]
	}

	return udp_data

## formats multi-line data





main()