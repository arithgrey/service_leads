from django.db import models

class LeadType(models.Model):
    name = models.CharField(max_length=100)
    status = models.IntegerField(default=1)

    def __str__(self):
        return self.name