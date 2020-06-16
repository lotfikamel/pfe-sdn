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

        self.packet_in_csv_file = './packet_in.csv'

        self.dataset_csv_file = './my_dataset.csv'

        packet_in_file = open(self.packet_in_csv_file, 'w')
        packet_in_file.write('flow_id,src_ip,src_port,dst_ip,dst_port,ip_proto \n')
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

            #print(f'flow {flow_id} has {self.flow_infos[flow_id]}')
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

            flow_id = self.get_flow_id(flow_match['ipv4_src'], flow_match['ipv4_dst'])

            self.parse_flow_match(flow_match, flow_id)

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

    def parse_flow_match(self, flow_match, flow_id) :

        if flow_match['ip_proto'] == in_proto.IPPROTO_TCP:

            packet_in_file = open(self.packet_in_csv_file, 'a+')

            packet_in_file.write("{},{},{},{},{},{}\n".format(
               flow_id, flow_match['ipv4_src'], flow_match['tcp_src'],
               flow_match['ipv4_dst'], flow_match['tcp_dst'],
               flow_match['ip_proto']))


            packet_in_file.close()

        elif flow_match['ip_proto'] == in_proto.IPPROTO_UDP:

            packet_in_file = open(self.packet_in_csv_file, 'a+')

            packet_in_file.write("{},{},{},{},{},{}\n".format(
               flow_id, flow_match['ipv4_src'], flow_match['udp_src'],
               flow_match['ipv4_dst'], flow_match['udp_dst'],
               flow_match['ip_proto']))


            packet_in_file.close()
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
        
        ethernet_protocol = pkt.get_protocols(ethernet.ethernet)[0]

        if ethernet_protocol.ethertype == ether_types.ETH_TYPE_LLDP:

            print('lldp packet received')
            # ignore lldp packet
            return

        flow_match = self.build_flow_match(packet=pkt, in_port=in_port)

        source = ethernet_protocol.src

        destination = ethernet_protocol.dst

        datapath_swicth_id = datapath.id

        self.add_mac_to_port(datapath_swicth_id, source, in_port)

        out_port = self.get_dst_out_port(ofproto, destination, datapath_swicth_id)

        actions = [parser.OFPActionOutput(out_port)]

        #install flow entry if the port is not FLOODING port to avoid packet_in next time
        if out_port != ofproto.OFPP_FLOOD:

            match = parser.OFPMatch(**flow_match)

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

    @set_ev_cls(ofp_event.EventOFPPacketIn, CONFIG_DISPATCHER)
    def packet_in_config (self, ev) :

        self.logger.info("from packet out")

