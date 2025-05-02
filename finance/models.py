# finance/models.py

from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default="No description")

    def __str__(self):
        return self.name

class Expense(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField()

    def __str__(self):
        return f"{self.category.name} - {self.amount}"
