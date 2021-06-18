from django.db import models
from django.utils import timezone
import datetime

# Create your models here.
class Food_diary_new(models.Model):
    mfg_code = models.CharField(max_length=20,default='PH004')
    Food_id=models.AutoField(primary_key=True)
    food_type=models.CharField(max_length=100,default='food')
    food_name=models.CharField(max_length=200)
    seq_id=models.IntegerField()
    description=models.TextField()
    ss_code=models.CharField(max_length=200)
    carbs=models.CharField(max_length=200)
    protein=models.CharField(max_length=200)
    fat=models.CharField(max_length=200)
    fiber=models.CharField(max_length=200)
    sugar=models.CharField(max_length=200)
    sodium=models.CharField(max_length=200)
    alchohol=models.CharField(max_length=200)
    calorie=models.CharField(max_length=200)
    calorie_saturated_fats=models.CharField(max_length=200)
    image_path=models.URLField()
    def __str__(self):
            return self.food_name

class meal_new(models.Model): 
    meal_type=models.CharField(max_length=50)
    def __str__(self):
        return self.meal_type

class Transaction_det_new(models.Model):
    user_id = models.EmailField()
    date = models.DateField()
    time_rec = models.TimeField()
    quantity = models.IntegerField(default=0)
    meal_type = models.CharField(max_length=25,default='Breakfast')
    mfg_code = models.CharField(max_length=20,default='PH004')
    Food_id=models.AutoField(primary_key=True)
    food_type=models.CharField(max_length=100,default='food')
    food_name=models.CharField(max_length=200)
    carbs=models.CharField(max_length=200)
    protein=models.CharField(max_length=200)
    fat=models.CharField(max_length=200)
    fiber=models.CharField(max_length=200)
    sugar=models.CharField(max_length=200)
    sodium=models.CharField(max_length=200)
    alchohol=models.CharField(max_length=200)
    calorie=models.CharField(max_length=200)
    calorie_saturated_fats=models.CharField(max_length=200)
    ss_code=models.CharField(max_length=200)
    
    

class Temporary_new(models.Model):
    user_id = models.CharField(max_length=100)
    mfg_code = models.CharField(max_length=20,default='PH004')
    quantity = models.IntegerField(default=0)
    meal_type = models.CharField(max_length=25,default='Breakfast')
    Food_id=models.AutoField(primary_key=True)
    food_type=models.CharField(max_length=100,default='food')
    food_name=models.CharField(max_length=200)
    carbs=models.CharField(max_length=200)
    protein=models.CharField(max_length=200)
    fat=models.CharField(max_length=200)
    fiber=models.CharField(max_length=200)
    sugar=models.CharField(max_length=200)
    sodium=models.CharField(max_length=200)
    alchohol=models.CharField(max_length=200)
    calorie=models.CharField(max_length=200)
    calorie_saturated_fats=models.CharField(max_length=200)
    ss_code=models.CharField(max_length=200)
    
    

class Unsaved_new(models.Model):
    user_id = models.CharField(max_length=100)
    date = models.DateField()
    time_rec = models.TimeField()
    quantity = models.IntegerField(default=0)
    meal_type = models.CharField(max_length=25,default='Breakfast')
    mfg_code = models.CharField(max_length=20,default='PH004')
    Food_id=models.AutoField(primary_key=True)
    food_type=models.CharField(max_length=100,default='food')
    food_name=models.CharField(max_length=200)
    carbs=models.CharField(max_length=200)
    protein=models.CharField(max_length=200)
    fat=models.CharField(max_length=200)
    fiber=models.CharField(max_length=200)
    sugar=models.CharField(max_length=200)
    sodium=models.CharField(max_length=200)
    alchohol=models.CharField(max_length=200)
    calorie=models.CharField(max_length=200)
    calorie_saturated_fats=models.CharField(max_length=200)
    ss_code=models.CharField(max_length=200)
    
    


class Purchase_det_new(models.Model):
    user_id = models.CharField(max_length=100)
    date = models.DateField()
    time_rec = models.TimeField()
    quantity = models.IntegerField(default=0)
    mfg_code = models.CharField(max_length=20,default='PH004')
    Food_id=models.AutoField(primary_key=True)
    food_type=models.CharField(max_length=100,default='food')
    food_name=models.CharField(max_length=200)
    carbs=models.CharField(max_length=200)
    protein=models.CharField(max_length=200)
    fat=models.CharField(max_length=200)
    fiber=models.CharField(max_length=200)
    sugar=models.CharField(max_length=200)
    sodium=models.CharField(max_length=200)
    alchohol=models.CharField(max_length=200)
    calorie=models.CharField(max_length=200)
    calorie_saturated_fats=models.CharField(max_length=200)
    ss_code=models.CharField(max_length=200)
    
    


class Temporary_purchase_new(models.Model):
    user_id = models.CharField(max_length=100)
    mfg_code = models.CharField(max_length=20,default='PH004')
    quantity = models.IntegerField(default=0)
    Food_id=models.AutoField(primary_key=True)
    food_type=models.CharField(max_length=100,default='food')
    food_name=models.CharField(max_length=200)
    carbs=models.CharField(max_length=200)
    protein=models.CharField(max_length=200)
    fat=models.CharField(max_length=200)
    fiber=models.CharField(max_length=200)
    sugar=models.CharField(max_length=200)
    sodium=models.CharField(max_length=200)
    alchohol=models.CharField(max_length=200)
    calorie=models.CharField(max_length=200)
    calorie_saturated_fats=models.CharField(max_length=200)
    ss_code=models.CharField(max_length=200)
    
    


class Unsaved_purchase_new(models.Model):
    user_id = models.CharField(max_length=100)
    date = models.DateField()
    time_rec = models.TimeField()
    quantity = models.IntegerField(default=0)
    mfg_code = models.CharField(max_length=20,default='PH004')
    Food_id=models.AutoField(primary_key=True)
    food_type=models.CharField(max_length=100,default='food')
    food_name=models.CharField(max_length=200)
    carbs=models.CharField(max_length=200)
    protein=models.CharField(max_length=200)
    fat=models.CharField(max_length=200)
    fiber=models.CharField(max_length=200)
    sugar=models.CharField(max_length=200)
    sodium=models.CharField(max_length=200)
    alchohol=models.CharField(max_length=200)
    calorie=models.CharField(max_length=200)
    calorie_saturated_fats=models.CharField(max_length=200)
    ss_code=models.CharField(max_length=200)
    
    
