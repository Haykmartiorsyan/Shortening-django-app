from django import forms
from .validators import validate_dot_com, validate_url


class SubmitUrlForm(forms.Form):
    url = forms.CharField(validators=[validate_url, validate_dot_com],
                          widget=forms.TextInput(
                              attrs={
                                  'placeholder': 'Long URL',
                                  'class': 'form-control'
                              }
                          ))

    # def clean(self):
    #     cleaned_data = super(SubmitUrlForm, self).clean()
    #     print(cleaned_data)
    #     url = cleaned_data.get('url')
    #     # print(url)
    #     url_validator = URLValidator()
    #     try:
    #         url_validator(url)
    #     except:
    #         raise forms.ValidationError('Inavalid field')
    #     return url
    #
    # def clean_url(self):
    #     url = self.cleaned_data['url']
    #     # print(url)
    #
    #     # url_validator = URLValidator()
    #     # try:
    #     #     url_validator(url)
    #     # except:
    #     #     raise forms.ValidationError('Inavalid field')
    #     return url



