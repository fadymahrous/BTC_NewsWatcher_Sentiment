from django.db import models

class news_healines(models.Model):
    title = models.CharField(max_length=1000)
    details = models.TextField()
    published_on = models.DateTimeField()
    source=models.CharField(max_length=100)
    hexenmeinung= models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.title} ({self.published_on})"
