# models.py
from django.db import models
from django.db.models import JSONField


class MainPage(models.Model):
    language_choices = [
        ('english', 'English'),
        ('arabic', 'العربيّة'),
    ]

    language = models.CharField(max_length=20, choices=language_choices)
    documents = JSONField()


class SearchPageModel(models.Model):
    retrieval_models_choices = [
        ('boolean', 'Boolean Model'),
        ('extended_boolean', 'Extended Boolean Model'),
        ('vector', 'Vector Model'),
    ]

    retrieval_model = models.CharField(max_length=20, choices=retrieval_models_choices)
    query = models.CharField(max_length=255)

