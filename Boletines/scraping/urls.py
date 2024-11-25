from django.urls import path
from .views import show_scrap
from .views import show_content
from .views import update_db

urlpatterns = [
    path('', show_scrap, name='scrap_urls'),
    path('news', show_content, name='news_content'),
    path('update-database/', update_db, name='update_database'),
]