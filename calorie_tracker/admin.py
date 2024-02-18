from django.contrib import admin
from .models import Food  ,  Consume , Intake
from .models import BMIResult

class BMIResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'weight', 'height', 'category', 'age', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('user__username', 'category')
    ordering = ('-created_at',)

admin.site.register(BMIResult, BMIResultAdmin)

class FoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'calories')

class IntakeAdmin(admin.ModelAdmin):
    list_display = ('user', 'date')

class ConsumeAdmin(admin.ModelAdmin):
    list_display = ('intake', 'food_consumed')

admin.site.register(Food, FoodAdmin)
admin.site.register(Intake, IntakeAdmin)
admin.site.register(Consume, ConsumeAdmin)





from .models import Category, Recipe

class RecipeAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    list_filter = ['category']
    search_fields = ['name', 'category__name']

admin.site.register(Category)
admin.site.register(Recipe, RecipeAdmin)








