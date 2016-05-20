from django.conf.urls import url
from . import views
from . import api

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login', views.login_view, name='login'),
    url(r'^dashboard', views.dashboard, name='dashboard'),
    url(r'^report', views.report, name='report'),
    url(r'^add_post', api.add_test_post),
    url(r'^crawler', api.crawler, name='crawler'),
    url(r'^add_report_list', api.add_post_report_list),
    url(r'^show_report_list',api.show_report_list)
]
