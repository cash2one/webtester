from django.conf.urls import url
from . import views
from django.conf.urls import include

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login',views.login_view,name='login'),
    url(r'^dashboard', views.dashboard, name='dashboard'),
    url(r'^add_post',views.add_test_post)
]
