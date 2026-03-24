from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.
from django.conf import settings



import uuid
import os

def ticket_attachment_upload_path(instance, filename):
    ext = filename.split('.')[-1]

    # short uuid (8 chars)
    unique_name = uuid.uuid4().hex[:8]

    # get ticket identifier
    if instance.ticket:
        ticket_identifier = instance.ticket.ticket_code or str(instance.ticket.id)
    elif instance.comment:
        ticket_identifier = instance.comment.ticket.ticket_code or str(instance.comment.ticket.id)
    else:
        ticket_identifier = "unknown"

    return f"attachments/{ticket_identifier}/{unique_name}.{ext}"

class Ticket(models.Model):
    TICKET_TYPE_CHOICES = [
    ('INCIDENT', 'Incident'),
    ('SERVICE', 'Service Request'),
]
    
    ticket_code  = models.CharField(max_length=50, unique=True, editable=False)

    ticket_type = models.CharField(
        max_length=20,
        choices=TICKET_TYPE_CHOICES,
        null=True,blank=True
    )

    title = models.CharField(max_length=255)
    description = models.TextField()

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='assigned_tickets')

    is_deleted = models.BooleanField(default=False)
    deleted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,related_name='deleted_tickets')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)






class TicketProgress(models.Model):
    STATUS_CHOICES = [
            ('OPEN', 'Open'),
            ('IN_PROGRESS', 'In Progress'),
            ('WAITING', 'Waiting'),
            ('CLOSED', 'Closed'),
            ('RESOLVED', 'Resolved'),
    ]

    PRIORITY_CHOICES = [
        ('P1', 'Critical'),
        ('P2', 'High'),
        ('P3', 'Medium'),
        ('P4', 'Low'),
    ]
    
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='status_history')

    status = models.CharField(max_length=30, choices=STATUS_CHOICES,)

    priority = models.CharField(
                                max_length=2,
                                choices=PRIORITY_CHOICES,
                                default='P3'
                                )

    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='status_changed')

    updated_at = models.DateTimeField(auto_now_add=True)




class Comment(models.Model):
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_comments'
    )

    content = models.TextField()

    # 🔒 visibility control
    is_internal = models.BooleanField(default=False)

    # ✏️ edit control
    is_edited = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def edit_comment(self, new_content):
        """
        Allow edit ONLY once
        """
        if self.is_edited:
            raise ValueError("Comment can only be edited once")

        self.content = new_content
        self.is_edited = True
        self.save()

    def __str__(self):
        return f"{self.ticket.id} - {self.user}"
    


class Attachment(models.Model):
    file = models.FileField(upload_to=ticket_attachment_upload_path)

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='ticket_attachments'
    )

    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='comment_attachments'
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name}"