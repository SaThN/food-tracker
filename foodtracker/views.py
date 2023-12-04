from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required,  permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from django.db.models import Count

# from .models import User, Food, FoodCategory, FoodLog, Image, Weight
from .models import *
from .forms import FoodForm, ImageForm


def index(request):
    '''
    The default route which lists all food items
    '''
    return food_list_view(request)


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']

        # Ensure password matches confirmation
        password = request.POST['password']
        confirmation = request.POST['confirmation']
        if password != confirmation:
            return render(request, 'register.html', {
                'message': 'Passwords must match.',
                'categories': FoodCategory.objects.all()
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, 'register.html', {
                'message': 'Username already taken.',
                'categories': FoodCategory.objects.all()
            })
        login(request, user)
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'register.html', {
            'categories': FoodCategory.objects.all()
        })


def login_view(request):
    if request.method == 'POST':

        # Attempt to sign user in
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'login.html', {
                'message': 'Invalid username and/or password.',
                'categories': FoodCategory.objects.all()
            })
    else:
        return render(request, 'login.html',  {
            'categories': FoodCategory.objects.all()
        })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login_view'))

# Profile
def profile(request):
    quests=Question.objects.filter(user=request.user).order_by('-id')
    answers=Answer.objects.filter(user=request.user).order_by('-id')
    comments=Comment.objects.filter(user=request.user).order_by('-id')
    upvotes=UpVote.objects.filter(user=request.user).order_by('-id')
    downvotes=DownVote.objects.filter(user=request.user).order_by('-id')
    if request.method=='POST':
        profileForm=ProfileForm(request.POST,instance=request.user)
        if profileForm.is_valid():
            profileForm.save()
            messages.success(request,'Profile has been updated.')
    form=ProfileForm(instance=request.user)
    return render(request,'registration/profile.html',{
        'form':form,
        'quests':quests,
        'answers':answers,
        'comments':comments,
        'upvotes':upvotes,
        'downvotes':downvotes,
    })


def food_list_view(request):
    '''
    It renders a page that displays all food items
    Food items are paginated: 4 per page
    '''
#     foods = Food.objects.all()
    foods = Food.objects.all().order_by('id')  # Order by 'id' or any other field you want

    for food in foods:
        food.image = food.get_images.first()

    # Show 4 food items per page
    page = request.GET.get('page', 1)
    paginator = Paginator(foods, 4)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {
        'categories': FoodCategory.objects.all(),
        'foods': foods,
        'pages': pages,
        'title': 'Food List'
    })


def food_details_view(request, food_id):
    '''
    It renders a page that displays the details of a selected food item
    '''
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    food = Food.objects.get(id=food_id)

    return render(request, 'food.html', {
        'categories': FoodCategory.objects.all(),
        'food': food,
        'images': food.get_images.all(),
        'food_id': food_id,
    })


@login_required
@permission_required('accounts.view_lesson')
def food_add_view(request):
    '''
    It allows the user to add a new food item
    '''
    ImageFormSet = forms.modelformset_factory(Image, form=ImageForm, extra=2)

    if request.method == 'POST':
        food_form = FoodForm(request.POST, request.FILES)
        image_form = ImageFormSet(request.POST, request.FILES, queryset=Image.objects.none())

        if food_form.is_valid() and image_form.is_valid():
            new_food = food_form.save(commit=False)
            new_food.save()

            for food_form in image_form.cleaned_data:
                if food_form:
                    image = food_form['image']

                    new_image = Image(food=new_food, image=image)
                    new_image.save()

            return render(request, 'food_add.html', {
                'categories': FoodCategory.objects.all(),
                'food_form': FoodForm(),
                'image_form': ImageFormSet(queryset=Image.objects.none()),
                'success': True
            })

        else:
            return render(request, 'food_add.html', {
                'categories': FoodCategory.objects.all(),
                'food_form': FoodForm(),
                'image_form': ImageFormSet(queryset=Image.objects.none()),
            })

    else:
        return render(request, 'food_add.html', {
            'categories': FoodCategory.objects.all(),
            'food_form': FoodForm(),
            'image_form': ImageFormSet(queryset=Image.objects.none()),
        })

@login_required
def food_edit_view(request, food_id):
    '''
    It allows the admin to edit a food item
    '''

    food = get_object_or_404(Food, pk=food_id)

    if request.method == 'POST':
        # Handle the form submission for editing the food item
        form = FoodForm(request.POST, instance=food)
        if form.is_valid():
            form.save()
            return redirect('food_details', food_id=food_id)  # Redirect to food details page
    else:
        # Create a form pre-populated with the existing food item data
        form = FoodForm(instance=food)

    return render(request, 'food_edit.html', {
        'food': food,
        'form': form,
    })

