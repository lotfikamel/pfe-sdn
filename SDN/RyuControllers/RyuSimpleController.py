import sys

import subprocess

sys.path.append('/home/lotfi/pfe/PFE')

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER, HANDSHAKE_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet, tcp, udp, icmp, ipv4, arp, openflow, ipv6, in_proto
from ryu.lib.packet import ether_types
from ryu.lib import hub

from ryu.topology.api import *

import socket

import pickle

import json

import copy

from Helpers import json_printer
from Helpers.CmdAsync import CmdAsync
from MachineLearning.Classifiers.DrDoSDNSClassifier import DrDoSDNSClassifier

class SwitchMacToPort(app_manager.RyuApp):

    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):

        super(SwitchMacToPort, self).__init__(*args, **kwargs)

        self.nodejs_server = CmdAsync(['node', '/home/lotfi/pfe/PFE/App/sdn-monitor-server/Server.js'])

        # run monitor server as thread
        self.nodejs_server.start()

        # mac to port table
        # format : { datapath_swicth_id : {mac : port} }
        self.mac_to_port = {}

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.sock.settimeout(1)

        self.PREDICTION_MAX_COUNT = 3

        #flow collector threaed
        self.flow_collector_thread = hub.spawn(self._collect_flows)

        #flow collection interval
        self.flow_collection_interval = 2

        #flow prediction
        self.flow_predictions = {}

        self.topology = {}

    """
        collect flow from the flow collector device
    """
    def _collect_flows (self) :

        while True :

            data = bytes(json.dumps({ 'event' : 'GET_FLOWS', 'data' : [] }), 'utf-8')

            self.sock.sendto(data, ('127.0.0.1', 6000))

            self.update_topology()

            try :

                data, address = self.sock.recvfrom(65000)

                flows = pickle.loads(data)
            
                if len(flows) > 0 :

                    flow_ids = list(flows.keys())

                    flow_values = list(flows.values())

                    predictions = DrDoSDNSClassifier.predict(flow_values)

                    self.update_flow_predictions(flow_ids, flow_values, predictions)

                else :

                    print('no flow to classify')
            except Exception as e:

                print('FlowCollector Server is off try next time', e)

            hub.sleep(self.flow_collection_interval)

    """
        update flows prediction status
        @param {List<String>} flow_ids
        @param {List<List>} flow_values
        @param {List<String>} predictions
        @return {Void}
    """
    def update_flow_predictions (self, flow_ids, flow_values, predictions) :

        for i in range(len(predictions)) :

            if flow_ids[i] not in self.flow_predictions :

                self.flow_predictions.update({

                    flow_ids[i] : {

                        'predicted_as' : {

                            'BENIGN' : 0,
                            'DrDoS' : 0
                        },

                        'prediction_count' : 0
                    }
                })


            if self.flow_predictions[flow_ids[i]]['prediction_count'] !=0 and self.flow_predictions[flow_ids[i]]['prediction_count']%self.PREDICTION_MAX_COUNT == 0:

                as_benign = self.flow_predictions[flow_ids[i]]['predicted_as']['BENIGN']

                as_ddos = self.flow_predictions[flow_ids[i]]['predicted_as']['DrDoS']

                final_prediction = 'BENIGN' if as_benign > as_ddos else 'DrDoS'

                data = bytes(json.dumps({ 'event' : 'FINAL_PREDICTION', 'data' : { flow_ids[i] : final_prediction } }), 'utf-8')

                self.sock.sendto(data, ('127.0.0.1', 6000))

                print('\033[1;33m' + '\033[1;31m'+ f'flow {flow_ids[i]} predicted as {final_prediction}' + '\033[0m')

            self.flow_predictions[flow_ids[i]]['predicted_as'][predictions[i]] += 1

            self.flow_predictions[flow_ids[i]]['prediction_count'] += 1

    """
    
        update topology infos
    """
    def update_topology (self) :

        hosts = copy.copy(get_all_host(self))

        switches = copy.copy(get_all_switch(self))

        self.topology['hosts'] = [ host.to_dict() for host in hosts]

        self.topology['switches'] = [ switch.to_dict() for switch in switches]

        data = bytes(json.dumps({ 'event' : 'UPDATE_TOPOLOGY', 'data' : self.topology }), 'utf-8')

        self.sock.sendto(data, ('127.0.0.1', 6000))


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
    def build_flow_match (self, packet, in_port) :

        flow_match = {

            'in_port' : in_port,
        }

        ethernet_packet = packet.get_protocols(ethernet.ethernet)[0]


        flow_match['eth_src']  =  ethernet_packet.src
        flow_match['eth_dst']  = ethernet_packet.dst
        flow_match['eth_type'] = ethernet_packet.ethertype

        ipv4_layer = packet.get_protocol(ipv4.ipv4)


        if ipv4_layer :

            flow_match['ipv4_src'] = ipv4_layer.src
            flow_match['ipv4_dst'] = ipv4_layer.dst

            protocol = ipv4_layer.proto

            if protocol == in_proto.IPPROTO_ICMP:

                icmp_packet = packet.get_protocol(icmp.icmp)

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

        if out_port != ofproto.OFPP_FLOOD:

            match = parser.OFPMatch(**flow_match)

            if msg.buffer_id != ofproto.OFP_NO_BUFFER :

                self.add_flow_entry(datapath, 1, match, actions, msg.buffer_id)

                return
            else:

                self.add_flow_entry(datapath, 1, match, actions)
                
        data = None

        if msg.buffer_id == ofproto.OFP_NO_BUFFER :

            data = msg.data

            out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id, in_port=in_port, actions=actions, data=data)

        datapath.send_msg(out)
