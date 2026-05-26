
# ---------------- NOTES ----------------
# https://gist.github.com/roachhd/dce54bec8ba55fb17d3a
# > = increases memory pointer, or moves the pointer to the right 1 block.
# < = decreases memory pointer, or moves the pointer to the left 1 block.
# + = increases value stored at the block pointed to by the memory pointer
# - = decreases value stored at the block pointed to by the memory pointer
# [ = like c while(cur_block_value != 0) loop.
# ] = if block currently pointed to's value is not zero, jump back to [
# , = like c getchar(). input 1 character.
# . = like c putchar(). print 1 character to the console
#
# chr() = From ASCII value to char
# ord() = Opposite from chr
#
# ---------------- RULES ----------------
# Any arbitrary character besides the 8 listed above should be ignored by the compiler or interpretor. Characters besides the 8 operators should be considered comments.
#
# All memory blocks on the "array" are set to zero at the beginning of the program. And the memory pointer starts out on the very left most memory block.
#
# Loops may be nested as many times as you want. But all [ must have a corresponding ].




import numpy as np
import os
import sys
import argparse
import pyfiglet

parser = argparse.ArgumentParser("BF Compiler")
parser.add_argument("file", nargs="?", help="The path to the file that will be compiled", type=str, default="ZGVmYXVsdA==")
args = parser.parse_args()

ending = ".bf"

def get_file():
	if str(args.file) == "ZGVmYXVsdA==":
		for dl in os.listdir():
			if ending in dl:
				print(args.file)
	else:
		if ending in args.file:
			print(args.file)

get_file()
