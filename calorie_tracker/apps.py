from django.apps import AppConfig


class CalorieTrackerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "calorie_tracker"
    
default_app_config = 'calorie_tracker.apps.CalorieTrackerConfig'
