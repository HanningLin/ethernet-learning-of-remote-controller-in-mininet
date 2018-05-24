# This code is for project #3 of CSCI-4211
# Group K
# Hanning Lin
# Student ID: 5454150
# X.500 ID: lin00116
# Zijing Mo
# Student ID: 50758101
# X.500 ID: moxxx069

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpid_to_str

# Even a simple usage of the logger is much nicer than print!


# PROJ3 Define your data structures here
log = core.getLogger()
port_table={}
#switch_table={}


# Handle messages the switch has sent us because it has no
# matching rule.

def _handle_PacketIn (event):
  # PROJ3 Your logic goes here
  packet=event.parsed
  src_mac=packet.src
  dst_mac=packet.dst
  switch_id=dpid_to_str(event.connection.dpid)
  #
  port_table[str(src_mac)+switch_id]=event.port
  # switch_table[src_mac]=#switch number!!!#need to add switch number in dictionary
  if str(dst_mac)+switch_id not in port_table:
      log.warning("Destination not in table,flood")
      flood(event,"%s is not associated with a port"%(dst_mac,))
  else:
      port=port_table[str(dst_mac)+switch_id]
      if port==event.port:
          log.warning("Destination is the Source")
          return
      else:
          log.warning("Unicast, port is {}".format(port))
          msg=of.ofp_flow_mod()
          msg.match=of.ofp_match()
          msg.match.dl_src=src_mac
          msg.match.dl_dst=dst_mac
          msg.actions.append(of.ofp_action_output(port=port))
          msg.data=event.ofp
          event.connection.send(msg)

def flood(event,message=None):
    if message is not None:
        log.warning(message)
    msg=of.ofp_packet_out()
    msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
    msg.data=event.ofp
    msg.in_port=event.port
    event.connection.send(msg)
# def _handle_ConnectionUp(event):
#   log.debug("Connection %s" %(event.Connection,))

def launch ():#this is the main actually
  core.openflow.addListenerByName("PacketIn", _handle_PacketIn)#listenner, go to _handle_PacketIn (event)
  # core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)#listen to ConnectionUp
  log.info("Pair-Learning switch running.")
