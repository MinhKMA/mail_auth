"""Authentication interface"""

from django.conf.urls import url

from auth_imap import views

urlpatterns = [
    url(r'^login/$', views.loginView, name='login'),
    url(r'^logout/$', views.logoutView, name='logout'),
    ]