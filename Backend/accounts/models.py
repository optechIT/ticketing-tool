from django.db import models

from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import AbstractUser

from uuid import uuid4
import os


from TicketingTool.utils.snowflake_id_generator import SnowflakeIDGenerator

snowflake_id_acc_obj = SnowflakeIDGenerator()


@deconstructible
class UploadProfilePicRename(object):
    def __init__(self, path):
        self.sub_path = path

    def __call__(self, instance, filename, *args,**kwargss):
        try:
            ext = filename.split('.')[-1]
            userID = instance.pk if instance.pk else 'default_profile_pic'

            filename = f"IMG{uuid4().hex}.{ext}"

            return os.path.join(self.sub_path, str(userID), filename)
        
        except  Exception as E:
            raise ValidationError(f'Error generating file path : {str(E)}')

class CustomUser(AbstractUser):

    # ✅ Gender choices
    class GenderChoices(models.TextChoices):
        MALE = "M", "Male"
        FEMALE = "F", "Female"
        OTHER = "O", "Other"

    id = models.BigIntegerField(primary_key=True, editable=False, unique=True)

    username = models.CharField(max_length=200, unique=True)

    email = models.EmailField()

    # ✅ Profile picture
    profile_pic = models.ImageField(
        upload_to=UploadProfilePicRename("profile_pics/"),
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])],
        blank=True,
        null=True
    )

    # ✅ Phone number (universal format)
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Include country code e.g. +919876543210"
    )

    

    gender = models.CharField(
        max_length=1,
        choices=GenderChoices.choices,
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)  # set once on create
    updated_at = models.DateTimeField(auto_now=True)      # updates on every save


    def save(self, *args, **kwargs):
        if not self.id:
            self.id = snowflake_id_acc_obj.generate_id()
        
        self.full_clean()

        return super().save()

    def __str__(self):
        return self.username
    

    