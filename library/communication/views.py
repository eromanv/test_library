from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from library.celery import create_event_with_delay
from .models import Organization, Event
from .serializers import OrganizationSerializer, EventSerializer
from django.utils.dateparse import parse_datetime
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

import tracemalloc

def chat_view(request):
    return render(request, 'chat.html')

class OrganizationCreateView(generics.CreateAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]


class EventCreateView(generics.CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        instance = serializer.save()
        create_event_with_delay.delay(instance.id)
    

class EventListFilterView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Event.objects.all()

        # Фильтрация по дате
        date_param = self.request.query_params.get("date", None)
        if date_param:
            # Преобразование строки даты в формат datetime
            date_param = parse_datetime(date_param)
            queryset = queryset.filter(date__gte=date_param)

        # Фильтрация по названию
        title_param = self.request.query_params.get("title", None)
        if title_param:
            queryset = queryset.filter(title__icontains=title_param)

        # Сортировка по дате
        queryset = queryset.order_by("date")

        return queryset

class EventWithUsersAndOrganizationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, event_id):
        try:
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

        serialized_event = EventSerializer(event).data
        users_data = []

        for organization in event.organizations.all():
            for user in organization.members.all():
                user_data = {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "organization": {
                        "id": organization.id,
                        "title": organization.title,
                        "address": organization.address,
                        "postcode": organization.postcode,
                    }
                }
                users_data.append(user_data)

        serialized_event["users"] = users_data

        return Response(serialized_event)

