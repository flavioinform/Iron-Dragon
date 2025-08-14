from django.contrib.auth.models import Group
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Profile

@receiver(post_save,sender=Profile)
def add_user_to_default_group(sender, instance, created, **kwargs):
    if created:
        try:
            client=Group.objects.get(name='usuario')
        except Group.DoesNotExist:
            client=Group.objects.create(name='usuario')
            client=Group.objects.create(name='administrador')
        instance.user.groups.add(client)
