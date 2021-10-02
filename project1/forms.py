from django import forms
from django.contrib.auth.forms import User
from django.contrib.auth.forms import UserCreationForm
from my_users.models import Profile

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )

# .........
class UploadedDataFormHandler(forms.Form):
    accept_value = forms.CharField(widget = forms.HiddenInput(), max_length=20,
                                    required=False, initial=False)
    # dtype_changes???

class GenericValueForm(forms.Form):
    text_key = forms.CharField(widget = forms.HiddenInput(), max_length=100,
                                    required=False, initial=False)
    text_value = forms.CharField(widget = forms.HiddenInput(), max_length=100,
                                    required=False, initial=False)


class GenericMultichoiceForm(forms.Form):
    def __init__(self, custom_choices, *args, **kwargs):
         super(GenericMultichoiceForm, self).__init__(*args, **kwargs)
         self.fields['choice_field'].choices = custom_choices
    
    choice_field = forms.ChoiceField(choices=(), required=False)
