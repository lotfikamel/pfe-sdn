import threading

class ThreadOne (threading.Thread) :

	def __init__ (self) :

		threading.Thread.__init__(self)

	def run (self) :

		print('1')

t1 = ThreadOne()

t2 = ThreadOne()

t1.start()

t2.start()