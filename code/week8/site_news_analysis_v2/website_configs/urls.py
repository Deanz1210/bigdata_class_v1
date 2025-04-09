"""
URL configuration for website_configs project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from django.urls import include

urlpatterns = [
   #path('admin/', admin.site.urls),
   path('topword/', include('app_top_keyword.urls')),
   path('topperson/', include('app_top_person.urls')),
    path('userkeyword/', include('app_user_keyword.urls')),
   path('hotpersonsofyesterday/', include('app_hot_persons_of_yesterday.urls', namespace='app_hot_person_of_yesterday')),
    path('voiceofshare/', include('app_voice_of_share.urls')),
    path('wordcloud/', include('app_word_cloud.urls')),
    path('correlation/', include('app_correlation_analysis.urls')),
    path('userkeyword_assoc/', include('app_user_keyword_association.urls')),
    
]
