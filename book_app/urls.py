from django.conf.urls import url
from book_app import views as book_views

urlpatterns = [
    url(r'^add/(?P<model_type>\w+)', book_views.add_handle),
    url(r'^info/(?P<model_type>\w+)/(?P<nid>\d+)', book_views.info_handle),
    url(r'^update/(?P<model_type>\w+)/(?P<nid>\d+)', book_views.update_handle),
    url(r'^delete/(?P<model_type>\w+)', book_views.delete_handle),
    url(r'^list/(?P<model_type>\w+)', book_views.list_handle),
]
