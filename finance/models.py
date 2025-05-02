# finance/models.py


from django.db import models
from django.contrib.auth.models import User


class Entry(models.Model):
   TYPE_CHOICES = (
       ('Income', 'Income'),
       ('Expense', 'Expense'),
   )


   CATEGORY_CHOICES = (
       ('Food', 'Food'),
       ('Bill', 'Bill'),
       ('Travel', 'Travel'),
       ('Health', 'Health'),
       ('Personal', 'Personal'),
       ('Debt', 'Debt'),
       ('Miscellaneous', 'Miscellaneous'),
   )


   user = models.ForeignKey(User, on_delete=models.CASCADE)
   title = models.CharField(max_length=100)
   amount = models.DecimalField(max_digits=10, decimal_places=2)
   date = models.DateField()
   type = models.CharField(max_length=10, choices=TYPE_CHOICES)
   category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, blank=True, default="")
   notes = models.TextField(blank=True)


   def __str__(self):
       return f"{self.title} ({self.type}): {self.amount}"