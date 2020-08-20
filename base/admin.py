from django.contrib import admin
# Register your models here.
from .models import *

bot = telegram.Bot(TELEGRAM_TOKEN)


class UserTabularInline(admin.StackedInline):
    model = TrainingGroup.users.through
    max_num = 1

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return True


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = UserForm
    inlines = [UserTabularInline]
    list_display = ('id', 'first_name', 'last_name', 'phone_number', 'status')
    search_fields = ('first_name', 'last_name')
    list_filter = ('status',)
    ordering = ['first_name']


@admin.register(TrainingGroup)
class TrainingGroupAdmin(admin.ModelAdmin):

    form = TrainingGroupForm
    list_display = ('name', 'max_players')
    filter_horizontal = ('users',)


def make_trday_unavailable(modeladmin, request, queryset):
    queryset.update(is_available=False)

    for day in queryset:
        send_alert_about_changing_tr_day_status(day, day.is_available, bot)


def make_trday_available(modeladmin, request, queryset):
    queryset.update(is_available=True)
    for day in queryset:
        send_alert_about_changing_tr_day_status(day, day.is_available, bot)


make_trday_unavailable.short_description = "Сделать выбранные дни недоступными"
make_trday_available.short_description = 'Сделать выбранные дни доступными'


@admin.register(GroupTrainingDay)
class GroupTrainingDayAdmin(admin.ModelAdmin):
    form = GroupTrainingDayForm
    list_display = ('group', 'date', 'is_available', 'start_time', 'duration',)
    list_filter = ('group', 'date', 'tr_day_status')
    filter_horizontal = ('visitors', 'absent')
    date_hierarchy = 'date'
    actions = [make_trday_unavailable, make_trday_available]
    ordering = ['date', 'start_time']

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


