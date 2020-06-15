# Copyright (C) 2016 Nippon Telegraph and Telephone Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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


class SimpleMonitor13(ryu_switch_mac_to_port.SwitchMacToPort):

    def __init__(self, *args, **kwargs):
        super(SimpleMonitor13, self).__init__(*args, **kwargs)
        self.datapaths = {}
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
            hub.sleep(.1)

    def _request_stats(self, datapath):
        self.logger.debug('send stats request: %016x', datapath.id)
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        req = parser.OFPFlowStatsRequest(datapath)

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
            '{}'.format(self.find_protocol_type(match.fields[6].value)) + '_src' : match.fields[7].value,
            '{}'.format(self.find_protocol_type(match.fields[6].value)) + '_dst' : match.fields[8].value,
            'label'   : self.find_protocol_type(match.fields[6].value)
            
        }


      return packet_match

    def find_protocol_type (self, protocol_type):

      if protocol_type == 17:

        return 'udp'

      elif protocol_type == 6:

        return 'tcp'

      elif protocol_type == 1:

        return 'icmp'

    def get_mac_addr(self, byts_addr):

      byts_str = map('{:02x}'.format, byts_addr)

      mac_addr = ':'.join(byts_str).upper()

      return mac_addr

    def flow_building(self, flows):
     
        for flow in flows:

          # timestamp = 

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
              'time_stamp'    : datetime.utcnow().strftime('%H:%M:%S.%f')
          }

          flow_packet.update(self.flow_match_parse(flow.match))

          json_printer.o(flow_packet)


    @set_ev_cls(ofp_event.EventOFPFlowStatsReply, MAIN_DISPATCHER)
    def _flow_stats_reply_handler(self, ev):

  
      self.flow_building(ev.msg.body)






      # flows = []
      # for stat in ev.msg.body:
      #     flows.append('table_id=%s '
      #                  'duration_sec=%d duration_nsec=%d '
      #                  'priority=%d '
      #                  'idle_timeout=%d hard_timeout=%d flags=0x%04x '
      #                  'cookie=%d packet_count=%d byte_count=%d '
      #                  'match=%s instructions=%s' %
      #                  (stat.table_id,
      #                   stat.duration_sec, stat.duration_nsec,
      #                   stat.priority,
      #                   stat.idle_timeout, stat.hard_timeout, stat.flags,
      #                   stat.cookie, stat.packet_count, stat.byte_count,
      #                   stat.match, stat.instructions))
      # # self.logger.debug('FlowStats: %s', flows)
      # print(flows)

        


        # self.logger.info('datapath         '
        #                  'in-port  eth-dst           '
        #                  'out-port packets  bytes')
        # self.logger.info('---------------- '
        #                  '-------- ----------------- '
        #                  '-------- -------- --------')
        # for stat in sorted([flow for flow in body if flow.priority == 1],
        #                    key=lambda flow: (flow.match['in_port'],
        #                                      flow.match['eth_dst'])):
        #     self.logger.info('%016x %8x %17s %8x %8d %8d',
        #                      ev.msg.datapath.id,
        #                      stat.match['in_port'], stat.match['eth_dst'],
        #                      stat.instructions[0].actions[0].port,
        #                      stat.packet_count, stat.byte_count)

    @set_ev_cls(ofp_event.EventOFPPortStatsReply, MAIN_DISPATCHER)
    def _port_stats_reply_handler(self, ev):
        body = ev.msg.body

        ports = []
        for stat in ev.msg.body:
            ports.append('port_no=%d '
                         'rx_packets=%d tx_packets=%d '
                         'rx_bytes=%d tx_bytes=%d '
                         'rx_dropped=%d tx_dropped=%d '
                         'rx_errors=%d tx_errors=%d '
                         'rx_frame_err=%d rx_over_err=%d rx_crc_err=%d '
                         'collisions=%d duration_sec=%d duration_nsec=%d' %
                         (stat.port_no,
                          stat.rx_packets, stat.tx_packets,
                          stat.rx_bytes, stat.tx_bytes,
                          stat.rx_dropped, stat.tx_dropped,
                          stat.rx_errors, stat.tx_errors,
                          stat.rx_frame_err, stat.rx_over_err,
                          stat.rx_crc_err, stat.collisions,
                          stat.duration_sec, stat.duration_nsec))

        # self.logger.info('datapath         port     '
        #                  'rx-pkts  rx-bytes rx-error '
        #                  'tx-pkts  tx-bytes tx-error')
        # self.logger.info('---------------- -------- '
        #                  '-------- -------- -------- '
        #                  '-------- -------- --------')
        # for stat in sorted(body, key=attrgetter('port_no')):
        #     self.logger.info('%016x %8x %8d %8d %8d %8d %8d %8d',
        #                      ev.msg.datapath.id, stat.port_no,
        #                      stat.rx_packets, stat.rx_bytes, stat.rx_errors,
        #                      stat.tx_packets, stat.tx_bytes, stat.tx_errors)

        
        # @set_ev_cls(ofp_event.EventOFPGroupStatsReply, MAIN_DISPATCHER)
        # def Group_stats_reply_handler(self, ev):

        #   groups = []
        #   for stat in ev.msg.body:
        #       groups.append('length=%d group_id=%d '
        #                     'ref_count=%d packet_count=%d byte_count=%d '
        #                     'duration_sec=%d duration_nsec=%d' %
        #                     (stat.length, stat.group_id,
        #                      stat.ref_count, stat.packet_count,
        #                      stat.byte_count, stat.duration_sec,
        #                      stat.duration_nsec))

        #   print('this is group event', groups)


