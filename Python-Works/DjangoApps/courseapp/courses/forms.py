from django import forms
from courses.models import Course
from django.forms import SelectMultiple, TextInput, Textarea

class CourseCreateForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ("title", "description", "image", "slug")
        labels = {
            "title" : "Kurs Başlığı",
            "description" : "Açıklama",
        }
        widgets = {
            "title" : TextInput(attrs={"class":"form-control"}),
            "description" : Textarea(attrs={"class":"form-control"}),
            "slug" : TextInput(attrs={"class":"form-control"}),
        }
        erro_messages = {
            "title" : {
                'required' : "Kurs Başlığı Girmelisiniz",
                "max_length" : "maksimum 50 karakter girmelisiniz"
            },
            "description" : {
                'required' : "Kurs açıklması gereklidir",
            }
        }

class CourseEditForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('title','description','image','slug','categories','isActive')
        labels = {
            'title':"kurs başlığı",
            'description':'açıklama'
        }
        widgets = {
            "title": TextInput(attrs={"class":"form-control"}),
            "description": Textarea(attrs={"class":"form-control"}),
            "slug": TextInput(attrs={"class":"form-control"}),
            "categories": SelectMultiple(attrs={"class":"form-control"})
        }
        error_messages = {
            "title": {
                "required":"kurs başlığı girmelisiniz.",
                "max_length": "maksimum 50 karakter girmelisiniz"
            },
            "description": {
                "required":"kurs açıklaması gereklidir."
            }
        }

class UploadForm(forms.Form):
    image = forms.FileField()
    