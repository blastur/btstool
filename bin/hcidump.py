#!/usr/bin/python
''' Extract all HCI commands from BTS file and store in wireshark dump format '''
import binascii
import sys
import json
import bts.decode as bts
from bts import *
import struct

# 1002 = HCI UART (H4), 1003 = HCI BSCP, 1004 = HCI Serial (H5)
DATALINK_TYPE = 1002

def die(errmsg):
	sys.stderr.write("%s\n" % errmsg)
	sys.exit(1)

def btsnoop_record(data, sent, tstamp):
	hcidata = binascii.unhexlify(data)
	datalen = len(hcidata)
	if sent:
		flags = 0 # bit 0 is sent/recv, bit 1 is command/event
	else:
		flags = 1
	packetloss = 0 # no packet loss
	return struct.pack('>IIIIQ', datalen, datalen, flags, packetloss, tstamp) + hcidata


def hci_dump(data):
	script = bts.decode_bts(data)
	if script['magic'] != bts.HEADER_MAGIC:
		die("bad magic %d" % script['magic'])

	# btsnoop header
	# http://www.fte.com/webhelp/SD/Content/Technical_Information/BT_Snoop_File_Format.htm
	dump = struct.pack('>8sII', "\x62\x74\x73\x6e\x6f\x6f\x70\x00".encode(), 1,
		DATALINK_TYPE)
	tstamp = 0
	for action in script['actions']:
		if action['type'] == ACTION_SEND_COMMAND:
			dump += btsnoop_record(action['properties']['data'], True, tstamp)
			tstamp = tstamp + 1
		elif action['type'] == ACTION_WAIT_EVENT:
			dump += btsnoop_record(action['properties']['wait_data'], False, tstamp)
			tstamp = tstamp + 1

	sys.stdout.buffer.write(dump)

if __name__ == '__main__':
	if len(sys.argv) != 2:
		die('usage: %s <bts-file>' % sys.argv[0])
	with open(sys.argv[1], "rb") as f:
		hci_dump(f.read())
