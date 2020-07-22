from threading import Thread

import subprocess

class CmdAsync (Thread) :

	def __init__ (self, cmd) :

		Thread.__init__(self)

		self.cmd = cmd

	def run (self) :

		print('starting monitor server')

		self.run_cmd_async()

	def run_cmd_async (self) :

		subprocess.Popen(self.cmd)