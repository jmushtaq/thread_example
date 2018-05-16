import sys
import Queue
import threading
from datetime import datetime
import time

TS_FORMAT = '%Y-%m-%dT%H:%M:%S'
STREAM_TO_QUEUE_HEARTBEAT = 0 # seconds
CONTROLLER_HEARTBEAT = 0 # seconds

PRIORITY_LOW = 5
PRIORITY_MEDIUM = 10
PRIORITY_HIGH = 15
PRIORITY_QUIT = 999

# Create a Dummy map of events
DUMMY_EVENTS_MAP = [
	dict(event_type='TYPE_1', priority=PRIORITY_LOW),
	dict(event_type='TYPE_1', priority=PRIORITY_LOW),
	dict(event_type='TYPE_3', priority=PRIORITY_HIGH),
	dict(event_type='TYPE_2', priority=PRIORITY_MEDIUM),
	dict(event_type='TYPE_3', priority=PRIORITY_HIGH),
	dict(event_type='TYPE_1', priority=PRIORITY_LOW),
	dict(event_type='QUIT', priority=PRIORITY_QUIT),
]


class Event():
	def __init__(self, type, timestamp, priority='LOW'):
		self.type = type
		self.timestamp = timestamp
		self.priority = priority

	def __str__(self):
		return '{} - {} - {}'.format(self.type, self.priority, self.timestamp)


class Engine():

	def __init__(self, type, events_queue):
		self.type = type
		self.events_queue = events_queue

	def stream_to_queue(self):
		while True:
			try:
				self.send_event()
				time.sleep(STREAM_TO_QUEUE_HEARTBEAT)

			except IndexError:
				break

	def send_event(self):
		dummy_event_map = DUMMY_EVENTS_MAP.pop(0)

		event_type = dummy_event_map['event_type']
		priority = dummy_event_map['priority']
		timestamp = datetime.now().strftime(TS_FORMAT)

		ev = Event(event_type, timestamp, priority)
		self.events_queue.put((priority, ev))


class PidController():
	""" to run:
			python pid_controller.py
	"""
	def __init__(self, number_of_threads):
		self.number_of_threads = number_of_threads

	def run(self):
		#events = Queue.Queue()
		events = Queue.PriorityQueue()

		for thread_id in range(1, self.number_of_threads+1):
			engine_thread = threading.Thread(
				target=Engine('Engine_' + str(thread_id), events).stream_to_queue,
				args=[]
			)
			engine_thread.start()

		controller_thread = threading.Thread(
			target=self.listener,
			args=[events]
		)
		controller_thread.start()


	def listener(self, events):
		"""
		Carries out an infinite while loop that polls the
		events queue and directs each event to either the
		action method.

		The loop will then pause for "heartbeat" seconds and
		continue.
		"""

		count = 0
		while True:
			#import ipdb; ipdb.set_trace()
			try:
				event = events.get(False)[1] # first element id the priority, second element is the data (event object)
			except Queue.Empty:
				pass
			else:
				if event is not None:
					#import ipdb; ipdb.set_trace()
					if event.type == 'TYPE_1':
						# respond to 'TYPE 1 event' ...
						print('EVENT TYPE 1: Received event {}'.format(event))

					elif event.type == 'TYPE_2':
						# respond to 'TYPE 2 event' ...
						print('EVENT TYPE 2: Received event {}'.format(event))

					elif event.type == 'TYPE_3':
						# respond to 'TYPE 3 event' ...
						print('EVENT TYPE 3: Received event {}'.format(event))

					elif event.type == 'QUIT':
						#import ipdb; ipdb.set_trace()
						print '*************************** END ******************************'
						sys.exit()

			time.sleep(CONTROLLER_HEARTBEAT)



if __name__ == '__main__':
	if len(sys.argv) == 1:
		print('Usage: python pid_controller.py <num_threads>'.format())
		sys.exit()

	number_of_threads = int(sys.argv[1])
	PidController(number_of_threads).run()

