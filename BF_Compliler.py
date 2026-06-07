
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




from tracemalloc import start
# Standard libraries
import numpy as np
import os
import sys
import argparse
import keyboard
import time
# Progress bars and terminal rendering
from tqdm import tqdm
from alive_progress import *
# Rich for terminal rendering
from rich.console import Console
from rich.live import Live
from rich.layout import Layout
from rich.panel import Panel
# Bangen for rendering the banner
from bangen.rendering import RenderEngine
from bangen.gradients import Gradient, ColorStop
from bangen.effects import *
# Colorama for colored terminal output
import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

parser = argparse.ArgumentParser("BF Compiler")
parser.add_argument("file", nargs="?", help="The path to the file that will be compiled", type=str, default="ZGVmYXVsdA==")
args = parser.parse_args()

ending = ".bf"

def get_file():
	if str(args.file) == "ZGVmYXVsdA==":
		for dl in os.listdir():
			if ending in dl:
				return dl
	else:
		if ending in args.file:
			return args.file
		else:
			print("No file found")


def remove_comments(code):
	operators = ['>', '<', '+', '-', '[', ']', ',', '.']
	return ''.join([c for c in code if c in operators])

def read_code(file):
	try:
		with open(file, 'r') as f:
			code = f.read()
		return remove_comments(code)
	except (TypeError, FileNotFoundError):
		return "Fore.RED + Error: File not found or invalid file type. Please provide a valid .bf file."

def banner(file):
	global layout, console, start, banner
	engine = RenderEngine()
	banner = engine.render("BF Compiler", font="slant")
	gradient_stops = [
		ColorStop(0.0, "#00ffff"),
		ColorStop(0.5, "#ff00ff"),
		ColorStop(1.0, "#ffff00"),
	]
	banner.set_gradient(Gradient(stops=gradient_stops, direction="horizontal"))
	banner.apply(FlickerEffect()).apply(ScanlineEffect()).apply(GlitchEffect()).apply(NoiseInjectionEffect())

	layout = Layout()
	layout.split_column(
		Layout(name="banner", ratio=4),
		Layout(name="info", ratio=2),
	)
	file_display = file if file else "No .bf file found"
	layout["info"].update(Panel(f"File: {file_display}", style="dim cyan"))

	console = Console()
	console.clear()
	start = time.time()
	# with Live(layout, console=console, refresh_per_second=20):
	# 	# while True:
	# 		t = time.time() - start
	# 		# if t >= 3.0:
	# 		# 	break
	# 		layout["banner"].update(banner.render_frame(t))
	# 		#time.sleep(1 / 20)

file = get_file()
banner(file)

running = True
with Live(layout, console=console, refresh_per_second=20):
	while running:
		if keyboard.is_pressed('esc'):
			print("Exiting...")
			running = False
		t = time.time() - start
		layout["banner"].update(banner.render_frame(t))
