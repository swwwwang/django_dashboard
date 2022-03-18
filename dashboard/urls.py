from django.urls import path
from dashboard import views

urlpatterns = [
    path('first', views.first),
    path('conncected', views.connected),
    path('bestcentres', views.bestcentres),
    path('has_data', views.has_data)
]
