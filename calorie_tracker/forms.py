from django import forms
from django.contrib.auth.models import User
from .models import Food , BMIResult


class ContactForm(forms.Form):
    fullname = forms.CharField(max_length=50)
    subject = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=150)
    message = forms.CharField(widget=forms.Textarea, max_length=2000)




class BMICalculatorForm(forms.ModelForm):
    age = forms.IntegerField()

    class Meta:
        model = BMIResult
        fields = ('weight', 'height', 'age')



class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = '__all__'

        

class ConsumedForm(forms.Form):
    food = forms.ModelChoiceField(queryset=Food.objects.all())
    servings = forms.IntegerField()


class RecipeSearchForm(forms.Form):
    ingredients = forms.CharField(label='Ingredients', max_length=255)
