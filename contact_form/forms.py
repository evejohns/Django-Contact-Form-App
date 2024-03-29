from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms
from .models import Snippet
from django.core.validators import RegexValidator 

class NameWidget(forms.MultiWidget):

    def __init__(self, attrs=None):
        super().__init__([
            forms.TextInput(),
            forms.TextInput()
        ], attrs)

    def decompress(self, value):
         # 'firstvalue' 'secondvalue'
        if value:
            return value.split(' ')
        # ['firstvalue', 'secondvalue]
        return ['','']        

class NameField(forms.MultiValueField):

    widget = NameWidget
    def __init__(self, *args, **kwargs):

        fields = (
            forms.CharField(validators=[
                RegexValidator(r'[a-zA-Z]+','Enter a valid first name (only letters)')
            ]), #test
            forms.CharField(validators=[
                RegexValidator(r'[a-zA-Z]+','Enter a valid last name (only letters)')
            ]) #none
        )

        super().__init__(fields, *args, **kwargs)
    
    def compress(self, data_list):
        # data_list = ['test','none']
        # data_list = ['firstvalue','secondvalue']
        # return f'{data_list[0]} {data_list[1]}'
        return f'{data_list[0]} {data_list[1]}'
        # 'firstvalue secondvalue'


class ContactForm(forms.Form):
    name = NameField()
    email = forms.EmailField(label = 'E-mail')
    category = forms.ChoiceField(choices = [('question','Question'), ('other','Other')])
    subject = forms.CharField(required = False)
    body = forms.CharField(widget = forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'name',
            'email',
            'category',
            'subject',
            'body',
            Submit('submit','Submit',css_class='btn-success')
        )


class SnippetForm(forms.ModelForm):
    class Meta:
        model = Snippet
        fields = ('name', 'body')