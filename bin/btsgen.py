#!/usr/bin/python
''' Translate human-readable JSON file into BTS file '''
import struct
import sys
import json
import binascii
import bts.encode as bts

def die(errmsg):
	sys.stderr.write("%s\n" % errmsg)
	sys.exit(1)

def bts_gen(data):
	script = json.loads(data)
	sys.stdout.buffer.write(bts.encode_bts(script))

if __name__ == '__main__':
	if len(sys.argv) != 2:
		die('usage: %s <json-file>' % sys.argv[0])
	with open(sys.argv[1], "r") as f:
		bts_gen(f.read())
