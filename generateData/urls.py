from django.conf.urls import url, include
from django.contrib import admin

from . import views

admin.autodiscover()

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'index$', views.index, name='index'),
    url(r'generate$', views.generate, name='generate'),
    url('^admin/', include(admin.site.urls)),


    #requete fait en ajax pour obtenir des informations de facon dynamique
    url(r'getExempleByTypeDonnees$', views.getExempleByTypeDonnees),
    url(r'getTypeDonnees$', views.getTypeDonnees),
]