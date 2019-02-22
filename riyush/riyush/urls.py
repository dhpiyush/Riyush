"""riyush URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin

from order import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^test$', views.test),
    # url(r'^signup$', views.signup),
    url(r'^available_slots$',views.available_slots),
    url(r'^orders/(?P<id>\d+)$',views.orders),
    url(r'^order_complete',views.order_complete),
    url(r'^menu/(?P<id>\d+)$',views.menu),
    url(r'^payment$', views.payment),
    url(r'^payment/success$', views.payment_success),
    url(r'^payment_details$', views.payment_details),
    url(r'^restaurants/(?P<id>\d+)$',views.restaurants),
    url(r'^save$',views.save_data),

]
