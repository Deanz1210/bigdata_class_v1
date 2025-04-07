from django.urls import path
from app_voice_of_share import views

app_name="app_voice_of_share"

urlpatterns = [
    
    # the first way:
    path('', views.home, name='home'),
   

    # the second way:
    #path('top_userkey/', views.home, name='home'),
    #path('top_userkey/api_get_top_userkey/', views.api_get_top_userkey),

]

'''
# the first way:
The url path on the browser will be
http://localhost:8000/userkeyword/

# the second way:
The url path on the browser will be
http://localhost:8000/userkeyword/top_userkey/

The ajax url is as the following:
$.ajax({
    type: "POST",
    url: "api_get_top_userkey/",
'''
