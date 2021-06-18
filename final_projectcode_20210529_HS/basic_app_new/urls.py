from django.urls import path,include
from basic_app_new import views 
from django.conf import settings
from django.conf.urls import url
app_name = 'basic_app_new'

urlpatterns=[
   path('north/',views.north,name='north'),
   path('search',views.search,name='search'),
]