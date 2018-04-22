import simplejson
from datetime import timedelta

import logging
logger = logging.getLogger(__name__)

from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import PermissionDenied

from django.http import Http404
from django.utils import timezone
from django.http import HttpResponse
from django.db.models.query import Q
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from ai.api import NoPermission
from ai.api import StaffPermission
from ai.api import PaginatedAPIView
from ai.api import ActiveAndAuthenticatedPermission

from . import serializers

class AuthView_0_1(APIView):
    '''
    AuthView returns the requesting User's info or an empty map if the request is not authed and active.
    '''
    permission_classes = (NoPermission,)

    def get(self, request):
        if request.user.is_anonymous() or not request.user.is_active: return Response({})
        return Response(serializers.SelfUserSerializer_0_1(request.user, context={'request':request}).data)
