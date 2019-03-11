#!/usr/bin/python
''' Translate BTS into human-readable JSON file '''
import sys
import json
import bts.decode as bts
import binascii
from bts import *

ti_opcodes = {
	0xFC06: 'HCI_VS_Write_BD_Addr',
	0xFD04: 'HCI_VS_Set_PCM_Loopback_Configuration',
	0xFD06: 'HCI_VS_Write_CODEC_Config',
	0xFD07: 'HCI_VS_Write_CODEC_Config_Enhanced',
	0xFD09: 'HCI_VS_Read_Modify_Write_Hardware_Register',
	0xFD0C: 'HCI_VS_Sleep_Mode_Configurations',
	0xFD0C: 'HCI_VS_Sleep_Mode_Configurations',
	0xFD13: 'HCI_VS_DRP_Read_BER_Meter_Result',
	0xFD17: 'HCI_VS_DRPb_Tester_Con_RX',
	0xFD1C: 'HCI_VS_Fast_Clock_Configuration_btip',
	0xFD2B: 'HCI_VS_HCILL_Parameters',
	0xFD55: 'HCI_VS_Configure_DDIP',
	0xFD5B: 'HCI_VS_LE_Enable',
	0xFD77: 'HCI_VS_Set_LE_Test_Mode_Parameters',
	0xFD78: 'HCI_VS_WBS_Associate',
	0xFD79: 'HCI_VS_WBS_Disassociate',
	0xFD80: 'HCI_VS_DRPb_Enable_RF_Calibration',
	0xFD82: 'HCI_VS_DRPb_Set_Power_Vector',
	0xFD84: 'HCI_VS_DRPb_Tester_Con_T',
	0xFD85: 'HCI_VS_DRPb_Tester_Packet_TX_RX',
	0xFD87: 'HCI_VS_DRPb_Set_Class2_Single_Power',
	0xFD88: 'HCI_VS_DRPb_Reset',
	0xFD8B: 'HCI_VS_DRPb_BER_Meter_Start',
	0xFD8C: 'HCI_VS_A3DP_Open_Stream',
	0xFD8D: 'HCI_VS_A3DP_Close_Stream',
	0xFD8E: 'HCI_VS_A3DP_Codec_Configuration',
	0xFD8F: 'HCI_VS_A3DP_Start_Stream',
	0xFD90: 'HCI_VS_A3DP_Stop_Stream',
	0xFD92: 'HCI_VS_AVPR_Enable',
	0xFD9A: 'HCI_VS_A3DP_Sink_Open_Stream',
	0xFD9B: 'HCI_VS_A3DP_Sink_Close_Stream',
	0xFD9C: 'HCI_VS_A3DP_Sink_Codec_Configuration',
	0xFD9D: 'HCI_VS_A3DP_Sink_Start_Stream',
	0xFD9E: 'HCI_VS_A3DP_Sink_Stop_Stream',
	0xFDCA: 'HCI_VS_DRPb_Tester_Con_TX',
	0xFDCB: 'HCI_VS_DRPb_Tester_Con_RX',
	0xFDCC: 'HCI_VS_DRPb_Tester_Packet_TX_RX',
	0xFDDD: 'HCI_VS_LE_Output_Power',
	0xFDFB: 'HCI_VS_DRPb_Enable_RF_Calibration_Enhanced',
	0xFDFC: 'HCI_VS_Read_RSSI',
	0xFE0E: 'HCI_VS_Write_I2C_Register',
	0xFE10: 'HCI_VS_Write_SCO_Configuration',
	0xFE1F: 'HCI_VS_Get_System_Status',
	0xFE24: 'HCI_VS_Clock_Set_Timeout',
	0xFE28: 'HCI_VS_Set_PCM_Loopback_Enable',
	0xFE37: 'HCI_VS_Start_VS_Lock',
	0xFE38: 'HCI_VS_Stop_VS_Lock',
	0xFE49: 'HCI_VS_Start_AVPR_VS_Lock',
	0xFF00: 'HCI_VS_Read_Hardware_Register',
	0xFF01: 'HCI_VS_Write_Hardware_Register',
	0xFF02: 'HCI_VS_Read_Memory',
	0xFF03: 'HCI_VS_Write_Memory',
	0xFF04: 'HCI_VS_Read_Memory_Block',
	0xFF05: 'HCI_VS_Write_Memory_Block',
	0xFF22: 'HCI_VS_Read_Patch_Version',
	0xFF26: 'HCI_VS_Set_Supported_Features',
	0xFF36: 'HCI_VS_Update_UART_HCI_Baudrate',
}

def die(errmsg):
	sys.stderr.write("%s\n" % errmsg)
	sys.exit(1)

def add_ti_opcodes(action):
	# Try decoding TI-specific HCI commands. Based on list of WiLink 8 opcodes:
	# http://www.ti.com/lit/ug/swru442a/swru442a.pdf
	if action['type'] == ACTION_SEND_COMMAND:
		data = binascii.unhexlify(action['properties']['data'])

		if data[0] == HCI_COMMAND_PACKET and len(data) >= 4:
			(opcode, ) = struct.unpack("<H", data[1:3])
			param_len = data[3]
			params = data[4:]
			if (param_len != len(params)):
				sys.stderr.write('warning: hci command packet with opcode 0x%x contains %d bytes (header specified %d bytes)\n' % (opcode, len(params), param_len))

			if opcode in ti_opcodes:
				action['properties']['ti_opcode'] = ti_opcodes[opcode]
			else:
				action['properties']['ti_opcode'] = "0x%x" % opcode
			action['properties']['ti_opcode_param'] = params.hex()

	return action


def bts_dump(data):
	script = bts.decode_bts(data)
	if script['magic'] != bts.HEADER_MAGIC:
		die("bad magic %d" % script['magic'])

	script['actions'] = [add_ti_opcodes(action) for action in script['actions']]
	return script


if __name__ == '__main__':
	if len(sys.argv) != 2:
		die('usage: %s <bts-file>' % sys.argv[0])
	with open(sys.argv[1], "rb") as f:
		script = bts_dump(f.read())
		print((json.dumps(script, indent=4, separators=(',', ': '))))