@login_required
@permission_required('foodtracker.delete_food')
def food_delete_view(request, food_id):
    '''
    Allows admin users to delete a food item
    '''
    food = Food.objects.get(id=food_id)

    if request.method == 'POST':
        food.delete()
        return redirect('food_list')

    return render(request, 'food_delete.html', {
        'categories': FoodCategory.objects.all(),
        'food': food,
    })

@login_required
def food_log_view(request):
#     '''
#     It allows the user to select food items and
#     add them to their food log
#     '''
#     total_calories = 0
#     total_protein = 0
#     total_carbohydrates = 0
#     total_fat = 0
#
#     if request.method == 'POST':
#         foods = Food.objects.all()
#         selected_food_names = request.POST.getlist('food_consumed')
#
#         # Get the selected food items by name
#         selected_foods = Food.objects.filter(food_name__in=selected_food_names)
#
#         # Calculate the total nutritional value
#         total_calories = sum(selected_food.calories for selected_food in selected_foods)
#         total_protein = sum(selected_food.protein for selected_food in selected_foods)
#         total_carbohydrates = sum(selected_food.carbohydrates for selected_food in selected_foods)
#         total_fat = sum(selected_food.fat for selected_food in selected_foods)
#
#         # You can save the total nutritional values to the user's profile or display them as needed.
#
#     # GET method
#     else:
#         foods = Food.objects.all()
#         # Rest of your code for displaying food items and processing the form.
#
#     return render(request, 'food_log.html', {
#         'categories': FoodCategory.objects.all(),
#         'foods': foods,
#         'title': 'Food Log',
#         'total_calories': total_calories,
#         'total_protein': total_protein,
#         'total_carbohydrates': total_carbohydrates,
#         'total_fat': total_fat,
#     })

    if request.method == 'POST':
        foods = Food.objects.all()

        # get the food item selected by the user
        food = request.POST['food_consumed']
        food_consumed = Food.objects.get(food_name=food)

        # get the currently logged in user
        user = request.user

        # add selected food to the food log
        food_log = FoodLog(user=user, food_consumed=food_consumed)
        food_log.save()

    else:  # GET method
        foods = Food.objects.all()

    # get the food log of the logged in user
    user_food_log = FoodLog.objects.filter(user=request.user)

    return render(request, 'food_log.html', {
        'categories': FoodCategory.objects.all(),
        'foods': foods,
        'user_food_log': user_food_log
    })


@login_required
def food_log_delete(request, food_id):
    '''
    It allows the user to delete food items from their food log
    '''
    # get the food log of the logged in user
    food_consumed = FoodLog.objects.filter(id=food_id)

    if request.method == 'POST':
        food_consumed.delete()
        return redirect('food_log')

    return render(request, 'food_log_delete.html', {
        'categories': FoodCategory.objects.all()
    })


@login_required
def weight_log_view(request):
    '''
    It allows the user to record their weight
    '''
    if request.method == 'POST':

        # get the values from the form
        weight = request.POST['weight']
        entry_date = request.POST['date']

        # get the currently logged in user
        user = request.user

        # add the data to the weight log
        weight_log = Weight(user=user, weight=weight, entry_date=entry_date)
        weight_log.save()

    # get the weight log of the logged in user
    user_weight_log = Weight.objects.filter(user=request.user)

    return render(request, 'user_profile.html', {
        'categories': FoodCategory.objects.all(),
        'user_weight_log': user_weight_log
    })


@login_required
def weight_log_delete(request, weight_id):
    '''
    It allows the user to delete a weight record from their weight log
    '''
    # get the weight log of the logged in user
    weight_recorded = Weight.objects.filter(id=weight_id)

    if request.method == 'POST':
        weight_recorded.delete()
        return redirect('weight_log')

    return render(request, 'weight_log_delete.html', {
        'categories': FoodCategory.objects.all()
    })


def categories_view(request):
    '''
    It renders a list of all food categories
    '''
    return render(request, 'categories.html', {
        'categories': FoodCategory.objects.all()
    })


def category_details_view(request, category_name):
    '''
    Clicking on the name of any category takes the user to a page that
    displays all of the foods in that category
    Food items are paginated: 4 per page
    '''
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    category = FoodCategory.objects.get(category_name=category_name)
    foods = Food.objects.filter(category=category)

    for food in foods:
        food.image = food.get_images.first()

    # Show 4 food items per page
    page = request.GET.get('page', 1)
    paginator = Paginator(foods, 4)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)

    return render(request, 'food_category.html', {
        'categories': FoodCategory.objects.all(),
        'foods': foods,
        'foods_count': foods.count(),
        'pages': pages,
        'title': category.category_name
    })