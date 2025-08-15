from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    if created:
        user_group, _ = Group.objects.get_or_create(name='User')
        instance.groups.add(user_group)
        
        if instance.email:
            token = default_token_generator.make_token(instance)
            activation_path = reverse('activate-user', args=[instance.id, token])  # Use your actual URL name
            activation_url = f"{settings.FRONTEND_URL}{activation_path}"

            subject = 'Activate Your Account'
            message = (
                f'Hi {instance.username},\n\n'
                f'Please activate your account by clicking the link below:\n'
                f'{activation_url}\n\nThank You!'
            )
            recipient_list = [instance.email]
            try:
                send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
                print("done")
            except Exception as e:
                print(f"Failed to send email to {instance.email}: {str(e)}")
