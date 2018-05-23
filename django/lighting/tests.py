import time
from django.test import TestCase
from django.test.client import Client

from mocks import MockPJLinkProjector
from lighting.models import *

# system under test
from lighting.pjlink import PJLinkCommandLine, PJLinkResponse, PJLinkAuthenticationException, PJLinkProtocol, PJLinkController


class PJLinkAPITest(TestCase):
	def setUp(self):
		self.client = Client()
		self.projector = MockPJLinkProjector()
		self.projector.start()

	def tearDown(self):
		self.projector.stop_server()

	def test_api_views(self):
		self.failUnlessEqual(len(Projector.objects.all()), 0)
		response = self.client.get('/api/projector/')
		self.failUnlessEqual(response.status_code, 200, 'status was %s' % response.status_code )
		element = etree.fromstring(response.content)
		self.failUnlessEqual(len(element), 0)
		proj_entry = Projector.objects.create(name=self.projector.projector_name, pjlink_host=self.projector.server.getsockname()[0], pjlink_port=self.projector.server.getsockname()[1], pjlink_password=self.projector.password)
		response = self.client.get('/api/projector/')
		self.failUnlessEqual(response.status_code, 200, 'status was %s' % response.status_code )
		element = etree.fromstring(response.content)
		self.failUnlessEqual(len(element), 1)
		proj_element = element[0]
		self.failUnlessEqual(proj_element.tag, 'projector')
		self.failUnlessEqual(proj_element.get('name'), self.projector.projector_name)

		projector_info_url = '/api/projector/%s/info/' % proj_entry.id
		response = self.client.get(projector_info_url)
		self.failUnlessEqual(response.status_code, 200, 'status was %s' % response.status_code)
		info_element = etree.fromstring(response.content)
		self.failUnlessEqual(info_element.get('power_state'), self.projector.power_state)
		self.failUnlessEqual(info_element.get('projector_name'), self.projector.projector_name)
		self.failUnlessEqual(info_element.get('manufacture_name'), self.projector.manufacture_name)
		self.failUnlessEqual(info_element.get('product_name'), self.projector.product_name)
		self.failUnlessEqual(info_element.get('other_info'), self.projector.other_info)
		self.failUnless(len(info_element) > 0)
		lamps_elements = info_element.find('lamps')
		self.failUnlessEqual(len(lamps_elements), len(self.projector.lamps))
		for index, lamp_element in enumerate(lamps_elements):
			self.failUnlessEqual(int(lamp_element.get('lighting_hours')), self.projector.lamps[index][0])
			self.failUnlessEqual(lamp_element.get('is_on'), '%s' % self.projector.lamps[index][1])

		response = self.client.post(projector_info_url, {'power':PJLinkProtocol.POWER_ON_STATUS})
		info_element = etree.fromstring(response.content)
		self.failUnlessEqual(info_element.get('power_state'), self.projector.power_state)
		self.failUnlessEqual(self.projector.power_state, PJLinkProtocol.POWER_ON_STATUS)
		response = self.client.post(projector_info_url, {'power':PJLinkProtocol.POWER_OFF_STATUS})
		info_element = etree.fromstring(response.content)
		self.failUnlessEqual(info_element.get('power_state'), self.projector.power_state)
		self.failUnlessEqual(self.projector.power_state, PJLinkProtocol.POWER_OFF_STATUS)


