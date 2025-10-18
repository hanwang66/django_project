from django.db import models

class RealEstate(models.Model):
    community = models.CharField(max_length=100)
    area = models.FloatField()
    city = models.CharField(max_length=50)
    floor = models.CharField(max_length=10)
    price = models.FloatField(blank=True, default=0)
    date = models.CharField(max_length=20, blank=True, default='')

    def __str__(self):
        return f"{self.community} - {self.city}"
