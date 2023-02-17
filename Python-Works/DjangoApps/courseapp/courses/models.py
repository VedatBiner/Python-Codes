from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField

class Category(models.Model):
    name = models.CharField(max_length=40)
    slug = models.SlugField(default="", null=False,unique=True,db_index=True, max_length=50)

    def __str__(self):
        return f"{self.name}"

class Course(models.Model):
    title = models.CharField(max_length=50)
    subtitle = models.CharField(max_length=100, default="")
    description = RichTextField()
    image = models.ImageField(upload_to="images",default="")
    date= models.DateField(auto_now=True)
    isActive = models.BooleanField(default=False)
    isHome = models.BooleanField(default=False)
    slug = models.SlugField(default="",blank=True,null=False, unique=True, db_index=True) 
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return f"{self.title}"

class UploadModel(models.Model):
    image = models.ImageField(upload_to="images")

class Slider(models.Model):
    tittle = models.CharField(max_length=100)
    image = models.ImageField(upload_to="images")
    isActive = models.BooleanField(default=False)
    # bire çok ilişki kuralım, ilişkili kursa gitsin
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True) 

   # def __str__(self):
    #    return f"{self.title}"

