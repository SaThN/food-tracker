from django.urls import path
from . import views

urlpatterns=[
    path('',views.forum,name='forum'),
    path('detail/<int:id>',views.detail,name='detail'),
    path('save-comment',views.save_comment,name='save-comment'),
    path('save-upvote',views.save_upvote,name='save-upvote'),
    path('save-downvote',views.save_downvote,name='save-downvote'),

    # Ask Question
    path('ask-question',views.ask_form,name='ask-question'),

    # Tag Page
    path('tag/<str:tag>',views.tag,name='tag'),
    path('tags',views.tags,name='tags'),
   
]