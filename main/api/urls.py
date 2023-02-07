from django.urls import path, include
from main.api import views
from rest_framework import routers

app_name = 'main'

router = routers.DefaultRouter()
router.register('main', viewset=views.ProductViewSet)

urlpatterns = [
    path('game_category/', views.GameCategoryListView.as_view(), name='game_category_list'),
    path('game_category/<pk>/', views.GameCategoryDetailView.as_view(), name='game_category_detail'),
    path('', include(router.urls))
]