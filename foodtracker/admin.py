from django.contrib import admin

# from .models import User, Food, FoodCategory, FoodLog, Image, Weight
from .models import *

admin.site.register(User)
admin.site.register(Food)
admin.site.register(FoodCategory)
admin.site.register(FoodLog)
admin.site.register(Image)
admin.site.register(Weight)

class QuestionAdmin(admin.ModelAdmin):
    list_display=('title','user')
    search_fields=('title','detail')
admin.site.register(Question,QuestionAdmin)

admin.site.register(Answer)

class CommentAdmin(admin.ModelAdmin):
    list_display=('answer','comment')
admin.site.register(Comment,CommentAdmin)

class UpvoteAdmin(admin.ModelAdmin):
    list_display=('answer','user')
admin.site.register(UpVote,UpvoteAdmin)

class DownvoteAdmin(admin.ModelAdmin):
    list_display=('answer','user')
admin.site.register(DownVote,DownvoteAdmin)