# Copyright 2009 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
import httplib
import urllib

from django.db import models


class StatusListenerTest(models.Model):

	name = models.CharField(max_length=512, null=False, blank=False)

	def __unicode__(self):
		return self.name


class StatusListenerManager(models.Manager):

	def broadcast_status(self, status):
		"""Send the status to all registered status listeners."""
		for listener in self.all(): listener.send_status(status)


class StatusListener(models.Model):
	"""A remote httpd which is requests status messages.  Set and deleted upon request from remote listener."""
	host = models.CharField(max_length=1024, null=False, blank=False, unique=True)
	created = models.DateTimeField(auto_now_add=True)
	tests = models.ManyToManyField(StatusListenerTest, blank=True, null=True)
	objects = StatusListenerManager()

	def send_status(self, status):
		"""Send the status to this status listener"""
		params = urllib.urlencode({'status':status})
		headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
		try:
			conn = httplib.HTTPConnection(self.host)
			conn.request("POST", "/status/", params, headers)
			response = conn.getresponse()
			response.read()
			conn.close()
			return True
		except:
			return False

	class Meta:
		ordering = ['-created']

	def __unicode__(self):
		return self.host
