from django.conf.urls import url
from deal import views

urlpatterns = [
    url(r'^', views.deals, name='deal')
]
