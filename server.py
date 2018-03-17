import zmq
from multiprocessing import Process, Value
import time


def worker_routine(counter):
	# context = zmq.Context.instance()
	# socket = context.socket(zmq.REP)
	# socket.connect(worker_url)
		
	while True:
		counter.value += 1
		time.sleep(1)
		print "tick: {}".format(counter.value)

def main():
	""" server """
	client_url = "tcp://127.0.0.1:5555"

	context = zmq.Context.instance()

	client_socket = context.socket(zmq.REP)
	client_socket.bind(client_url)

	counter = Value('i', 0, lock=False)
	p = Process(target=worker_routine, args=([counter]))
	p.start()
	
	try:
		while True:
			message = client_socket.recv().upper()
			print "got message: " + message
			if message == "OFF":
				client_socket.send("TURN_OFF")
			elif message == "COUNT":
				client_socket.send("Count: {}".format(counter.value))
			else:
				client_socket.send("ECHO: " + message)
	except KeyboardInterrupt:
		print "closing"
		p.terminate()
		client_socket.close()
		context.term()

main()
