from django.contrib import admin
from .models import Ticket, TicketProgress, Comment, Attachment



@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        'ticket_code',
        'ticket_type',
        'title',
        'created_by',
        'assigned_to',
        'created_at'
    )

    ordering = ('-created_at',)  # 🔥 latest first

    list_per_page = 20  # ✅ pagination

    search_fields = ('ticket_code', 'title')

    readonly_fields = ('ticket_code', 'created_at', 'updated_at')


@admin.register(TicketProgress)
class TicketProgressAdmin(admin.ModelAdmin):
    list_display = (
        'ticket',
        'status',
        'priority',
        'changed_by',
        'updated_at'
    )

    ordering = ('-updated_at',)
    list_per_page = 20



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'ticket',
        'user',
        'is_internal',
        'is_edited',
        'created_at'
    )

    ordering = ('-created_at',)
    list_per_page = 20


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = (
        'file',
        'uploaded_by',
        'ticket',
        'comment',
        'uploaded_at'
    )

    ordering = ('-uploaded_at',)
    list_per_page = 20