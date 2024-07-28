from django.db import models
from django.contrib.auth.models import User

class Alert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cryptocurrency = models.CharField(max_length=10)
    target_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.cryptocurrency} at {self.target_price}"
