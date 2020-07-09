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
from ryu_switch_mac_to_port import SwitchMacToPort
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

class SimpleMonitor13(SwitchMacToPort):

    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    """
        switch monitor contructor
    """
    def __init__(self, *args, **kwargs):

        super(SimpleMonitor13, self).__init__(*args, **kwargs)

        self.datapaths = {}

        self.monitor_count = 0

        self.monitoring_interval = 2

        self.monitor_thread = hub.spawn(self._monitor)

    """
        switch state event handler
    """
    @set_ev_cls(ofp_event.EventOFPStateChange, [MAIN_DISPATCHER, DEAD_DISPATCHER])
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

    """
        start monitoring every x seconds
    """
    def _monitor(self):

        while True :

            for dp in self.datapaths.values() :

                self._request_stats(dp)

            hub.sleep(self.monitoring_interval)

    """
        send the monitor request to the switch
    """
    def _request_stats(self, datapath):

        self.logger.debug('send stats request: %016x', datapath.id)

        ofproto = datapath.ofproto

        parser = datapath.ofproto_parser

        req = parser.OFPFlowStatsRequest(datapath)

        datapath.send_msg(req)

        req = parser.OFPPortStatsRequest(datapath, 0, ofproto.OFPP_ANY)

        datapath.send_msg(req)

    """
        build a match Dist
        @param {OFPMatch} match
        @return {Dict}
    """
    def flow_match_parse (self, match):

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
            'src_port': match.fields[7].value,
            'dst_port': match.fields[8].value,
            'label'   : self.find_protocol_type(match.fields[6].value)    
        }

        packet_match['flow_id'] = self.get_flow_id(packet_match['ipv4_src'], packet_match['ipv4_dst'])

      return packet_match

    """
        convert protocol code to protocol name
        @param {Int} protocol_code
        @return {String}
    """
    def find_protocol_type (self, protocol_code) :

        protocols_map = {

            17 : 'UDP',
            6 : 'TCP',
            1 : 'ICMP'            
        }

        return protocols_map.get(protocol_code, 'UNDEFINED_PROTOCOL')

    """
        convert byt mac address to string mac address
        @param {Byt} byts_addr
        @return {String}
    """
    def get_mac_addr(self, byts_addr):

      byts_str = map('{:02x}'.format, byts_addr)

      mac_addr = ':'.join(byts_str).upper()

      return mac_addr

    """
        build flow disct based on monotor data

    """
    def flow_building(self, flows) :

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
                'byte_count'    : flow.byte_count
            }

            flow_packet.update(self.flow_match_parse(flow.match))

            json_printer.dict(flow_packet)

            self.dataset_parsing(flow_packet)

    """
        calculate packet count per second and per nano second
        @param {Dict} flow_packet
        @return {Dict}
    """
    def packet_count (self, flow_packet) :

        packet_count = {}

        if flow_packet['packet_count'] == 0 :

            packet_count = {

                'packet_count_per_sec'  : 0,
                'packet_count_per_nsec' : 0
            }

        else :

            packet_count = {

                'packet_count_per_sec'  : flow_packet['duration_sec']  / flow_packet['packet_count'],
                'packet_count_per_nsec' : flow_packet['duration_nsec'] / flow_packet['packet_count']
            }

        return packet_count

    """
        calculate byt per second and per nanosecond
    """
    def flow_count(self, flow_packet) :

        packet_count = {}

        if flow_packet['byte_count'] == 0 :

            packet_count = {

                'byte_count_per_sec'  : 0,
                'byte_count_per_nsec' : 0
            }

        else :

            packet_count = {

                'byte_count_per_sec'  : flow_packet['duration_sec']  / flow_packet['byte_count'],
                'byte_count_per_nsec' : flow_packet['duration_nsec'] / flow_packet['byte_count']
            }

        return packet_count

    """
        gererate data set from monitoring data
        @param {Dict} flow_packet
        @return {Void}
    """
    def dataset_parsing (self, flow_packet) :

        if 'ip_proto' in flow_packet :

            dataset_file = open(self.dataset_csv_file, 'a+')

            flow_packet.update(self.packet_count(flow_packet))

            flow_packet.update(self.flow_count(flow_packet))

            dataset_file.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(
                           flow_packet['flow_id'],flow_packet['ipv4_src'], flow_packet['src_port'], 
                           flow_packet['ipv4_dst'], flow_packet['dst_port'], 
                           flow_packet['ip_proto'], flow_packet['duration_sec'],flow_packet['duration_nsec'],
                           flow_packet['packet_count'], flow_packet['byte_count'],flow_packet['packet_count_per_sec'],
                           flow_packet['packet_count_per_nsec'], flow_packet['byte_count_per_sec'],
                           flow_packet['byte_count_per_nsec'], flow_packet['label']))

            dataset_file.close()
  

    @set_ev_cls(ofp_event.EventOFPFlowStatsReply, MAIN_DISPATCHER)
    def _flow_stats_reply_handler(self, ev) :

        self.flow_building(ev.msg.body)