from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string

class Repair(models.Model):

    status_choices = [
        ('Submitted', 'Submitted'),
        ('Processing', 'Processing'),
        ('Under Review', 'Under Review'),
        ('Waiting For Parts', 'Waiting For Parts'),
        ('Complete', 'Complete'),
    ]

    urgency_choices = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High')
    ]

    suNumber = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Student Number")
    repairTitle = models.CharField(max_length=100, verbose_name='Issue Title')
    repairDescription = models.TextField(verbose_name='Issue Description')
    repairStatus = models.CharField(max_length=20, default='SUB', verbose_name='Issue Status', choices=status_choices)
    repairLocation = models.CharField(max_length=100, verbose_name='Issue Location')
    dateLogged = models.DateField(default = timezone.now)
    repairImage = models.ImageField(upload_to='repair_images', blank=True, verbose_name='Issue Evidence', default='default.jpg')
    repairUrgency = models.CharField(max_length=20, default='Low', verbose_name='Issue Urgency', choices=urgency_choices)

    def __str__(self):
        return self.repairTitle
    
    def get_absolute_url(self):
        return reverse('repair-detail', kwargs={'pk': self.pk})

class Feedback(models.Model):

    rating_choices=[
        ('1 Star', '1 Star'),
        ('2 Stars', '2 Stars'),
        ('3 Stars', '3 Stars'),
        ('4 Stars', '4 Stars'),
        ('5 Stars', '5 Stars'),
    ]

    time_choices = [
        ('Longer Than Expected', 'Longer Than Expected'),
        ('Reasonable Amount Of Time', 'Reasonable Amount Of Time'),
        ('Promptly Resolved', 'Promptly Resolved'),
    ]

    problemDescription = models.CharField(verbose_name='Problem Description', max_length=100)
    problemLink = models.CharField(verbose_name='Link To Problem (only part after .com)', max_length=100, default='None')
    resolutionDescription = models.CharField(verbose_name='Resolution Description (if any)', max_length=100)
    feedbackTime = models.CharField(verbose_name='Timeliness of Resolution', choices=time_choices, max_length=100)
    feedbackCommunication = models.CharField(verbose_name='Rate Our Communication', choices=rating_choices, max_length=100)
    feedbackOverallSatisfaction = models.CharField(verbose_name='Your Overall Satisfaction', choices=rating_choices, max_length=100)
    feedbackAdditional = models.TextField(verbose_name=' Any Additional Comments')

    def __str__(self):
        return self.problemDescription