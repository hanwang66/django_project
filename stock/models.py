from django.db import models

class Stock(models.Model):
	code = models.CharField(max_length=20)
	name = models.CharField(max_length=50)
	price = models.CharField(max_length=20)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"{self.name} ({self.code})"
