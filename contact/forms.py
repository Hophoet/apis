#
from django import forms
from django.forms.utils import ErrorList

class AddContactForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    phone_number = forms.CharField()
    company = forms.JSONField()

    def clean_company(self, *args, **kwargs):
        company = self.cleaned_data.get('company')
        name = company['name']
        if name and len(company) == 1:
            return company
        raise forms.ValidationError('Enter a valid JSON.')



#paragraph error list class creation
class AddContactError(ErrorList):
    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self: return ''
        errors_json = [error for error in self]
        return str(errors_json)
