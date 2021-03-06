import struct

HCI_COMMAND_PACKET = 0x1

ACTION_SEND_COMMAND = 1
ACTION_WAIT_EVENT = 2
ACTION_SERIAL = 3
ACTION_DELAY = 4
ACTION_RUN_SCRIPT = 5
ACTION_REMARKS = 6

HEADER_MAGIC = 0x42535442

BTS_HDR_FMT = '<II24s'
BTS_HDR_SIZE = struct.calcsize(BTS_HDR_FMT)

ACTION_HDR_FMT = '<HH'
ACTION_HDR_SIZE = struct.calcsize(ACTION_HDR_FMT)

WAIT_EVENT_HDR_FMT = '<II'
WAIT_EVENT_HDR_SIZE = struct.calcsize(WAIT_EVENT_HDR_FMT)

SERIAL_HDR_FMT = '<II'
SERIAL_HDR_SIZE = struct.calcsize(SERIAL_HDR_FMT)

DELAY_HDR_FMT = '<I'
DELAY_HDR_SIZE = struct.calcsize(DELAY_HDR_FMT)
