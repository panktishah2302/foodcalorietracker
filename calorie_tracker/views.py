from .models import BMIResult
from .forms import BMICalculatorForm
from .forms import FoodForm
from .models import  Food , Intake
from django.shortcuts import render
from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.urls import reverse
from django.views import generic
from .models import Food, Consume
from .models import User
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ContactForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import logout
from bokeh.embed import components
from bokeh.resources import CDN
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io
from io import BytesIO
import base64
from background_task import background
from datetime import datetime, timedelta
from django.db.models.functions import TruncDate
from django.db.models import Avg
from django.views import View
import datetime
from django.db.models import Count
from django.db.models import Sum



import matplotlib
matplotlib.use('Agg')


class IndexView(generic.TemplateView):
    template_name = 'calorie_tracker/index.html'


def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username taken')
                return redirect('calorie_tracker:signup_view')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email taken')
                return redirect('calorie_tracker:signup_view')
            else:
                user = User.objects.create_user(
                    username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
                user.save()
                print('User Created')
                return redirect('calorie_tracker:login')
        else:
            messages.info(request, 'Password not matching.!!')
        return redirect('calorie_tracker:signup_view')
    else:
        return render(request, 'registration/signup.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("calorie_tracker:home1")
        else:
            messages.info(request, 'Invalid Credentiala; Please try again')
            return redirect("calorie_tracker:login")
    else:
        return render(request, 'registration/login.html')


def logout_view(request):
    logout(request)
    messages.info(request, "Successfully Logout")
    return redirect("calorie_tracker:index")


class FoodDeleteView(generic.DeleteView, LoginRequiredMixin):
    model = Food, Consume
    template_name = 'calorie_tracker/delete.html'
    login_url = '/login/'

    def get(self, request, id):
        consumed_food = Consume.objects.get(id=id)
        context = {
            "consumed_food": consumed_food
        }
        return render(request, self.template_name, context)

    def post(self, *args, id):
        consumed_food = Consume.objects.get(id=id)
        consumed_food.delete()
        return redirect(reverse('calorie_tracker:FoodListView'))


def home1(request):
    if request.user.is_authenticated:
        return render(request, 'calorie_tracker/home1.html')
    else:
        return render(request, 'calorie_tracker/home_not_logged_in.html')


class FoodSearchView(generic.ListView):
    model = Food
    template_name = 'calorie_tracker/home1.html'
    context_object_name = 'food_list'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Food.objects.filter(name__icontains=query)
        else:
            return Food.objects.none()


class ThanksView(generic.TemplateView):
    template_name = 'calorie_tracker/thanks.html'


import logging

logger = logging.getLogger(__name__)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            body = {
                'fullname': form.cleaned_data['fullname'],
                'email': form.cleaned_data['email'],
                'message': form.cleaned_data['message'],
            }
            message = "\n".join(body.values())
            try:
                send_mail(subject, message, settings.EMAIL_HOST_USER,['pankti0203@gmail.com'])
            except Exception as e:
                # Log the error for debugging purposes
                logger.error(f"Email sending error: {str(e)}")
                return HttpResponse("Email Not send")
            return redirect("calorie_tracker:ThanksView")
    form = ContactForm()
    return render(request, "calorie_tracker/Contact.html", {'form': form})
 

def result(request):
    template = loader.get_template('calorie_tracker/result.html')
    return HttpResponse(template.render())


import io
import base64
import matplotlib.pyplot as plt
from django.shortcuts import render
from .forms import BMICalculatorForm
from .models import BMIResult

def calculator(request):
    if request.method == 'POST':
        form = BMICalculatorForm(request.POST)
        if form.is_valid():
            weight = form.cleaned_data.get('weight')
            height = form.cleaned_data.get('height')
            age = form.cleaned_data.get('age')

            # Calculate BMI
            bmi = weight / (height ** 2)

            # Determine BMI category based on age
            if age >= 20:
                if bmi < 18.5:
                    category = 'Underweight'
                elif bmi >= 18.5 and bmi < 25:
                    category = 'Normal'
                elif bmi >= 25 and bmi < 30:
                    category = 'Overweight'
                else:
                    category = 'Obese'
            else:
                if bmi < 5:
                    category = 'Underweight'
                elif bmi >= 5 and bmi < 85:
                    category = 'Normal'
                elif bmi >= 85 and bmi < 95:
                    category = 'Overweight'
                else:
                    category = 'Obese'

            # Save BMI result to database
            result = BMIResult(
                user=request.user,
                weight=weight,
                height=height,
                category=category,
                age=age
            )
            result.save()

            

            # Calculate healthy weight range
            min_weight = round(18.5 * (height ** 2), 1)
            max_weight = round(24.9 * (height ** 2), 1)
            if min_weight < 46:
                min_weight = 46
            if max_weight > 61:
                max_weight = 61

            # Render result template with BMI, healthy weight range, and plot
            return render(request, 'calorie_tracker/result.html', {
                'bmi': bmi,
                'category': category,
                'min_weight': min_weight,
                'max_weight': max_weight,
                'weight':weight,
                'height':height,
            })

    else:
        form = BMICalculatorForm()
    return render(request, 'calorie_tracker/bmi.html', {'form': form})











class FoodDetailView(generic.ListView):
    model=Food
    context_object_name='foods'
    template_name="calorie_tracker/FoodDetail.html"
    def get_queryset(self):
        foods = Food.objects.all()
        custom_foods = Food.objects.all()
        queryset = foods & custom_foods
        return queryset



    
from django.utils import timezone

class FoodConsumedView(generic.ListView):
    model = Consume
    template_name = "calorie_tracker/FoodConsumed.html"

    def post(self, request):
        food_consumed_name = request.POST.get("food_consumed")
        food_consumed = Food.objects.get(name=food_consumed_name)
        
        # Check if there's an existing intake object for the current day
        today = timezone.now().date()
        try:
            intake = Intake.objects.get(user=request.user, date=today)
        except Intake.DoesNotExist:
            # If not, create a new one
            intake = Intake(user=request.user, date=today)
            intake.save()
        
        # Add the consumed food to the intake object
        consume = Consume(intake=intake, food_consumed=food_consumed)
        consume.save()
        
        # Get all consumed foods for the current user today
        consumed_food = Consume.objects.filter(intake__user=request.user, intake__date=today)
        
        # Get all foods for the dropdown menu
        foods = Food.objects.all()
        
        context = {
            "consumed_food": consumed_food,
            "foods": foods
        }
        return render(request, self.template_name, context)




        
from django.shortcuts import render, get_object_or_404
from .models import Category, Recipe

def recipe_list(request):
    query = request.GET.get('category')
    if query:
        categories = Category.objects.filter(name__icontains=query)
        recipes = Recipe.objects.filter(category__in=categories)
    else:
        categories = []
        recipes = []
    return render(request, 'calorie_tracker/recipe_list.html', {'categories': categories, 'recipes': recipes})



def recipe_detail(request, category_id, recipe_id):
    category = get_object_or_404(Category, pk=category_id)
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    return render(request, 'calorie_tracker/recipe_detail.html', {'category': category, 'recipe': recipe})





import io
import urllib, base64
from .models import BMIResult

import matplotlib.pyplot as plt
import io
import urllib
import base64



from datetime import datetime, date

from django.utils import timezone

class FoodListView(generic.ListView): 
        model = Food
        template_name="calorie_tracker/FoodConsumed.html" 
        def get(self,request):
                foods=Food.objects.all()
                today = timezone.now().date()
                consumed_food=Consume.objects.filter(user=request.user, intake__date=today)
                context={"consumed_food":consumed_food,'foods': foods} 
                return render(request,self.template_name,context)


from django.http import HttpResponse
from django.utils import timezone
import matplotlib.pyplot as plt
import io
import base64

def weekly_report_view(request):
    # Generate weekly report graph
    start_date = timezone.now().date() - timezone.timedelta(days=6)
    end_date = timezone.now().date()
    consumed_per_day = []
    for i in range(7):
        date = start_date + timezone.timedelta(days=i)
        consumed = Consume.objects.filter(intake__user=request.user, intake__date=date).count()
        consumed_per_day.append(consumed)
    plt.plot(consumed_per_day)
    plt.xlabel('Day of Week')
    plt.ylabel('Foods Consumed')
    plt.yticks(range(max(consumed_per_day) + 1))
    plt.title('Weekly Report')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.clf()
    graph = buf.getvalue()
    response = HttpResponse(content_type='image/png')
    response.write(graph)
    return response

# views.py
from django.shortcuts import render
from django.db.models import Q
from .models import Recipe
from .forms import RecipeSearchForm

def recipe_search(request):
    if request.method == 'POST':
        form = RecipeSearchForm(request.POST)
        if form.is_valid():
            ingredients = form.cleaned_data['ingredients']
            # Split the entered ingredients into a list
            ingredient_list = ingredients.split(',')
            # Query the Recipe model to find matching recipes
            query = Q()
            for ingredient in ingredient_list:
                query &= Q(ingredients__icontains=ingredient.strip())
            recipes = Recipe.objects.filter(query)
            return render(request, 'calorie_tracker/recipe_search.html', {'recipes': recipes})
    else:
        form = RecipeSearchForm()
    return render(request, 'calorie_tracker/recipe_search.html', {'form': form})


def add_custom_food(request):
    if request.method == 'POST':
        form = FoodForm(request.POST)
        if form.is_valid():
            # Process the form data and add the custom food to the database
            food_name = form.cleaned_data['food_name']
            carbs = form.cleaned_data['carbs']
            protein = form.cleaned_data['protein']
            fats = form.cleaned_data['fats']
            calories = form.cleaned_data['calories']
            
            # Create a new CustomFood instance and save it to the database
            custom_food = Food(
                name=food_name,
                carbs=carbs,
                protein=protein,
                fats=fats,
                calories=calories
            )
            custom_food.save()
            
            # Redirect the user to a success page or the food detail page
            return redirect('calorie_tracker:FoodDetail')
    else:
        form = FoodForm()
    
    context = {
        'form': form
    }
    return render(request, 'calorie_tracker/add_custom_food.html', context)
