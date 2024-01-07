from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=False)
    description = models.TextField()
    date = models.DateField()
    # repeat
    done = models.BooleanField(default=False)

    # sort by date

    def __str__(self): return self.name + ' | ' + str(self.user)