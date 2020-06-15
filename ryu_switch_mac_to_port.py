from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER, HANDSHAKE_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet, tcp, udp, icmp, ipv4, arp, openflow, ipv6, in_proto
from ryu.lib.packet import ether_types
from helpers import json_printer
from operator import attrgetter

# from ryu.app import simple_switch_13
import ryu_switch_mac_to_port
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, DEAD_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.lib import hub
from helpers import json_printer
import json
import ipaddress
from helpers import json_printer
from datetime import datetime
from pprint import pprint 

import array
import socket
import struct
import textwrap
import time

TAB1 = '\t'
TAB2 = '\t\t'
TAB3 = '\t\t\t'

class SwitchMacToPort(app_manager.RyuApp):

    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):

        super(SwitchMacToPort, self).__init__(*args, **kwargs)

        # mac to port table
        # format : { datapath_swicth_id : {mac : port} }
        self.mac_to_port = {}

        ###
        # Track flow calculated attr
        # { "flow_id" : {  } }
        ##
        self.flow_infos = {}

        self.packet_in_csv_file = '/home/lotfi/pfe/ryu-codes/packet_in.csv'

        self.dataset_csv_file = '/home/lotfi/pfe/ryu-codes/my_dataset.csv'

        self.siwtch_flow_id = 0
        packet_in_file = open(self.packet_in_csv_file, 'w')
        packet_in_file.write('flow_id,src_ip,src_port,dst_ip,dst_port,ip_proto,total_length \n')
        packet_in_file.close()

    def __str__ (self) :

        return str(self.__dict__)

    """
        add new entry to the flow table
    """
    def add_flow_entry (self, datapath, priority, match, actions, buffer_id=None) :

        ofproto = datapath.ofproto

        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]

        if buffer_id:

            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id, priority=priority, match=match, instructions=inst)
        else:

            mod = parser.OFPFlowMod(datapath=datapath, priority=priority, match=match, instructions=inst)

        datapath.send_msg(mod)

    def get_dst_out_port (self, ofproto, destination, datapath_swicth_id) :

        if destination in self.mac_to_port[datapath_swicth_id] :

            return self.mac_to_port[datapath_swicth_id][destination]

        return ofproto.OFPP_FLOOD

    """
        add mac to port
    """
    def add_mac_to_port (self, datapath_swicth_id, mac, port) :

        if datapath_swicth_id not in self.mac_to_port :

            self.mac_to_port[datapath_swicth_id] = {}

        self.mac_to_port[datapath_swicth_id][mac] = port

    """
        build flow flow id based on ip src and ip dst
        @param {String} ipv4_src
        @param {String} ipv4_dst
        @return {String}
    """
    def get_flow_id (self, ipv4_src, ipv4_dst) :
        
        return f'{ipv4_src}-{ipv4_dst}'

    """
        update flow infos on packet in
        @param {Dict} flow_match
    """
    def update_flow_infos (self, flow_match) :
        
        flow_id = self.get_flow_id(flow_match['ipv4_src'], flow_match['ipv4_dst'])

        if flow_id not in self.flow_infos :

            print(f'first packet in for the flow {flow_id}')

            self.flow_infos[flow_id] = 1

        else :

            self.flow_infos[flow_id] += 1

            print(f'flow {flow_id} has {self.flow_infos[flow_id]}')
    """
        build the full match flow based on
        protocol stack in received packet
        @param {List<Object>}
        @return {Dictionery}
    """
    def build_flow_match (self, packet, in_port):

        flow_match = {

            'in_port' : in_port,
        }

        ethernet_packet = packet.get_protocols(ethernet.ethernet)[0]

        if ethernet_packet.ethertype == ether_types.ETH_TYPE_IP:

            flow_match['eth_src']  = ethernet_packet.src
            flow_match['eth_dst']  = ethernet_packet.dst
            flow_match['eth_type'] = ethernet_packet.ethertype

            ipv4_layer = packet.get_protocol(ipv4.ipv4)

            flow_match['ipv4_src'] = ipv4_layer.src
            flow_match['ipv4_dst'] = ipv4_layer.dst

            protocol = ipv4_layer.proto

            if protocol == in_proto.IPPROTO_ICMP:

                icmp_packet = packet.get_protocol(icmp.icmp)

                # print(payload)

                flow_match['ip_proto'] = protocol
                flow_match['icmpv4_code'] = icmp_packet.code
                flow_match['icmpv4_type'] = icmp_packet.type

            elif protocol == in_proto.IPPROTO_TCP:

                tcp_packet = packet.get_protocol(tcp.tcp)

                flow_match['ip_proto'] = protocol
                flow_match['tcp_src'] = tcp_packet.src_port
                flow_match['tcp_dst'] = tcp_packet.dst_port

            elif protocol == in_proto.IPPROTO_UDP:

                udp_packet = packet.get_protocol(udp.udp)

                flow_match['ip_proto'] = protocol
                flow_match['udp_src'] = udp_packet.src_port
                flow_match['udp_dst'] = udp_packet.dst_port



            # json_printer.o(flow_match)

        if 'ip_proto' in flow_match :

            self.update_flow_infos(flow_match)

        return flow_match

    """
        install the miss flow entry to match all packets
        with EMPTY match
    """
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):

        self.logger.info('staring switch_features_handler')

        msg = ev.msg

        datapath = msg.datapath

        ofproto = datapath.ofproto

        parser = datapath.ofproto_parser

        #create wildcard or empty match
        match = parser.OFPMatch()

        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER, ofproto.OFPCML_NO_BUFFER)]

        self.add_flow_entry(datapath, 0, match, actions)

        self.logger.info('ending switch_features_handler')

    def parse_flow_match(self, packet_in, in_port):

        full_packet_in = {}

        packets = packet_in.get_protocols(ipv4.ipv4)

        for packet in packets:

            full_packet_in['total_length'] =  packet.total_length


        full_packet_in.update(self.build_flow_match(packet_in, in_port))

        self.siwtch_flow_id += 1

        if len(full_packet_in) > 1:


            if full_packet_in['ip_proto'] == in_proto.IPPROTO_TCP:

                packet_in_file = open(self.packet_in_csv_file, 'a+')

                packet_in_file.write("{},{},{},{},{},{},{}\n".format(
                   self.siwtch_flow_id, full_packet_in['ipv4_src'], full_packet_in['tcp_src'],
                   full_packet_in['ipv4_dst'], full_packet_in['tcp_dst'],
                   full_packet_in['ip_proto'],full_packet_in['total_length']))


                packet_in_file.close()

            elif full_packet_in['ip_proto'] == in_proto.IPPROTO_UDP:

                packet_in_file = open(self.packet_in_csv_file, 'a+')

                packet_in_file.write("{},{},{},{},{},{},{}\n".format(
                   self.siwtch_flow_id, full_packet_in['ipv4_src'], full_packet_in['udp_src'],
                   full_packet_in['ipv4_dst'], full_packet_in['udp_dst'],
                   full_packet_in['ip_proto'],full_packet_in['total_length']))


                packet_in_file.close()

        # pprint(full_packet_in)
    """
        packet in event handler
    """
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler (self, ev) :

        msg = ev.msg

        datapath = msg.datapath

        ofproto = datapath.ofproto

        parser = datapath.ofproto_parser

        in_port = msg.match.get('in_port')

        pkt = packet.Packet(msg.data)

        self.parse_flow_match(pkt, in_port=in_port)
        
        ethernet_protocol = pkt.get_protocols(ethernet.ethernet)[0]

        # print('ethernet type' , ethernet_protocol.ethertype)

        if ethernet_protocol.ethertype == ether_types.ETH_TYPE_LLDP:

            print('lldp packet received')
            # ignore lldp packet
            return

        flow_match = self.build_flow_match(packet=pkt, in_port=in_port)

        source = ethernet_protocol.src

        destination = ethernet_protocol.dst

        datapath_swicth_id = datapath.id

        #self.logger.info(f'packet_in event : source {source}, destination {destination}, in_port {in_port} from switch : {datapath_swicth_id}')

        self.add_mac_to_port(datapath_swicth_id, source, in_port)



        #json_printer.args(source=source, destination=destination, swicth_id=datapath_swicth_id)

        #json_printer.o(self.mac_to_port)

        out_port = self.get_dst_out_port(ofproto, destination, datapath_swicth_id)

        actions = [parser.OFPActionOutput(out_port)]

        #install flow entry if the port is not FLOODING port to avoid packet_in next time
        if out_port != ofproto.OFPP_FLOOD:

            # print('installing flow on the switch', json_printer.o(flow_match))

            match = parser.OFPMatch(**flow_match)

            #match = parser.OFPMatch(in_port=in_port, eth_type=ethernet_protocol.ethertype, eth_dst=destination, eth_src=source, ipv4_src=ipv4_protocol.src, ipv4_dst=ipv4_protocol.dst)

            if msg.buffer_id != ofproto.OFP_NO_BUFFER :

                self.add_flow_entry(datapath, 1, match, actions, msg.buffer_id)

                return
            else:

                self.add_flow_entry(datapath, 1, match, actions)

        else : 

            print('the out port is FLOODING port no flow installation will be done')
        data = None

        if msg.buffer_id == ofproto.OFP_NO_BUFFER :

            data = msg.data

            out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id, in_port=in_port, actions=actions, data=data)

        datapath.send_msg(out)

        # print('*'*100)

    @set_ev_cls(ofp_event.EventOFPPacketIn, CONFIG_DISPATCHER)
    def packet_in_config (self, ev) :

        self.logger.info("from packet out")



