from lighting import serializers, models
from lighting.api import api_helpers
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework.exceptions import PermissionDenied

from lighting.pjlink import PJLinkController, PJLinkProtocol, SocketException as PJLinkSocketException
from lighting.bacnet import BacnetControl
from lighting.creston import CrestonControl, SocketException as CrestonSocketException
from artwork.models import Equipment

from rest_framework.response import Response
from rest_framework import status

from django.conf import settings


class CrestonViewSet(api_helpers.GenericApiEndpoint):

    get_queryset_class            = models.Creston
    get_queryset_serializer_class = serializers.CrestonSerializer

    def get(self, request, format=None, paginate="on"):
        if paginate == "on":
            return super(CrestonViewSet, self).get(request, format)
        else:
            crestons = models.Creston.objects.all()
            serializer = serializers.CrestonSerializer(crestons, many=True)
            return Response(serializer.data)

    def post(self, request, format=None):
        serializer = serializers.CrestonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        try:
            creston  = models.Creston.objects.get(pk=int(request.data.get("id")))
            serializer = serializers.CrestonSerializer(creston, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except ObjectDoesNotExist:
            raise Http404

    def delete(self, request, format=None):
        try:
            creston = models.Creston.objects.get(pk=int(request.data.get("id")))
            creston_id = creston.id
            Equipment.delete_device(creston)
            creston.delete()
        except (ObjectDoesNotExist, TypeError):
            raise Http404

        return Response({"id": creston_id}, status=status.HTTP_200_OK)


class CrestonCommandViewSet(api_helpers.GenericApiEndpoint):

    def get(self, request, format=None):
        try:
            creston = models.Creston.objects.get(pk=int(request.data.get("id")))
            control = CrestonControl(creston.host, creston.port)
            control_info = control.query_status()
            #control_info = {'High': '55000', 'Current': '63098', 'Wake': '5:00 AM', 'Low': '63098', 'Lamp1': '2-1468', 'Sleep': '1:00 AM', 'Lamp2': '2-1469'}
        except ObjectDoesNotExist:
            raise Http404
        except IOError:
            control_info = None

        return Response({'details':control_info})

    def put(self, request, format=None):
        command = request.data.get("command")
        id  = int(request.data.get("id"))
        try:
            creston = models.Creston.objects.get(pk=id)
            control = CrestonControl(creston.host, creston.port)
            if command == 'Update':
                lines = 9
            else:
                lines = 1
            result = control.send_command(command, lines)
            # Please use result and pass it to the UI and render it there.
        except ObjectDoesNotExist:
            raise Http404
        except CrestonSocketException:
            return Response({"details": "Not able to connect to creston."}, status=status.HTTP_502_BAD_GATEWAY)

        return Response({"details": "Command successfully sent."}, status=status.HTTP_201_CREATED)


class ProjectorInfo:

    def __init__(self, power_state, projector_name, manufacture_name, product_name, other_info, audio_mute, video_mute):
        self.power_state = power_state
        self.projector_name = projector_name
        self.manufacture_name = manufacture_name
        self.product_name = product_name
        self.other_info = other_info
        self.video_mute = video_mute
        self.audio_mute = audio_mute
        self.lamps = []


class LampInfo:
    def __init__(self, lighting_hours, is_on):
        self.lighting_hours = lighting_hours
        self.is_on = is_on


class ProjectorCommandViewSet(api_helpers.GenericApiEndpoint):

    def put(self, request, format=None):

        cmd      = request.data.get("command")
        event_id = request.data.get("event_id")

        try:

            if cmd not in [PJLinkProtocol.POWER_ON_STATUS, PJLinkProtocol.POWER_OFF_STATUS]:
                return Response({"details": "Command '%s' not supported." % cmd}, status=status.HTTP_400_BAD_REQUEST)

            projector  = models.Projector.objects.get(pk=int(request.data.get("id")))
            controller = PJLinkController(projector.pjlink_host, projector.pjlink_port, projector.pjlink_password)

            if cmd == PJLinkProtocol.POWER_ON_STATUS:
                controller.power_on()

            elif cmd == PJLinkProtocol.POWER_OFF_STATUS:
                controller.power_off()

        except ObjectDoesNotExist:
            raise Http404
        except PJLinkSocketException:
            return Response({"details": "Not able to connect to projector."}, status=status.HTTP_502_BAD_GATEWAY)

        projector_serializer = serializers.ProjectorSerializer(projector)
        projector_events_serializer = serializers.ProjectorEventsSerializer(
            models.ProjectorEvent.objects.filter(device=projector), many=True)

        return Response({"details": "Command successfully sent."}, status=status.HTTP_201_CREATED)


class ProjectorViewSet(api_helpers.GenericApiEndpoint):

    get_queryset_class            = models.Projector
    get_queryset_serializer_class = serializers.ProjectorSerializer

    def get(self, request, format=None, paginate="on"):
        if paginate == "on":
            return super(ProjectorViewSet, self).get(request, format)
        else:
            projectors = models.Projector.objects.all()
            serializer = serializers.ProjectorSerializer(projectors, many=True)
            return Response(serializer.data)

    def post(self, request, format=None):
        serializer = serializers.ProjectorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        try:
            projector  = models.Projector.objects.get(pk=int(request.data.get("id")))
            serializer = serializers.ProjectorSerializer(projector, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except ObjectDoesNotExist:
            raise Http404

    def delete(self, request, format=None):
        try:
            projector = models.Projector.objects.get(pk=int(request.data.get("id")))
            projector_id = projector.id
            Equipment.delete_device(projector)
            projector.delete()
        except (ObjectDoesNotExist, TypeError):
            raise Http404

        return Response({"id": projector_id}, status=status.HTTP_200_OK)


class BACNetViewSet(api_helpers.GenericApiEndpoint):

    get_queryset_class            = models.BACNetLight
    get_queryset_serializer_class = serializers.BACNetLightSerializer

    def get(self, request, format=None, paginate="on"):
        if paginate == "on":
            return super(BACNetViewSet, self).get(request, format)
        else:
            bacnet_lights = models.BACNetLight.objects.all()
            serializer = serializers.BACNetLightSerializer(bacnet_lights, many=True)
            return Response(serializer.data)

    def post(self, request, format=None):
        serializer = serializers.BACNetLightSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        try:
            bacnet_light = models.BACNetLight.objects.get(pk=int(request.data.get("id")))
            serializer = serializers.BACNetLightSerializer(bacnet_light, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except ObjectDoesNotExist:
            raise Http404

    def delete(self, request, format=None):
        try:
            bacnet_light = models.BACNetLight.objects.get(pk=int(request.data.get("id")))
            bacnet_light_id = bacnet_light.id
            Equipment.delete_device(bacnet_light)
            bacnet_light.delete()
        except (ObjectDoesNotExist, TypeError):
            raise Http404

        return Response({"id": bacnet_light_id}, status=status.HTTP_200_OK)


class BACNetCommandViewSet(api_helpers.GenericApiEndpoint):

    def get(self, request, format=None):
        try:
            light = models.BACNetLight.objects.get(pk=int(request.data.get("id")))
            control = BacnetControl(settings.BACNET_BIN_DIR)
            light_value = control.read_analog_output(light.device_id, light.property_id)[1]
        except ObjectDoesNotExist:
            raise Http404
        except IOError:
            light_value = None

        return Response({"details":"Command - #{light_value}"})

    def put(self, request, format=None):
        cmd = request.data.get("command")
        try:
            light = models.BACNetLight.objects.get(pk=request.data.get("id"))
            control = BacnetControl(settings.BACNET_BIN_DIR)
            control.write_analog_output_int(light.device_id, light.property_id, cmd)
        except ObjectDoesNotExist:
            raise Http404
        except IOError, e:
            return Response({"details": str(e)}, status=status.HTTP_502_BAD_GATEWAY)
        except Exception, e:
            return Response({"details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"details": "Command successfully sent."}, status=status.HTTP_201_CREATED)
