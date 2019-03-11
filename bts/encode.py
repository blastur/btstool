import binascii
import struct
from bts import *

def encode_wait_event(properties):
	hdr = struct.pack(WAIT_EVENT_HDR_FMT, properties['msec'], properties['size'])
	return hdr + binascii.unhexlify(properties['wait_data'])

def encode_serial(properties):
	return struct.pack(SERIAL_HDR_FMT, properties['baudrate'], properties['flowcontrol'])

def encode_delay(properties):
	return struct.pack(DELAY_HDR_FMT, properties['msec'])

def encode_run_script(properties):
	return binascii.unhexlify(properties['data'])

def encode_remarks(properties):
	''' The data is a null-terminated string '''
	return properties['data'].encode()

def encode_unknown(properties):
	return binascii.unhexlify(properties['data'])

def encode_send_cmd(properties):
	return binascii.unhexlify(properties['data'])

action_dict = {
	ACTION_SEND_COMMAND: {
		'title': 'Send command',
		'encode': encode_send_cmd
	},
	ACTION_WAIT_EVENT: {
		'title': 'Wait event',
		'encode': encode_wait_event,
	},
	ACTION_SERIAL: {
		'title': 'Serial',
		'encode': encode_serial,
	},
	ACTION_DELAY: {
		'title': 'Delay',
		'encode': encode_delay,
	},
	ACTION_RUN_SCRIPT: {
		'title': 'Run script',
		'encode': encode_run_script,
	},
	ACTION_REMARKS: {
		'title': 'Remarks',
		'encode': encode_remarks,
	}
}

def encode_action(action):
	if action['type'] not in action_dict:
		die('Unknown action type %d, cannot encode' % action['type'])

	encoder = action_dict[action['type']]['encode']
	data = encoder(action['properties'])
	hdr = struct.pack(ACTION_HDR_FMT, action['type'], len(data))
	return hdr + data

def encode_all_actions(actions):
	all_encoded = b''
	for action in actions:
		all_encoded += encode_action(action)

	return all_encoded

def encode_bts(script):
	hdr = struct.pack(BTS_HDR_FMT, script['magic'], script['version'], binascii.unhexlify(script['future']))
	return hdr + encode_all_actions(script['actions'])
