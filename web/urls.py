from django.conf.urls import url
from . import views
from webtester.settings import PAGE_CRAWLER_URL

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login', views.login_view, name='login'),
    url(r'^dashboard', views.dashboard, name='dashboard'),
    url(r'^report', views.report, name='report'),
    url(r'^add_post', views.add_test_post),
    url(r'^crawler', views.crawler,name='crawler'),
    url(r'^add_report_list',views.add_post_report_list)
]
