from django.urls import include, path
from .views import EventListFilterView, EventWithUsersAndOrganizationsView, OrganizationCreateView, EventCreateView, chat_view

urlpatterns = [
    path('create_organization/', OrganizationCreateView.as_view(), name='create-organization'),
    path('create_event/', EventCreateView.as_view(), name='create-event'),
    path('event_list/', EventListFilterView.as_view(), name='event-list'),
    path("events/<int:event_id>/with_users_organizations/", EventWithUsersAndOrganizationsView.as_view(), name="event-with-users-organizations"),
]