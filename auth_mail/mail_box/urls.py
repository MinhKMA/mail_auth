from django.conf.urls import url
from django.urls import path
from mail_box import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^compose$', views.compose, name='compose'),
    url(r'^sent$', views.sent, name='sent'),
    url(r'^drafts$', views.drafts, name='drafts'),
    url(r'^junk$', views.junk, name='junk'),
    url(r'^trash$', views.trash, name='trash'),
    path('<slug:uuid>/read/', views.read_mail, name='read'),
    url(r'^sentmail$', views.send_mail_test, name='compose_mail'),
]