#!/usr/bin/python
''' Compares 2 JSON dumps of BTS files '''
import sys
import json
import bts.decode as bts
import binascii
from bts import *
import argparse
import tempfile
import subprocess
import os

def die(errmsg):
	sys.stderr.write("%s\n" % errmsg)
	sys.exit(1)

def bts_diff(data1, data2, ignore_remarks, group_send_wait, diff_tool):
	script1 = json.loads(data1)
	script2 = json.loads(data2)

	if ignore_remarks:
		script1['actions'] = [action for action in script1['actions'] if action['type'] != ACTION_REMARKS]
		script2['actions'] = [action for action in script2['actions'] if action['type'] != ACTION_REMARKS]

	if group_send_wait:
		die('send/wait grouping is not not implemented')

	(fd1, path1) = tempfile.mkstemp()
	os.write(fd1, (json.dumps(script1['actions'], indent=4, separators=(',', ': '))).encode())
	os.close(fd1)

	(fd2, path2) = tempfile.mkstemp()
	os.write(fd2, (json.dumps(script2['actions'], indent=4, separators=(',', ': '))).encode())
	os.close(fd2)

	diff_args = diff_tool.split(" ") + [path1, path2]
	subprocess.run(diff_args)

	os.unlink(path1)
	os.unlink(path2)


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Compare two BTS JSON dumps')
	parser.add_argument('file', help="JSON files to compare", nargs=2)
	parser.add_argument('--no-remarks', action='store_true', default=False,
						help='Ignore remarks in comparison')
	parser.add_argument('--diff-tool', default='/usr/bin/diff -u',
						help='Diff tool (must accept 2 files)')
	parser.add_argument('--group-send-wait', action='store_true', default=False,
						help='Group pairs of send command & wait event')

	args = parser.parse_args()
	with open(args.file[0], "r") as f1:
		with open(args.file[1], "r") as f2:
			bts_diff(f1.read(), f2.read(), args.no_remarks,
					 args.group_send_wait, args.diff_tool)
