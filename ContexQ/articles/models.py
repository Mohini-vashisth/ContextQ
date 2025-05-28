from django.db import models

class Article(models.Model):
    title = models.TextField()
    published = models.CharField(max_length=100)
    source = models.CharField(max_length=200)
    summary = models.TextField(blank=True, null=True)
    link = models.URLField(unique=True)
    country = models.CharField(max_length=100)
    language = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.title} [{self.country}]"