from django.db import models
from django.contrib.auth.models import User

class NewsItem(models.Model):
    title = models.CharField(max_length=256)
    news = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    
    def __unicode__(self):
        return self.title