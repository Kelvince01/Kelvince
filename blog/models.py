from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models.fields import TextField
from django.forms import forms
from django.forms.widgets import MediaDefiningClass
from django.template.defaultfilters import slugify
from taggit.managers import TaggableManager

STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

class Category(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")
    title = models.CharField(max_length=255, verbose_name="Title", unique=True)
    slug = models.SlugField(unique=True, null=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['title']

    def save(self, *args, **kwargs):
                # Uncomment if you don't want the slug to change every time the name changes
                #if self.id is None:
                        #self.slug = slugify(self.name)
                self.slug = slugify(self.title)
                super(Category, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

class Article(models.Model):
    thumbnail = models.ImageField(upload_to='photos/%Y/%m/%d')
    title = models.CharField(max_length=200, verbose_name="Title", unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.CharField(max_length=400, null=True)
    category = models.ForeignKey(Category, verbose_name="Category", on_delete=models.CASCADE, null=True, related_name='articles')
    tags = TaggableManager()
    author = models.ForeignKey(User, on_delete= models.CASCADE,related_name='articles')
    updated_on = models.DateTimeField(auto_now= True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    views = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        ordering = ['-created_on']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Article, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("article", kwargs={"slug": str(self.slug)})

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

class Comment(models.Model):
    post = models.ForeignKey(Article,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)

class Author(models.Model):
    avatar = models.ImageField(upload_to='authors/%Y/%m/%d')
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    join_date = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        ordering = ['join_date']

    def __str__(self):
        return self.name

class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    message = TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return self.name