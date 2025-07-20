from django.db import models

# Create your models here.
from django.db import models
import json

class ContentProject(models.Model):
    """Main project containing all topics and metadata"""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    pdf_file = models.FileField(upload_to='pdfs/', null=True, blank=True)
    raw_text = models.TextField(blank=True)
    metadata = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('processing', 'Processing'),
            ('completed', 'Completed'),
            ('failed', 'Failed'),
        ],
        default='pending'
    )

    def __str__(self):
        return self.name

class Topic(models.Model):
    """Topics within a project"""
    project = models.ForeignKey(ContentProject, on_delete=models.CASCADE, related_name='topics')
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"{self.project.name} - {self.title}"

class Session(models.Model):
    """Sessions within a topic"""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='sessions')
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"{self.topic.title} - {self.title}"

class Episode(models.Model):
    """Episodes within a session"""
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='episodes')
    title = models.CharField(max_length=200)
    description = models.TextField()
    script = models.TextField(blank=True)
    duration_minutes = models.IntegerField(null=True, blank=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"{self.session.title} - {self.title}"

class ProcessingLog(models.Model):
    """Log processing steps and errors"""
    project = models.ForeignKey(ContentProject, on_delete=models.CASCADE, related_name='logs')
    step = models.CharField(max_length=100)
    message = models.TextField()
    level = models.CharField(
        max_length=10,
        choices=[('info', 'Info'), ('warning', 'Warning'), ('error', 'Error')],
        default='info'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']