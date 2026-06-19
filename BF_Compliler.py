
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


# DONE: fix layout proportions
# TODO: make the file_display show file name
# TODO: simplify imports
# TODO: add in loops
# TODO: add in user input and output
# TODO: fix cloned display above in cmd
# TODO: fix updating flashing issue

from ast import JoinedStr
from tracemalloc import start
# Standard libraries
import alive_progress
import numpy as np
import os
import sys
import argparse
import keyboard
import time
# Progress bars and terminal rendering
from alive_progress import *
# Rich for terminal rendering
from rich import panel
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

memory_tape = np.zeros(1)
tape_position = 0

compiled = False

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
		Layout(name="banner", ratio=3),
		Layout(name="info", ratio=7),
	)

	file_display = "Found .bf file. Compilling..." if file else "No .bf file found"

	console = Console()
	console.clear()
	start = time.time()
	with Live(layout, console=console, refresh_per_second=20):
		with alive_bar(len(read_code(file)) * 1, disable=True, ) as bar:
			for _ in range(len(read_code(file)) * 1):
				t = time.time() - start
				# if t >= 3.0:
				#  	break

				layout["banner"].update(banner.render_frame(t))
				bar()
				visual_compiler_bar = bar.receipt()
				layout["info"].update(Panel(f"{file_display}\n{visual_compiler_bar}", style="dim cyan"))
				time.sleep(1 / 20)

def compile_file(file_contents, memory_tape, tape_position, position):
	# TODO: add back the bar
	with alive_bar(len(file_contents), disable=True, length=33) as bar:
		for char in file_contents:
			if char == "+":
				memory_tape[tape_position] += 1
			if char == "-":
				if memory_tape[tape_position] - 1 >= 0:
					memory_tape[tape_position] -= 1
			if char == "<":
				if tape_position - 1 >= 0:
					tape_position -= 1
			if char == ">":
				try:
					memory_tape[tape_position+1]
				except:
					# TODO: if possible make this line simpler
					memory_tape = np.append(memory_tape, 0)
				tape_position += 1
			if char == ",":
				tape_position += 0
			if char == ".":
				tape_position += 0
			#memory_tape_display(memory_tape, tape_position)
			#file_contents_display(file_contents, position)
			update_banner_visual()
			bar()
			layout["info"].update(Panel(f"\n" + memory_tape_display(memory_tape, tape_position) + file_contents_display(file_contents, position) + f"\n" + bar.receipt(), style="dim cyan"))
			position += 1
			time.sleep(2/len(file_contents))

def memory_tape_display(memory_tape, tape_position):
	arrow_display_tape = " "
	for i in range(tape_position):
		arrow_display_tape = "".join([arrow_display_tape, "   "])
	arrow_display_tape = "".join([arrow_display_tape, "^"])
	#layout["info"].update(Panel(f"{memory_tape}\n{arrow_display_tape}", style="dim cyan"))
	return f" {memory_tape}\n {arrow_display_tape}"

def file_contents_display(file_contents, position):
	arrow_display_content = ""
	for i in range(position):
		arrow_display_content = "".join([arrow_display_content, " "])
	arrow_display_content = "".join([arrow_display_content, "^"])
	#layout["info"].update(Panel(f"\n\n{file_contents}\n{arrow_display_content}", style="dim cyan"))
	return f"\n {file_contents}\n {arrow_display_content}"

def update_banner_visual():
	for i in range(1):
		t = time.time() - start
		layout["banner"].update(banner.render_frame(t))


file = get_file()
banner(file)

running = True
with Live(layout, console=console, refresh_per_second=20):
	while running:
		if keyboard.is_pressed('esc'):
			print("Exiting...")
			running = False
		update_banner_visual()
		#t = time.time() - start
		#layout["banner"].update(banner.render_frame(t))
		# file_contents = read_code(file)
		# for c in range(len(file_contents)):
		# 	layout["info"].update(Panel(f"{c}", style="dim cyan"))
		# 	time.sleep(0.2)
		if not compiled:
			compile_file(read_code(file), memory_tape, tape_position, 0)
			compiled = True
