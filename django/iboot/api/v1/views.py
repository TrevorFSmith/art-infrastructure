from iboot import serializers, models
from iboot.api import api_helpers
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import status

from iboot.iboot_control import IBootControl, SocketException
from django.conf import settings


class IBootViewSet(api_helpers.GenericApiEndpoint):

    get_queryset_class            = models.IBootDevice
    get_queryset_serializer_class = serializers.IBootSerializer

    def get(self, request, format=None, paginate="on"):
        if paginate == "on":
            return super(IBootViewSet, self).get(request, format)
        else:
            iboots = models.IBootDevice.objects.all()
            serializer = serializers.IBootSerializer(iboots, many=True)
            return Response(serializer.data)

    def post(self, request, format=None):
        serializer = serializers.IBootSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        try:
            iboot  = models.IBootDevice.objects.get(pk=int(request.data.get("id")))
            serializer = serializers.IBootSerializer(iboot, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except ObjectDoesNotExist:
            raise Http404

    def delete(self, request, format=None):
        try:
            iboot  = models.IBootDevice.objects.get(pk=int(request.data.get("id")))
            iboot_id = iboot.id
            iboot.delete()
        except (ObjectDoesNotExist, TypeError):
            raise Http404

        return Response({"id": iboot_id}, status=status.HTTP_200_OK)


class IBootCommandViewSet(api_helpers.GenericApiEndpoint):

    def get(self, request, format=None):
        try:
            iboot = models.IBootDevice.objects.get(pk=int(request.data.get("id")))
            control = IBootControl(settings.IBOOT_POWER_PASSWORD, iboot.host, iboot.port)
            control_status = control.query_iboot_state()
        except ObjectDoesNotExist:
            raise Http404
        except SocketException:
            control_status = None

        return Response({'control_status':control_status})

    def put(self, request, format=None):
        command = request.data.get("command")
        try:
            if command not in ["cycle", "on", "off", "toggle"]:
                return Response({"details": "Command '%s' not supported." % command}, status=status.HTTP_400_BAD_REQUEST)

            iboot = models.IBootDevice.objects.get(pk=int(request.data.get("id")))
            control = IBootControl(settings.IBOOT_POWER_PASSWORD, iboot.host, iboot.port)
            if command == 'cycle':
                control.cycle_power()
            elif command == 'on':
                control.turn_on()
            elif command == 'off':
                control.turn_off()
            elif command == 'toggle':
                control.toggle()
        except ObjectDoesNotExist:
            raise Http404
        except SocketException:
            return Response({"details": "Not able to connect to iBoot."}, status=status.HTTP_502_BAD_GATEWAY)
        except Exception, e:
            return Response({"details": str(e)}, status=status.HTTP_502_BAD_GATEWAY)

        return Response({"details": "Command successfully sent."}, status=status.HTTP_201_CREATED)
