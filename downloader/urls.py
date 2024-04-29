from django.urls import path
from .views import index_views

urlpatterns = [
    path('', index_views.index, name='index'), 
    path('download/', index_views.download_video, name='download_video'),
    path('features/', index_views.features, name='features'),
    path('pricing/', index_views.pricing, name='pricing'),
    path('donate/', index_views.donate, name='donate'),
]
