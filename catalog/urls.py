from django.urls import path
from . import views
from django.conf.urls import url


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^movie/(?P<pk>\d+)$', views.NMovieDetailView.as_view(), name='movie-detail'),
    url(r'^ticket/(?P<pk>\d+)$',views.NTicketDetailView.as_view(),name='ticket'),
    url(r'^movies/$',views.NMovieListView.as_view(),name='movies'),
    url('supervisor/',views.supervisor_panel,name='supervisor'),
    url('about/',views.about,name="about"),
]