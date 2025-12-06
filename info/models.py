from django.db import models

class Info(models.Model):
	name = models.CharField(max_length=50)
	email = models.EmailField()
	message = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name
