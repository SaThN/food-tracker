from django import forms
from django.forms import ModelForm

# from .models import Food, Image, Answer, Question
from .models import *


class FoodForm(forms.ModelForm):
    '''
    A ModelForm class for adding a new food item
    '''
    class Meta:
        model = Food
        fields = ['food_name', 'quantity', 'calories', 'fat', 'carbohydrates', 'protein', 'category']

    def __init__(self, *args, **kwargs):
        super(FoodForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ImageForm(forms.ModelForm):
    '''
    A ModelForm class for adding an image to the food item
    '''
    class Meta:
        model = Image
        fields = ['image']

    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        self.visible_fields()[0].field.widget.attrs['class'] = 'form-control'

## Forum Forms

class AnswerForm(ModelForm):
    class Meta:
        model=Answer
        fields=('detail',)

class QuestionForm(ModelForm):
    class Meta:
        model=Question
        fields=('title','detail','tags')

## Recipe Forms