from django.shortcuts import render

from rest_framework import generics, permissions

from .models import Ticket


from .serializers import TicketListUserSerializer, TicketCreateSerializer

class TicketListCreateView(generics.ListCreateAPIView):


    def get_queryset(self):
        user = self.request.user

        queryset = Ticket.objects.filter(is_deleted=False).select_related(
            'created_by',
            'assigned_to'
        ).prefetch_related(
            'status_history'
        )
        if not (user.is_staff or user.is_superuser):
            queryset = queryset.filter(created_by=user)

        ticket_type = self.request.query_params.get('type')
        status = self.request.query_params.get('status')

        if ticket_type:
            queryset = queryset.filter(ticket_type=ticket_type)

        return queryset.order_by('-created_at')


    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TicketCreateSerializer

        return TicketListUserSerializer

