import binascii
import struct
from bts import *

def decode_wait_event(data):
	(msec, size) = struct.unpack(WAIT_EVENT_HDR_FMT, data[:WAIT_EVENT_HDR_SIZE])
	wait_data = data[WAIT_EVENT_HDR_SIZE:].hex()
	return {'msec': msec, 'size': size, 'wait_data': wait_data}


def decode_serial(data):
	(baud, flow) = struct.unpack(SERIAL_HDR_FMT, data)
	return {'baudrate': baud, 'flowcontrol': flow}


def decode_delay(data):
	(msec, ) = struct.unpack(DELAY_HDR_FMT, data)
	return {'msec': msec}

def decode_run_script(data):
	return {'data': data.hex()}

def decode_remarks(data):
	''' The data is a null-terminated string '''
	return {'data': data.decode("ascii")}

def decode_unknown(data):
	return {'data': data.hex()}

def decode_send_cmd(data):
	return {"data": data.hex()}

action_dict = {
	ACTION_SEND_COMMAND: {
		'title': 'Send command',
		'decode': decode_send_cmd
	},
	ACTION_WAIT_EVENT: {
		'title': 'Wait event',
		'decode': decode_wait_event,
	},
	ACTION_SERIAL: {
		'title': 'Serial',
		'decode': decode_serial,
	},
	ACTION_DELAY: {
		'title': 'Delay',
		'deocde': decode_delay,
	},
	ACTION_RUN_SCRIPT: {
		'title': 'Run script',
		'decode': decode_run_script,
	},
	ACTION_REMARKS: {
		'title': 'Remarks',
		'decode': decode_remarks,
	}
}

def decode_action(atype, adata):
	if atype in action_dict:
		atypestr = action_dict[atype]['title']
		decoder = action_dict[atype]['decode']
	else:
		atypestr = "Unknown"
		decoder = decode_unknown

	return {'type': atype, 'name': atypestr, 'properties': decoder(adata)}

def decode_all_actions(data):
	actions = []
	while data:
		(action_type, action_size) = struct.unpack(ACTION_HDR_FMT, data[:ACTION_HDR_SIZE])
		data = data[ACTION_HDR_SIZE:]
		action_data = data[:action_size]
		data = data[action_size:]
		actions.append(decode_action(action_type, action_data))

	return actions

def decode_bts(data):
	(magic, version, future) = struct.unpack(BTS_HDR_FMT, data[:BTS_HDR_SIZE])

	data = data[BTS_HDR_SIZE:]
	actions = decode_all_actions(data)

	return {
		'magic': magic,
		'version': version,
		'future': future.hex(),
		'actions': actions
	}
