"""lastdemo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,re_path
from app01 import views
from app022 import views as view22
from app033 import views as view33
from app044 import views as view44
urlpatterns = [
    # path('admin', admin.site.urls),
    path(r'show/',views.show_msg),
    # path(r'reports/',views.show_people_report),
    path(r'msgupload/',view22.msgupload,name='msg'),
    re_path(r'^symsg/(?P<id>\d+)/',view22.show_symsg,name='symsg'),
    path(r'syadd',view22.add_symsg,name='addmsg'),
    path(r'reports',view22.cnfllmsg,name='cnfllmsg'),
    path(r'download',view22.download,name='download'),
    path(r'listdownload', view22.listdownload, name='listdownload'),
    path('cnmsg/',view33.cn_msg),
    path('CTW_LT/',view33.CTW_LT ,name='CTW_LT'),
    path(r'text/',view44.greeting.test1)



]
