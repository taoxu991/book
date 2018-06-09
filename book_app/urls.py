from django.conf.urls import url
from book_app import views as book_views

urlpatterns = [

    url(r'^book_add/', book_views.book_add),
    url(r'^book_info/(?P<nid>\d+)', book_views.book_info),
    url(r'^book_update/(?P<nid>\d+)', book_views.book_update),
    url(r'^book_delete/', book_views.book_delete),

    url(r'^author_add/', book_views.author_add),
    url(r'^author_info/(?P<nid>\d+)', book_views.author_info),
    url(r'^author_update/(?P<nid>\d+)', book_views.author_update),
    url(r'^author_delete/', book_views.author_delete),

    url(r'^publish_add/', book_views.publish_add),
    url(r'^publish_info/(?P<nid>\d+)', book_views.publish_info),
    url(r'^publish_update/(?P<nid>\d+)', book_views.publish_update),
    url(r'^publish_delete/', book_views.publish_delete),

    # url(r'^add/(?P<type>)\w+/(?P<nid>\d+)', book_views.add_handle),
    # url(r'^info/(?P<type>)\w+/(?P<nid>\d+)', book_views.info_handle),
    # url(r'^update/(?P<type>)\w+/(?P<nid>\d+)', book_views.update_handle),
    # url(r'^delete/(?P<type>)\w+/(?P<nid>\d+)', book_views.delete_handle),
    url(r'^list/(?P<model_type>\w+)', book_views.list_handle),
]
