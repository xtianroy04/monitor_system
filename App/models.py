from django.db import models
from datetime import date

class Attendee(models.Model):
    YES_NO_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.TextField()
    is_adventist = models.CharField(max_length=3, choices=YES_NO_CHOICES, default='No')
    age = models.IntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Attendance(models.Model):
    attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    status = models.CharField(max_length=10, default='Present') 

    def __str__(self):
        return f'{self.attendee} - {self.date} - {self.status}'
