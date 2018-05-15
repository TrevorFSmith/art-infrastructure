from lighting import serializers, models
from lighting.api import api_helpers
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework.exceptions import PermissionDenied

from lighting.pjlink import PJLinkController, PJLinkProtocol, SocketException
from lighting.connectors.bacnet import BacnetControl

from rest_framework.response import Response
from rest_framework import status

from django.conf import settings


class CrestonViewSet(api_helpers.GenericApiEndpoint):

    def get(self, request, format=None):
        projectors = models.BACNetLight.objects.all()
        serializer = serializers.BACNetLightSerializer(projectors, many=True)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        return Response([])

    def delete(self, request, pk, format=None):
        return Response([])

# def creston(request):
#     control = CrestonControl(settings.CRESTON_CONTROL_HOST)
#     message = None
#     control_info = None
#     return_json = False
#     try:
#         if request.method == 'POST':
#             command_form = CrestonCommandForm(request.POST)
#             if request.POST.get('action', None):
#                 action = request.POST.get('action')
#                 if action == 'high-up':
#                     control.raise_high()
#                 elif action == 'high-down':
#                     control.lower_high()
#                 elif action == 'low-up':
#                     control.raise_low()
#                 elif action == 'low-down':
#                     control.lower_low()
#                 else:
#                     print "Error: unknown action: %s" % action
#                     raise HttpResponseServeError('unknown action: %s' % action)
#                 return_json = True
#             elif request.POST.get('command', None):
#                 if command_form.is_valid():
#                     command = command_form.cleaned_data['command']
#                     if command == 'Update':
#                         lines = 9
#                     else:
#                         lines = 1
#                     result = control.send_command(command, lines)
#                     return HttpResponse(str(result or "Error"), mimetype='text/plain')
#                 else:
#                     print 'is not valid', command_form
#             else:
#                 print 'no POST', request.POST
#         else:
#             command_form = CrestonCommandForm()

#         try:
#             control_info = control.query_status()
#             #control_info = {'High': '55000', 'Current': '63098', 'Wake': '5:00 AM', 'Low': '63098', 'Lamp1': '2-1468', 'Sleep': '1:00 AM', 'Lamp2': '2-1469'}
#         except:
#             message = 'Could not communicate with the controller.'
#         if return_json: return HttpResponse(json.dumps(control_info), mimetype='application/json')
#         return render(request, 'lighting/creston.html', {'command_form':command_form, 'control_info':control_info})
#     except:
#         traceback.print_exc()


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

            # FIXME:
            # This is to be decided what to do with it. Probably makes sense to move it to Scheduler a.k.a. Heartbeat.
            #
            # audio_mute, video_mute = controller.query_mute()

            # info = ProjectorInfo(
            #     controller.query_power(),
            #     controller.query_name(),
            #     controller.query_manufacture_name(),
            #     controller.query_product_name(),
            #     controller.query_other_info(),
            #     audio_mute,
            #     video_mute
            #     )
            # See note above
            #
            # for lamp in controller.query_lamps():
            #     info.lamps.append(LampInfo(lamp[0], lamp[1]))

            if cmd == PJLinkProtocol.POWER_ON_STATUS:
                controller.power_on()

            elif cmd == PJLinkProtocol.POWER_OFF_STATUS:
                controller.power_off()

        except ObjectDoesNotExist:
            raise Http404
        except SocketException:
            return Response({"details": "Not able to connect to projector."}, status=status.HTTP_502_BAD_GATEWAY)

        projector_serializer = serializers.ProjectorSerializer(projector)
        projector_events_serializer = serializers.ProjectorEventsSerializer(
            models.ProjectorEvent.objects.filter(device=projector), many=True)

        return Response({"details": "Command successfully sent."}, status=status.HTTP_201_CREATED)


class ProjectorViewSet(api_helpers.GenericApiEndpoint):


    def get(self, request, format=None):
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
            projector  = models.Projector.objects.get(pk=int(request.data.get("id")))
            projector_id = projector.id
            projector.delete()
        except (ObjectDoesNotExist, TypeError):
            raise Http404

        return Response({"id": projector_id}, status=status.HTTP_200_OK)


class BACNetViewSet(api_helpers.GenericApiEndpoint):


    def get(self, request, format=None):
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
            bacnet_light  = models.BACNetLight.objects.get(pk=int(request.data.get("id")))
            bacnet_light_id = bacnet_light.id
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

        return Response({'cmd':light_value})


    def put(self, request, format=None):
        cmd = request.data.get("command")
        id  = int(request.data.get("id"))
        try:
            light = models.BACNetLight.objects.get(pk=id)
            control = BacnetControl(settings.BACNET_BIN_DIR)
            control.write_analog_output_int(light.device_id, light.property_id, cmd)
        except ObjectDoesNotExist:
            raise Http404
        except IOError:
            details = "Could not write the posted value (%s) for bacnet device %s property %s" % (cmd, light.device_id, light.property_id)
            return Response({"details": details}, status=status.HTTP_502_BAD_GATEWAY)

        return Response({"details": "Command sent."}, status=status.HTTP_200_OK)
