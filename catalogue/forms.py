from django import forms

from .models import Resource


class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = [
            "title",
            "description",
            "resource_type",
            "file",
            "country",
            "year",
            "projects",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "projects": forms.CheckboxSelectMultiple(),
        }

