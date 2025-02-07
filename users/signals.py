import logging
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User,Group
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)

@receiver(post_save, sender=User, weak=False)
def send_activation_email(sender, instance, created, **kwargs):
    if created and instance.email:
        token = default_token_generator.make_token(instance)
        activation_url = f"{settings.FRONTEND_URL}/users/activate/{instance.id}/{token}"

        subject = "Activate Your Account"
        message = f"Hi {instance.username},\n\nPlease activate your account by clicking the link below:\n{activation_url}\n\nThank you!"
        recipient_list = [instance.email]

        try:
            send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
        except Exception as e:
            logger.error(f"Failed to send email to {instance.email}: {str(e)}")


@receiver(post_save, sender=User)
def assign_user_role(sender, instance, created, **kwargs):
    if created:
        default_group = Group.objects.get(name="Participant") 
        instance.groups.add(default_group)
        