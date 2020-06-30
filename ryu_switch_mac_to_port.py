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

import os

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
        build the full match flow based on
        protocol stack in received packet
        @param {List<Object>}
        @return {Dictionery}
    """
    def build_flow_match (self, packet, in_port):

        flow_match = {

            'in_port' : in_port,
        }

        for protocol in packet.protocols:

            if protocol.protocol_name == 'ethernet' :

                flow_match['eth_src'] = protocol.src
                flow_match['eth_dst'] = protocol.dst
                flow_match['eth_type'] = protocol.ethertype

            if protocol.protocol_name == 'ipv4' :

                flow_match['ipv4_src'] = protocol.src
                flow_match['ipv4_dst'] = protocol.dst
                flow_match['ip_proto'] = protocol.proto

            elif protocol.protocol_name == 'ipv6' :

                print('packet ip version 6')

                flow_match['ipv6_src'] = protocol.src
                flow_match['ipv6_dst'] = protocol.dst

            if protocol.protocol_name == 'tcp' :

                flow_match['tcp_src'] = protocol.src_port
                flow_match['tcp_dst'] = protocol.dst_port

            if protocol.protocol_name == 'udp' :

                flow_match['udp_src'] = protocol.src_port
                flow_match['udp_dst'] = protocol.dst_port

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

