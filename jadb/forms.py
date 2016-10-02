from django import forms
from maakdenbosch.models import Entiteitsoort, Tag

class SearchForm(forms.Form):
    soort = forms.ModelChoiceField(queryset=Entiteitsoort.objects.all(), required=False)
    query = forms.CharField(required=False)
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.filter(groep__naam='Cultuur categorie'), widget=forms.CheckboxSelectMultiple, required=False)
