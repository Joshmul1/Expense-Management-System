from datetime import timezone

from django.db import models


# Create your models here.

# class Expenses(models.Model):
#     name = models.CharField(max_length=200)
#
#     def __str__(self):
#         return self.name

class Category(models.Model):
    category_name = models.CharField(primary_key=True, max_length=20)


class Expense(models.Model):
    name = models.CharField("Name of receipt", blank=True, max_length=20)
    date = models.DateField("Date of receipt", blank=True)
    time = models.TimeField("Time of receipt", blank=True)
    price = models.FloatField(max_length=10, blank=True)
    # TODO Change the default image
    image = models.ImageField(upload_to='images/', default="PLEASE FIX ME")
    has_been_changed = models.BooleanField(default=False)
    has_been_paid = models.BooleanField(default=False)
    category_name = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default=None, blank=True)


class Todo(models.Model):
    text = models.CharField("What do you need to do?", max_length=1000)