class SimpleMonitor13(SwitchMacToPort):

    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SimpleMonitor13, self).__init__(*args, **kwargs)
        self.datapaths = {}
        self.monitor_flow_id = 1
        self.monitor_count = 0
        self.monitor_thread = hub.spawn(self._monitor)

    @set_ev_cls(ofp_event.EventOFPStateChange,
                [MAIN_DISPATCHER, DEAD_DISPATCHER])
    def _state_change_handler(self, ev):
        datapath = ev.datapath
        if ev.state == MAIN_DISPATCHER:
            if datapath.id not in self.datapaths:
                self.logger.debug('register datapath: %016x', datapath.id)
                self.datapaths[datapath.id] = datapath
        elif ev.state == DEAD_DISPATCHER:
            if datapath.id in self.datapaths:
                self.logger.debug('unregister datapath: %016x', datapath.id)
                del self.datapaths[datapath.id]

    def _monitor(self):
        while True:
            for dp in self.datapaths.values():
                self._request_stats(dp)
            hub.sleep(0.1)

    def _request_stats(self, datapath):
        self.logger.debug('send stats request: %016x', datapath.id)
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        req = parser.OFPFlowStatsRequest(datapath)


        # self.monitor_count += 1
        # print('the monitore count ', self.monitor_count)

        datapath.send_msg(req)

        req = parser.OFPPortStatsRequest(datapath, 0, ofproto.OFPP_ANY)
        datapath.send_msg(req)

    def flow_match_parse(self, match):

      packet_match = {}


      if len(match.fields) == 9:


        packet_match = {

            'in_port' :  match.fields[0].value,
            'eth_src' : self.get_mac_addr(match.fields[1].value),
            'eth_dst' : self.get_mac_addr(match.fields[2].value),
            'eth_type': match.fields[3].value,
            'ipv4_src': str(ipaddress.IPv4Address(match.fields[4].value)),
            'ipv4_dst': str(ipaddress.IPv4Address(match.fields[5].value)),
            'ip_proto': match.fields[6].value,
            # '{}'.format(self.find_protocol_type(match.fields[6].value)) + '_src' : match.fields[7].value,
            # '{}'.format(self.find_protocol_type(match.fields[6].value)) + '_dst' : match.fields[8].value,
            'src_port': match.fields[7].value,
            'dst_port': match.fields[8].value,
            'label'   : self.find_protocol_type(match.fields[6].value)
            
        }

      # json_printer.o(packet_match)
      return packet_match




    def find_protocol_type (self, protocol_type):

      if protocol_type == 17:

        return 'UDP'

      elif protocol_type == 6:

        return 'TCP'

      elif protocol_type == 1:

        return 'ICMP'

    def get_mac_addr(self, byts_addr):

      byts_str = map('{:02x}'.format, byts_addr)

      mac_addr = ':'.join(byts_str).upper()

      return mac_addr

    def flow_building(self, flows) :

        self.monitor_flow_id = 1

        dataset_file = open(self.dataset_csv_file, 'w+')

        dataset_file.write('flow_id,src_ip,src_port,dst_ip,dst_port,protocol,flow_duration,flow_duration_nsec,packet_count,byte_count,packet_count_per_sec,packet_count_per_nsec,byte_count_per_sec,byte_count_per_nsec,label\n')
     
        dataset_file.close()

        for flow in flows:

            flow_packet = {

                'table_id'      : flow.table_id,
                'duration_sec'  : flow.duration_sec,
                'duration_nsec' : flow.duration_nsec,
                'priority'      : flow.priority,
                'idle_timeout'  : flow.idle_timeout,
                'hard_timeout'  : flow.hard_timeout,
                'flags'         : flow.flags,
                'cookie'        : flow.cookie,
                'packet_count'  : flow.packet_count,
                'byte_count'    : flow.byte_count,
                #'time_stamp'    : datetime.utcnow().strftime('%H:%M:%S.%f')
            }

            flow_packet.update(self.flow_match_parse(flow.match))

            # json_printer.o(flow_packet)

            self.dataset_parsing(flow_packet)

    def packet_count(self, flow_packet):

      packet_count = {}

      try:

        packet_count_per_sec  = flow_packet['duration_sec']  / flow_packet['packet_count']
        packet_count_per_nsec = flow_packet['duration_nsec'] / flow_packet['packet_count']

        packet_count = {

            'packet_count_per_sec'  : packet_count_per_sec,
            'packet_count_per_nsec' : packet_count_per_nsec
        }

        # json_printer.o(packet_count)
        return packet_count



      except:

        packet_count_per_sec  = 0
        packet_count_per_nsec = 0

        packet_count = {

            'packet_count_per_sec'  : -1,
            'packet_count_per_nsec' : -1
        }

        return packet_count

    def flow_count(self, flow_packet):

      flow_count = {}

      try:

        flow_count_per_sec   = flow_packet['duration_sec']  / flow_packet['byte_count']
        flow_count_per_nsec  = flow_packet['duration_nsec'] / flow_packet['byte_count']

        flow_count = {

            'byte_count_per_sec'  : flow_count_per_sec,
            'byte_count_per_nsec' : flow_count_per_nsec
        }

        # json_printer.o(flow_count)
        return flow_count



      except:

        flow_count_per_sec  = 0
        flow_count_per_nsec = 0

        flow_count = {

            'byte_count_per_sec'  : -1,
            'byte_count_per_nsec' : -1
        }

        return flow_count


    def dataset_parsing(self, flow_packet):

        if len(flow_packet) == 20 :

            dataset_file = open(self.dataset_csv_file, 'a+')


            # self.packet_count(flow_packet)
            # self.flow_count(flow_packet)

            flow_packet.update(self.packet_count(flow_packet))
            flow_packet.update(self.flow_count(flow_packet))

            #json_printer.o(flow_packet)

            

            dataset_file.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(
                           self.monitor_flow_id,flow_packet['ipv4_src'], flow_packet['src_port'], 
                           flow_packet['ipv4_dst'], flow_packet['dst_port'], 
                           flow_packet['ip_proto'], flow_packet['duration_sec'],flow_packet['duration_nsec'],
                           flow_packet['packet_count'], flow_packet['byte_count'],flow_packet['packet_count_per_sec'],
                           flow_packet['packet_count_per_nsec'], flow_packet['byte_count_per_sec'],
                           flow_packet['byte_count_per_nsec'], flow_packet['label']))


            dataset_file.close()

            self.monitor_flow_id += 1
  

    @set_ev_cls(ofp_event.EventOFPFlowStatsReply, MAIN_DISPATCHER)
    def _flow_stats_reply_handler(self, ev):
  
      self.flow_building(ev.msg.body)

