from django.urls import path

from . import views

app_name = 'event'


urlpatterns = [
    path('',views.IndexList.as_view(),name='home'),
    path('<int:year>/<int:month>/<int:day>/<slug:event>',views.event,name='event_detail'),
    path('share/<int:post_id>',views.event_share,name='share_post'),
    path('add_comment/<int:post_id>',views.post_comment,name='post_comment')    
]