"""book URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from book_app import views as book_views
from django.views.static import serve
from book import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/',book_views.index),
    url(r'^book/',book_views.book_list),
    url(r'^publish/',book_views.publish_list),
    url(r'^author/',book_views.author_list),
    url(r'^$',book_views.index),
    url(r'^login/',book_views.log_in,name='login'),
    url(r'^logout/',book_views.log_out,name='logout'),
    url(r'^register/',book_views.register,name='register'),
    url(r'^get_valid_img/',book_views.get_valid_img,name='get_valid_img'),
    url(r'^manage/',include('book_app.urls')),

    # media 配置
    url(r'^media/(?P<path>.*)$', serve,{'document_root':settings.MEDIA_ROOT}),
]
