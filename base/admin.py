from django.contrib import admin
# Register your models here.
from .models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = UserForm
    list_display = ('id', 'first_name', 'last_name', 'phone_number', 'status')
    search_fields = ('first_name', 'last_name')
    list_filter = ('status',)


@admin.register(TrainingGroup)
class TrainingGroupAdmin(admin.ModelAdmin):
    form = TrainingGroupForm
    list_display = ('name', 'max_players')
    raw_id_fields = ('users',)


@admin.register(GroupTrainingDay)
class GroupTrainingDayAdmin(admin.ModelAdmin):
    form = GroupTrainingDayForm
    list_display = ('group', 'date', 'is_available', 'start_time', 'duration', 'id')
    list_filter = ('group', 'date')
    raw_id_fields = ('group', 'visitors')

    def get_object(self, request, object_id, from_field=None):
        obj = super().get_object(request, object_id, from_field=from_field)
        # Cache object for use in formfield_for_manytomany
        request.report_obj = obj
        return obj

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'absent' and hasattr(request, 'report_obj'):
            kwargs['queryset'] = User.objects.filter(traininggroup__id=request.report_obj.group.id)
        if db_field.name == 'visitors' and hasattr(request, 'report_obj'):
            kwargs['queryset'] = User.objects.exclude(traininggroup__id=request.report_obj.group.id)
        return super(GroupTrainingDayAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ('code', 'username')

