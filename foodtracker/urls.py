from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
    path('profile/weight', views.weight_log_view, name='weight_log'),
    path('profile/weight/delete/<int:weight_id>', views.weight_log_delete, name='weight_log_delete'),

    path('food/list', views.food_list_view, name='food_list'),
    path('food/add', views.food_add_view, name='food_add'),
    path('food/edit/<int:food_id>/', views.food_edit_view, name='food_edit'),
    path('food/delete/<int:food_id>/', views.food_delete_view, name='food_delete'),
    path('food/foodlog', views.food_log_view, name='food_log'),
    path('food/foodlog/delete/<int:food_id>', views.food_log_delete, name='food_log_delete'),
    path('food/<str:food_id>', views.food_details_view, name='food_details'),

    path('categories', views.categories_view, name='categories_view'),
    path('categories/<str:category_name>', views.category_details_view, name='category_details_view'),

    ##Forum Paths
    path('forum/', include('foodtracker.forum.urls')),




    # Recipe Paths
#     path('recipe/', include('foodtracker.recipe.urls')),

    # Admin URLs
    path('admin/food/add/', views.food_add_view, name='admin_food_add'),
    path('admin/food/edit/<int:food_id>/', views.food_edit_view, name='admin_food_edit'),
    path('admin/food/delete/<int:food_id>/', views.food_delete_view, name='admin_food_delete'),
]
