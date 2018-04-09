from django import forms
from django.contrib import admin

from models import (
	BACNetLight,
	Projector,
	ProjectorEvent
)

class StyledModelAdmin(admin.ModelAdmin):
	save_on_top=True
	class Media:
		css = { "all": ('admin.css', )}

class BACNetLightAdmin(StyledModelAdmin):
	list_display = ('name', )
admin.site.register(BACNetLight, BACNetLightAdmin)	

class ProjectorAdmin(StyledModelAdmin):
	list_display = ('name', 'pjlink_host', 'pjlink_port')
admin.site.register(Projector, ProjectorAdmin)	

class ProjectorEventAdmin(StyledModelAdmin):
	readonly_fields = ('tries', 'last_run')
admin.site.register(ProjectorEvent, ProjectorEventAdmin)	
