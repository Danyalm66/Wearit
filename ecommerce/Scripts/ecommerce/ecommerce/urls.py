"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.views.generic.base import TemplateView
from django.conf.urls import include, url, handler404, handler500,handler403,handler400
from django.contrib import admin
from django.urls import path
from products import views
urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'query/', views.filter_form, name='filter_form'),
    url(r'search/', views.search_query, name='search-query'),
] 
handler404=views.error
handler500=views.error
handler403 = views.error
handler400 = views.error