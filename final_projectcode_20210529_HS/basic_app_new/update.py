from django import forms
from basic_app_new.models import *

class UpdateFood(forms.ModelForm):
    class Meta:
        model = Food_diary_new
        fields = '__all__'