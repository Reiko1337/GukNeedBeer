from django.urls import path
from .views import beer, beer_add, list_beer, DeleteBeer, UpdateBeer

urlpatterns = [
    path('', beer, name='beer'),
    path('beer_add/', beer_add, name='beer_add'),
    path('list_beer/', list_beer, name='list_beer'),
    path('list_beer/<int:pk>/delete', DeleteBeer.as_view(), name='delete_beer'),
    path('list_beer/<int:pk>/edit', UpdateBeer.as_view(), name='edit_beer'),
]
