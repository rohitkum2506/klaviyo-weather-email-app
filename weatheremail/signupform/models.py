from django.db import models
from django.core.exceptions import ValidationError
from cities import cities as cit
import csv

# Create your models here.

class WeatherSubscription(models.Model):
	email = models.EmailField(unique=True)
	cit = sorted(cit)
	location = models.CharField(max_length=100, choices=cit)
	
	def __str__(self):
		return str(self.email) + ',' + str(self.location)