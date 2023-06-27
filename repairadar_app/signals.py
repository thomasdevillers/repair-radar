from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import Repair

@receiver(post_save, sender=Repair)
def send_repair_status_update(sender, instance, created, **kwargs):
    if instance.repairStatus == 'Complete' and not created:
        # Load the email template and render the dynamic content
        email_template = 'email_template.html'
        email_subject = 'Repair Status Update'
        #email_body = render_to_string(email_template, {'username': instance.user.username, 'repair_id': instance.id})
        email_body = 'The Repair (' + instance.repairTitle +') You Logged on ' + str(instance.dateLogged) + ' Has Been Fixed.'

        # Send the email
        send_mail(email_subject, email_body, 'thomasdevilliers100@gmail.com', [str(instance.suNumber) + '@sun.ac.za'], fail_silently=False)
