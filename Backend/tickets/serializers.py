from rest_framework import serializers
from .models import Ticket, Attachment

from django.db import transaction

from django.contrib.auth import get_user_model

import os
from django.core.exceptions import ValidationError


CustomUser = get_user_model()

ALLOWED_EXTENSIONS = [
    # documents
    '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.txt',

    # images
    '.jpg', '.jpeg', '.png', '.gif', '.webp',

    # videos
    '.mp4', '.mov', '.avi', '.mkv'
]

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

import os
from django.core.exceptions import ValidationError

def validate_file(file):
    # ✅ Extension check
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValidationError(f"Unsupported file type: {ext}")

    # ✅ Size check
    if file.size > MAX_FILE_SIZE:
        raise ValidationError("File size exceeds 10MB limit.")
    



class MiniUserSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    class Meta:
        model = CustomUser
        fields=['id','username','profile_pic']






class TicketListUserSerializer(serializers.ModelSerializer):
    id = serializers.CharField()

    assigned_to = MiniUserSerializer(read_only=True)
    created_by = MiniUserSerializer(read_only=True)

    # 🔹 Latest status & priority
    status = serializers.SerializerMethodField()
    priority = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = [
            'id',
            'title',
            'created_by',
            'assigned_to',
            'status',
            'priority',
            'created_at',
            'is_deleted',
            'deleted_by',
        ]
        read_only_fields = ['created_at']

    # 🔹 Get latest status
    def get_status(self, obj):
        latest = obj.status_history.order_by('-updated_at').first()
        return latest.status if latest else None

    # 🔹 Get latest priority
    def get_priority(self, obj):
        latest = obj.status_history.order_by('-updated_at').first()
        return latest.priority if latest else None

    # 🔥 Remove fields dynamically based on role
    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        user = request.user

        # ❌ Hide deleted info for normal users
        if not (user.is_staff or user.is_superuser):
            data.pop('is_deleted', None)
            data.pop('deleted_by', None)

        # ❌ Remove assigned_to if null
        if data.get('assigned_to') is None:
            data.pop('assigned_to', None)

        return data





class TicketCreateSerializer(serializers.ModelSerializer):
    attachments = serializers.ListField(
       child=serializers.FileField(validators=[validate_file]),  # ✅ HE
        write_only=True,
        required=False
    )

    class Meta:
        model = Ticket
        fields = ['title', 'description', 'attachments']
        extra_kwargs = {
            'title': {'required': False}  # 👈 make it optional globally first
        }



    def create(self, validated_data):
        request = self.context.get('request')
        attachments = validated_data.pop('attachments', [])

        # 🔥 Atomic transaction (ALL or NOTHING)
        with transaction.atomic():

            # 1. Create ticket
            ticket = Ticket.objects.create(
                **validated_data,
                created_by=request.user,
                ticket_type=None
            )

            # 2. Create attachments
            attachment_objs = []
            for file in attachments:
                attachment_objs.append(
                    Attachment(
                        file=file,
                        uploaded_by=request.user,
                        ticket=ticket
                    )
                )

            # Bulk create (faster)
            Attachment.objects.bulk_create(attachment_objs)

        return ticket
    

    def to_representation(self, instance):
        return {
            "ticket_id": instance.id
        }