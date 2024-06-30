from django import forms
from .models import MainPage, SearchPageModel


class MainPageForm(forms.ModelForm):
    class Meta:
        model = MainPage
        fields = ['language', 'documents']


class SearchPageForm(forms.ModelForm):
    class Meta:
        model = SearchPageModel
        fields = ['retrieval_model', 'query']
