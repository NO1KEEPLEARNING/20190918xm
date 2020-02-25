from django.urls import path,re_path
from  .  import views
urlpatterns = [
    # path('admin', admin.site.urls),
    path(r'1show/',views.produce_show.produce_sunmsg)




]