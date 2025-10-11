from django.contrib import admin
from .models import FortuneFeature, Reading, ReadingHistory


@admin.register(FortuneFeature)
class FortuneFeatureAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'feature_type',
        'input_type',
        'is_active',
        'credit_cost',
        'model_name',
        'created_at',
    ]
    list_filter = ['is_active', 'input_type', 'feature_type', 'created_at']
    search_fields = ['name', 'description', 'feature_type']
    readonly_fields = ['id', 'created_at', 'updated_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'name', 'feature_type', 'input_type', 'description', 'is_active')
        }),
        ('Prompt Configuration', {
            'fields': ('prompt_template',)
        }),
        ('OpenRouter.ai Settings', {
            'fields': ('model_name', 'max_tokens', 'temperature')
        }),
        ('Pricing', {
            'fields': ('credit_cost',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Reading)
class ReadingAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'feature',
        'status',
        'created_at',
        'processing_time',
    ]
    list_filter = ['status', 'feature__feature_type', 'created_at']
    search_fields = ['user__phone_number', 'feature__name', 'text_input']
    readonly_fields = [
        'id',
        'user',
        'feature',
        'text_input',
        'image',
        'interpretation',
        'model_used',
        'tokens_used',
        'processing_time',
        'created_at',
        'updated_at',
    ]

    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'user', 'feature', 'status')
        }),
        ('Input Data', {
            'fields': ('text_input', 'image')
        }),
        ('Output Data', {
            'fields': ('interpretation', 'error_message')
        }),
        ('Metadata', {
            'fields': ('model_used', 'tokens_used', 'processing_time', 'created_at', 'updated_at')
        }),
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        # Only allow deletion of failed readings
        if obj and obj.status == 'failed':
            return True
        return False


@admin.register(ReadingHistory)
class ReadingHistoryAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'feature',
        'rating',
        'created_at',
    ]
    list_filter = ['rating', 'feature__feature_type', 'created_at']
    search_fields = ['user__phone_number', 'feature__name', 'feedback']
    readonly_fields = ['user', 'feature', 'reading', 'created_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'feature', 'reading', 'created_at')
        }),
        ('User Feedback', {
            'fields': ('rating', 'feedback')
        }),
    )

    def has_add_permission(self, request):
        return False
