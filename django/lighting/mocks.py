import socket
import threading

from pjlink import PJLinkCommandLine, PJLinkResponse, PJLinkAuthenticationRequest, PJLinkAuthenticationException, PJLinkProtocol, PJLinkController


class MockPJLinkProjector(threading.Thread):
	"""This creates a localhost server socket which speaks the PJLink protocol as if it were a projector"""
	def __init__(self):
		self.backlog = 5
		self.buffer_size = 1024
		self.server = None
		self.running = False

		self.port = 0 # 0 indicates that the server should use any open socket

		self.projector_name = "The Projector in the Blue Room"
		self.manufacture_name = "2038 Problems, Inc."
		self.product_name = "Big Bad Projector 1900"
		self.other_info = "This Thing Rocks (tm)"
		self.class_info = "1"

		self.password = 'squarePusher' # or None if the projector should use no auth

		self.power_state = PJLinkProtocol.POWER_OFF_STATUS
		self.input = [PJLinkProtocol.RGB_INPUT, PJLinkProtocol.INPUT_1]
		self.available_inputs = [[PJLinkProtocol.RGB_INPUT, PJLinkProtocol.INPUT_1], [PJLinkProtocol.VIDEO_INPUT, PJLinkProtocol.INPUT_2]]
		self.audio_mute = False
		self.video_mute = False

		self.errors = [['fan', PJLinkProtocol.ERROR_STATUS_OK], ['lamp', PJLinkProtocol.ERROR_STATUS_OK], ['filter', PJLinkProtocol.ERROR_STATUS_OK], ['cover', PJLinkProtocol.ERROR_STATUS_OK], ['other', PJLinkProtocol.ERROR_STATUS_OK]]

		# an array of arrays [[lighting time, lamp is on], ...]
		self.lamps = [[100, False], [500, False], [0, False]]

		threading.Thread.__init__(self)

	def _set_mute_state(self, state):
		if state == PJLinkProtocol.AUDIO_VIDEO_MUTE_ON:
			self.audio_mute = True
			self.video_mute = True
		elif state == PJLinkProtocol.AUDIO_MUTE_ON:
			self.audio_mute = True
		elif state == PJLinkProtocol.VIDEO_MUTE_ON:
			self.video_mute = True
		elif state == PJLinkProtocol.AUDIO_MUTE_OFF:
			self.audio_mute = False
		elif state == PJLinkProtocol.VIDEO_MUTE_OFF:
			self.video_mute = False
		elif state == PJLinkProtocol.AUDIO_VIDEO_MUTE_OFF:
			self.audio_mute = False
			self.video_mute = False
		else:
			return False
		return True

	def _get_mute_state(self):
		if self.audio_mute and self.video_mute:
			return PJLinkProtocol.AUDIO_VIDEO_MUTE_ON
		elif self.audio_mute:
			return PJLinkProtocol.AUDIO_MUTE_ON
		elif self.video_mute:
			return PJLinkProtocol.VIDEO_MUTE_ON
		else:
			return PJLinkProtocol.AUDIO_VIDEO_MUTE_OFF

	mute_state = property(_get_mute_state, _set_mute_state)

	def stop_server(self):
		self.running = False
		if self.server: self.server.close()

	def run(self):
		if self.running: return
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.bind(('127.0.0.1',self.port))
		self.server.listen(self.backlog)
		self.running = True
		while self.running:
			client, address = self.server.accept()
			auth_request = PJLinkAuthenticationRequest(self.password)
			client.send(auth_request.encode())
			data = client.recv(self.buffer_size)
			if not data:
				client.close()
				continue

			response = None
			command_line = PJLinkCommandLine.decode(data)

			if not auth_request.authentication_hash_matches(command_line.authentication_hash):
				response = PJLinkResponse(PJLinkProtocol.AUTHENTICATE, PJLinkProtocol.INVALID_PASSWORD_ERROR, version=None)
				client.send(response.encode())
				client.close()
				continue

			if command_line.command == PJLinkProtocol.POWER:
				if command_line.data == PJLinkProtocol.ON or command_line.data == PJLinkProtocol.OFF:
					self.power_state = command_line.data
					for lamp in self.lamps: lamp[1] = command_line.data == PJLinkProtocol.ON
					response = PJLinkResponse(PJLinkProtocol.POWER, PJLinkProtocol.OK)
				elif command_line.data == PJLinkProtocol.QUERY:
					response = PJLinkResponse(PJLinkProtocol.POWER, self.power_state)
				else:
					response = PJLinkResponse(command_line.command, PJLinkProtocol.ERROR_2)

			elif command_line.command == PJLinkProtocol.INPUT:
				if command_line.data == PJLinkProtocol.QUERY:
					response = PJLinkResponse(command_line.command, '%s%s' % (self.input[0], self.input[1]))
				elif len(command_line.data) == 2:
					self.input = [command_line.data[0], command_line.data[1]]
					response = PJLinkResponse(command_line.command, PJLinkProtocol.OK)
				else:
					response = PJLinkResponse(command_line.commands, PJLinkProtocol.ERROR_2)

			elif command_line.command == PJLinkProtocol.AVAILABLE_INPUTS:
				if command_line.data == PJLinkProtocol.QUERY:
					data = ' '.join(['%s%s' % (input[0], input[1]) for input in self.available_inputs])
					response = PJLinkResponse(command_line.command, data)
				else:
					response = PJLinkResponse(command_line.commands, PJLinkProtocol.ERROR_2)

			elif command_line.command == PJLinkProtocol.MUTE:
				if command_line.data == PJLinkProtocol.QUERY:
					response = PJLinkResponse(command_line.command, self.mute_state)
				elif command_line.data == PJLinkProtocol.AUDIO_VIDEO_MUTE_ON or command_line.data == PJLinkProtocol.AUDIO_VIDEO_MUTE_OFF or command_line.data == PJLinkProtocol.VIDEO_MUTE_ON or command_line.data == PJLinkProtocol.VIDEO_MUTE_OFF or command_line.data == PJLinkProtocol.AUDIO_MUTE_ON or command_line.data == PJLinkProtocol.AUDIO_MUTE_OFF:
					self.mute_state = command_line.data
					response = PJLinkResponse(command_line.command, PJLinkProtocol.OK)
				else:
					response = PJLinkResponse(command_line.command, PJLinkProtocol.ERROR_2)

			elif command_line.command == PJLinkProtocol.NAME:
				if command_line.data == PJLinkProtocol.QUERY:
					response = PJLinkResponse(command_line.command, self.projector_name)
				else:
					response = PJLinkResponse(command_line.command, PJLinkProtocol.ERROR_2)

			elif command_line.command == PJLinkProtocol.MANUFACTURE_NAME:
				if command_line.data == PJLinkProtocol.QUERY:
					response = PJLinkResponse(command_line.command, self.manufacture_name)
				else:
					response = PJLinkResponse(command_line.command, PJLinkProtocol.ERROR_2)

			elif command_line.command == PJLinkProtocol.PRODUCT_NAME:
				if command_line.data == PJLinkProtocol.QUERY:
					response = PJLinkResponse(command_line.command, self.product_name)
				else:
					response = PJLinkResponse(command_line.command, PJLinkProtocol.ERROR_2)

			elif command_line.command == PJLinkProtocol.OTHER_INFO:
				if command_line.data == PJLinkProtocol.QUERY:
					response = PJLinkResponse(command_line.command, self.other_info)
				else:
					response = PJLinkResponse(command_line.command, PJLinkProtocol.ERROR_2)

			elif command_line.command == PJLinkProtocol.CLASS_INFO:
				if command_line.data == PJLinkProtocol.QUERY:
					response = PJLinkResponse(command_line.command, self.class_info)
				else:
					response = PJLinkResponse(command_line.command, PJLinkProtocol.ERROR_2)

			elif command_line.command == PJLinkProtocol.ERROR_STATUS:
				if command_line.data == PJLinkProtocol.QUERY:
					data = ''.join([error[1] for error in self.errors])
					response = PJLinkResponse(command_line.command, data)
				else:
					response = PJLinkResponse(command_line.command, PJLinkProtocol.ERROR_2)

			elif command_line.command == PJLinkProtocol.LAMP:
				if command_line.data == PJLinkProtocol.QUERY:
					data = ' '.join(['%s %s' % (lamp[0], '1' if lamp[1] == True else '0') for lamp in self.lamps])
					response = PJLinkResponse(command_line.command, data)
				else:
					response = PJLinkResponse(command_line.command, PJLinkProtocol.ERROR_2)

			else:
				response = PJLinkResponse(command_line.command, PJLinkProtocol.ERROR_1)

			client.send(response.encode())
			client.close()

		self.server.close()
