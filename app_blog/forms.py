from django import forms
from .models import load_image
 
 
class load_image_form(forms.ModelForm):

    class Meta:
        model = load_image
        fields = ['import_something' , 'current_user_username' , 'generated_code']