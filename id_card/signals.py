from django.db.models.signals import post_save
from django.dispatch import receiver
from info.models import StudentCreate
from .models import StudentIdCard

@receiver(post_save, sender=StudentCreate)
def create_student_id_card(sender, instance, created, **kwargs):
    if created:
        StudentIdCard.objects.create(student=instance)