from django.urls import path

from .views import TicketListCreateView


urlpatterns = [
    path('ticket', TicketListCreateView.as_view())
]