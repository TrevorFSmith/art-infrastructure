from django.contrib import admin
from django import forms

from ai.admin import StyledModelAdmin

from models import (
	Heartbeat,
)

class HeartbeatAdmin(StyledModelAdmin):
	list_display = ('installation', 'created', 'trimmed_info')
	date_hierarchy = 'created'
	search_fields = ('installation__name', )
admin.site.register(Heartbeat, HeartbeatAdmin)	
