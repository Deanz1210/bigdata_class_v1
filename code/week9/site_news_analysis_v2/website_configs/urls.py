from django.contrib import admin
from django.urls import path, include
from app_game_mayor import views as mayor_views  # <<== 新增這行，取別名 mayor_views

urlpatterns = [
    path('', mayor_views.home, name='home'),  # <<== 設定首頁，home 由 app_game_mayor.views.home 控制
    path('api_get_game_mayor_data/', mayor_views.api_get_game_mayor_data, name='api_get_game_mayor_data'),  # <<== 新增 API 路由

    path('topword/', include('app_top_keyword.urls')),
    path('topperson/', include('app_top_person.urls')),
    path('userkeyword/', include('app_user_keyword.urls')),
    path('hotpersonsofyesterday/', include('app_hot_persons_of_yesterday.urls', namespace='app_hot_person_of_yesterday')),
    path('voiceofshare/', include('app_voice_of_share.urls')),
    path('wordcloud/', include('app_word_cloud.urls')),
    path('correlation/', include('app_correlation_analysis.urls')),
    path('userkeyword_assoc/', include('app_user_keyword_association.urls')),
    path('userkeyword_senti/', include('app_user_keyword_sentiment.urls')),
    path('gamemayor/', include('app_game_mayor.urls')),
]