class PJLinkTest(TestCase):
	def setUp(self):
		self.projector = MockPJLinkProjector()
		self.projector.start()

	def tearDown(self):
		self.projector.stop_server()

	def test_controller(self):
		seconds_to_wait = 5
		while self.projector.running == False and seconds_to_wait > 0:
			time.sleep(1)
			seconds_to_wait -= 1
		self.failUnless(self.projector.running)

		# Connection and authentication
		bad_controller = PJLinkController(self.projector.server.getsockname()[0], self.projector.server.getsockname()[1], password='badPassword')
		try:
			bad_controller.query_name()
			self.fail() # should have thrown an authentication exception
		except PJLinkAuthenticationException:
			pass # this is what should happen
		self.projector.password = None
		unauth_controller = PJLinkController(self.projector.server.getsockname()[0], self.projector.server.getsockname()[1], password=None)
		try:
			unauth_controller.query_name()
		except PJLinkAuthenticationException:
			self.fail() # should not throw an authentication exception because both think there's no password
		self.projector.password = 'moceanWorker'
		controller = PJLinkController(self.projector.server.getsockname()[0], self.projector.server.getsockname()[1], password=self.projector.password)
		try:
			self.failUnlessEqual(controller.query_name(), self.projector.projector_name)
		except PJLinkAuthenticationException:
			self.fail() # should not throw an authentication exception because they agree on the password

		# Power setting, querying
		self.failUnless(self.projector.lamps[0][1] == False)
		self.failUnlessEqual(controller.query_power(), PJLinkProtocol.POWER_OFF_STATUS)
		self.failUnless(controller.power_on())
		self.failUnlessEqual(controller.query_power(), PJLinkProtocol.POWER_ON_STATUS)
		self.failUnless(self.projector.lamps[0][1] == True)
		self.failUnless(controller.power_off())
		self.failUnlessEqual(controller.query_power(), PJLinkProtocol.POWER_OFF_STATUS)
		self.failUnless(self.projector.lamps[0][1] == False)

		controller.power_on()

		# Input querying and setting
		input_state, input_number = controller.query_input()
		self.failUnlessEqual(input_state, PJLinkProtocol.RGB_INPUT)
		self.failUnlessEqual(input_number, PJLinkProtocol.INPUT_1)
		self.failUnless(controller.set_input(PJLinkProtocol.RGB_INPUT, PJLinkProtocol.INPUT_2))
		input_state, input_number = controller.query_input()
		self.failUnlessEqual(input_state, PJLinkProtocol.RGB_INPUT)
		self.failUnlessEqual(input_number, PJLinkProtocol.INPUT_2)
		self.failUnless(controller.set_input(PJLinkProtocol.VIDEO_INPUT, PJLinkProtocol.INPUT_3))
		input_state, input_number = controller.query_input()
		self.failUnlessEqual(input_state, PJLinkProtocol.VIDEO_INPUT)
		self.failUnlessEqual(input_number, PJLinkProtocol.INPUT_3)

		# Available inputs
		available_inputs = controller.query_available_inputs()
		self.failUnlessEqual(len(available_inputs), len(self.projector.available_inputs))
		for index, available_input in enumerate(self.projector.available_inputs):
			self.failUnlessEqual(available_inputs[index][0], self.projector.available_inputs[index][0])
			self.failUnlessEqual(available_inputs[index][1], self.projector.available_inputs[index][1])

		# Muting
		audio_mute, video_mute = controller.query_mute()
		self.failUnlessEqual(audio_mute, False)
		self.failUnlessEqual(video_mute, False)
		self.failUnless(controller.set_mute(PJLinkProtocol.AUDIO_VIDEO_MUTE_ON))
		audio_mute, video_mute = controller.query_mute()
		self.failUnlessEqual(audio_mute, True)
		self.failUnlessEqual(video_mute, True)
		self.failUnless(controller.set_mute(PJLinkProtocol.AUDIO_MUTE_OFF))
		self.failUnless(controller.set_mute(PJLinkProtocol.VIDEO_MUTE_ON))
		audio_mute, video_mute = controller.query_mute()
		#self.failUnlessEqual(audio_mute, False) # This fails because of the changes we made to make Panasonic projectors work.
		self.failUnlessEqual(video_mute, True)
		self.failUnless(controller.set_mute(PJLinkProtocol.AUDIO_MUTE_ON))
		self.failUnless(controller.set_mute(PJLinkProtocol.VIDEO_MUTE_OFF))
		audio_mute, video_mute = controller.query_mute()
		self.failUnlessEqual(audio_mute, True)
		self.failUnlessEqual(video_mute, False)

		# Error status
		fan_status, lamp_status, filter_status, cover_status, other_status = controller.query_error_status()
		self.failUnlessEqual(fan_status, PJLinkProtocol.ERROR_STATUS_OK)
		self.failUnlessEqual(lamp_status, PJLinkProtocol.ERROR_STATUS_OK)
		self.failUnlessEqual(filter_status, PJLinkProtocol.ERROR_STATUS_OK)
		self.failUnlessEqual(cover_status, PJLinkProtocol.ERROR_STATUS_OK)
		self.failUnlessEqual(other_status, PJLinkProtocol.ERROR_STATUS_OK)
		self.projector.errors[0][1] = PJLinkProtocol.ERROR_STATUS_ERROR
		fan_status, lamp_status, filter_status, cover_status, other_status = controller.query_error_status()
		self.failUnlessEqual(fan_status, PJLinkProtocol.ERROR_STATUS_ERROR)
		self.failUnlessEqual(lamp_status, PJLinkProtocol.ERROR_STATUS_OK)
		self.failUnlessEqual(filter_status, PJLinkProtocol.ERROR_STATUS_OK)
		self.failUnlessEqual(cover_status, PJLinkProtocol.ERROR_STATUS_OK)
		self.failUnlessEqual(other_status, PJLinkProtocol.ERROR_STATUS_OK)
		self.projector.errors[4][1] = PJLinkProtocol.ERROR_STATUS_ERROR
		fan_status, lamp_status, filter_status, cover_status, other_status = controller.query_error_status()
		self.failUnlessEqual(fan_status, PJLinkProtocol.ERROR_STATUS_ERROR)
		self.failUnlessEqual(lamp_status, PJLinkProtocol.ERROR_STATUS_OK)
		self.failUnlessEqual(filter_status, PJLinkProtocol.ERROR_STATUS_OK)
		self.failUnlessEqual(cover_status, PJLinkProtocol.ERROR_STATUS_OK)
		self.failUnlessEqual(other_status, PJLinkProtocol.ERROR_STATUS_ERROR)

		# LAMPS
		lamp_info = controller.query_lamps()
		self.failUnlessEqual(len(lamp_info), len(self.projector.lamps))
		for index, lamp in enumerate(self.projector.lamps):
			self.failUnlessEqual(len(lamp_info[index]), 2)
			self.failUnlessEqual(lamp_info[index][0], self.projector.lamps[index][0])
			self.failUnlessEqual(lamp_info[index][1], self.projector.lamps[index][1])
		controller.power_off()
		lamp_info = controller.query_lamps()
		for index, lamp in enumerate(self.projector.lamps):
			self.failUnlessEqual(lamp_info[index][0], self.projector.lamps[index][0])
			self.failUnlessEqual(lamp_info[index][1], self.projector.lamps[index][1])
		self.projector.lamps = [[0, False]]
		lamp_info = controller.query_lamps()
		for index, lamp in enumerate(self.projector.lamps):
			self.failUnlessEqual(lamp_info[index][0], self.projector.lamps[index][0])
			self.failUnlessEqual(lamp_info[index][1], self.projector.lamps[index][1])

		# INFO
		self.failUnlessEqual(controller.query_name(), self.projector.projector_name)
		self.failUnlessEqual(controller.query_manufacture_name(), self.projector.manufacture_name)
		self.failUnlessEqual(controller.query_product_name(), self.projector.product_name)
		self.failUnlessEqual(controller.query_other_info(), self.projector.other_info)
		self.failUnlessEqual(controller.query_class_info(), self.projector.class_info)

	def test_codecs(self):
		command1 = PJLinkCommandLine(PJLinkProtocol.POWER, PJLinkProtocol.ON)
		self.failUnlessEqual(command1.version, 1)
		self.failUnlessEqual(command1.command, PJLinkProtocol.POWER)
		self.failUnlessEqual(command1.data, PJLinkProtocol.ON)

		command2 = PJLinkCommandLine.decode(command1.encode())
		self.failUnlessEqual(command1.encode(), command2.encode())
		self.failUnlessEqual(command1.command, command2.command)
		self.failUnless(command1.data, command2.data)
		self.failUnless(command1.version, command2.version)

		response1 = PJLinkResponse(PJLinkProtocol.POWER, "1")
		self.failUnlessEqual(response1.version, 1)
		self.failUnlessEqual(response1.command, PJLinkProtocol.POWER)
		self.failUnlessEqual(response1.data, "1")

		response2 = PJLinkResponse.decode(response1.encode())
		self.failUnlessEqual(response1.encode(), response2.encode())
		self.failUnlessEqual(response1.version, response2.version)
		self.failUnlessEqual(response1.command, response2.command)
		self.failUnlessEqual(response1.data, response2.data)
