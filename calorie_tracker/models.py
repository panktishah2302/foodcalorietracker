from django.db import models
from django.contrib.auth.models import User 
from django.utils import timezone
from decimal import Decimal, InvalidOperation
from django.core.exceptions import ValidationError







# Create your models here.



class Food(models.Model):
    name= models.CharField(max_length=255, db_index=True)
    carbs = models.FloatField()
    protein = models.FloatField()
    fats = models.FloatField()
    calories = models.IntegerField()
    
    def __str__(self):
        return self.name
    
class Intake(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    # Add any other fields related to daily intake here

    def __str__(self):
        return f"{self.user.username}'s intake on {self.date}"

class Consume(models.Model):
    intake = models.ForeignKey(Intake, on_delete=models.CASCADE)
    food_consumed = models.ForeignKey(Food, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # object is being created, set user to current user
            self.user = self.intake.user
        super().save(*args, **kwargs)




    
import datetime

class BMIResult(models.Model):
    

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    weight = models.FloatField()
    height = models.FloatField()
    category = models.CharField(max_length=50)
    age = models.IntegerField()
    created_at = models.DateTimeField( null=True, blank=True, default=datetime.datetime.now)
    
    def calculate_bmi(self):
        return self.weight / (self.height ** 2)

    

    def get_ideal_weight(self):
        ideal_min = 18.5 * (self.height ** 2)
        ideal_max = 24.9 * (self.height ** 2)
        if ideal_min < 46:
            ideal_min = 46
        if ideal_max > 61:
            ideal_max = 61
        return f"{ideal_min:.1f} to {ideal_max:.1f} kilograms"



class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    photo=models.ImageField(upload_to='images/' , null=True)
    ingredients = models.TextField(default='')
    description = models.TextField(default='')
    Nutrition=models.TextField(max_length=2000 , null=True)
    Method=models.TextField(max_length=2000 , null=True)

    def __str__(self):
        
        return self.name
    








    

   
