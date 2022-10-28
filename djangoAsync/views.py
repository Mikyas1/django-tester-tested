import time
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.apps import apps
from django_hint import RequestType


@api_view(['GET'], )
def hello_world(request: RequestType):
    for conf in apps.app_configs:
        for model in apps.app_configs[conf].get_models():
            # print(conf, model.objects.all())  # get all records from all tables found in registered apps
            pass
    return Response("hello world")


@api_view(['GET'], )
def sleep_for_given_seconds(request: RequestType, seconds: int):
    time.sleep(seconds)
    return Response(f"slept for {seconds} seconds.")
