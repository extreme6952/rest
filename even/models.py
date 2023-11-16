from typing import Any
from django.db import models

from django.contrib.auth.models import User
from django.db.models.query import QuerySet

from django.utils import timezone

from django.urls import reverse


class PublishedManager(models.Manager):

    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(status=Event.Status.PUBLISHED)
    

    
class Event(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DF','Draft'
        PUBLISHED = 'PB','Published'

    title = models.CharField(max_length=250)

    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    
    body = models.TextField()

    author = models.ForeignKey(User,on_delete=models.CASCADE,
                               related_name='events')
    
    publish = models.DateTimeField(default = timezone.now)

    created = models.DateTimeField(auto_now_add=True)

    updated = models.DateTimeField(auto_now=True)

    status = models.CharField(max_length=2,choices=Status.choices,
                              default=Status.DRAFT)
    
    published = PublishedManager()

    objects = models.Manager()
    
    
    class Meta:
        ordering = ['-publish']
        
        indexes = [
            models.Index(fields=['-publish'])
        ]
        
    
    def __str__(self):
        return self.title
    

    def get_absolute_url(self):

        return reverse('event:event_detail',args=[self.publish.year,
                                                  self.publish.month,
                                                  self.publish.day,
                                                  self.slug])
    









class Comment(models.Model):

    event = models.ForeignKey(Event,on_delete=models.CASCADE,
                              related_name='comments')
    
    name = models.CharField(max_length=85)

    email = models.EmailField()

    body = models.TextField()

    created = models.DateTimeField(auto_now_add=True)

    updated = models.DateTimeField(auto_now=True)

    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        
        indexes = [
            models.Index(fields=['created'])
        ]

    def __str__(self):

        return f"comment {self.name} by {self.event}"