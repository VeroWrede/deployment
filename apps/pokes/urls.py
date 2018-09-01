from django.conf.urls import url, include
from . import views 

urlpatterns = [
    url(r'^(?P<user_id>\d+)/poke$', views.poke, name="poke")
]