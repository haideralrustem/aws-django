from django import forms




# .........
class UploadedDataFormHandler(forms.Form):
    text_value = forms.CharField(widget = forms.HiddenInput(),
                                    required=False, initial=False)

    param1 = forms.CharField(widget = forms.HiddenInput(), max_length=20,
                                    required=False, initial=False)
    param2 = forms.CharField(widget = forms.HiddenInput(), max_length=20,
                                    required=False, initial=False)
    param3 = forms.CharField(widget = forms.HiddenInput(), max_length=20,
                                    required=False, initial=False)