import adminapp.views as adminapp
from django.urls import path

app_name = 'adminapp'

urlpatterns = [
    path('users/read/', adminapp.TravelUsersListView.as_view(), name='users'),
    path('users/create/', adminapp.travel_user_create, name='user_create'),
    path('users/update/<int:pk>/', adminapp.travel_user_update, name='user_update'),
    path('users/delete/<int:pk>/', adminapp.travel_user_delete, name='user_delete'),

    path('countries/read/', adminapp.countries, name='countries'),
    path('countries/create/', adminapp.CountryCreateView.as_view(), name='country_create'),
    path('countries/update/<int:pk>/', adminapp.CountryUpdateView.as_view(), name='country_update'),
    path('countries/delete/<int:pk>/', adminapp.CountryDeleteView.as_view(), name='country_delete'),

    path('accommodation/read/countries/<int:pk>/', adminapp.accommodations, name='accommodations'),
    path('accommodation/create/countries/<int:pk>/', adminapp.accommodation_create, name='accommodation_create'),
    path('accommodation/update/<int:pk>/', adminapp.accommodation_update, name='accommodation_update'),
    path('accommodation/read/<int:pk>/', adminapp.AccommodationDetailView.as_view(), name='accommodation_read'),
    path('accommodation/delete/<int:pk>/', adminapp.accommodation_delete, name='accommodation_delete'),
]
