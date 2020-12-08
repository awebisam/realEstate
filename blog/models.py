from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.


class BlogManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(published=True)


class Blog(models.Model):

    image = models.ImageField(upload_to="blog/%Y/%m/%d", blank=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    author = "Admin"
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    body = models.TextField()
    published = models.BooleanField(default=False)
    objects = models.Manager()
    blogs = BlogManager()
    seodescription = models.TextField()

    def save(self, *args, **kwargs):
        self.slug = slugify(f'{self.id}-{self.title}')
        super(Blog, self).save(*args, **kwargs)  # Call the real save() method

    class Meta:
        verbose_name = "Blog"
        verbose_name_plural = "Blogs"
        ordering = ['-created_on']

    def __str__(self):
        return self.title
