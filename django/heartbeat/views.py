import logging
logger = logging.getLogger(__name__)

from django.shortcuts import render, render_to_response
from django.http import (
    Http404,
    HttpResponse,
    HttpResponseRedirect,
    HttpResponseServerError,
    HttpResponsePermanentRedirect
)

from artwork.models import Installation

from models import Heartbeat

INFO_PARAMETER = 'info'
INSTALLATION_ID_PARAMETER = 'installation_id'
CLEAN_HEARTBEATS_PARAMETER = 'clean_heartbeats'


def index(request):

    if request.GET.has_key(INSTALLATION_ID_PARAMETER):
        id = int(request.GET[INSTALLATION_ID_PARAMETER])
        info = request.GET.get(INFO_PARAMETER, None)
        try:
            installation = Installation.objects.get(pk=id)
            heartbeat = Heartbeat(installation=installation, info=info)
            heartbeat.save()
        except:
            logger.exception("Received heartbeat for unknown installation id: %s from IP# %s" % (id, request.META['REMOTE_ADDR']))

    if request.GET.has_key(CLEAN_HEARTBEATS_PARAMETER):
        Heartbeat.objects.delete_old_heartbeats()

    return render(request, 'heartbeat/index.html', {
        'installations':Installation.objects.all_open(),
        'heartbeats':Heartbeat.objects.all()
    })
