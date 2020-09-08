from django.contrib import admin
# Register your models here.
from .models import *
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin import SimpleListFilter
from django.core.exceptions import ValidationError
from django import forms

bot = telegram.Bot(TELEGRAM_TOKEN)


class UserTabularForm(forms.ModelForm):
    def clean(self):
        tr_group = self.cleaned_data.get('traininggroup')
        if tr_group and tr_group.status == TrainingGroup.STATUS_GROUP:
            users = tr_group.users.all()
            max_players = tr_group.max_players
            if users.count() >= max_players:
                raise ValidationError(
                    {'traininggroup': 'Количество игроков в группе должно быть не больше {}, вы указали {}.'. \
                    format(max_players, users.count() + 1)})


class UserTabularInline(admin.StackedInline):
    model = TrainingGroup.users.through
    max_num = 2
    form = UserTabularForm


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = UserForm
    inlines = [UserTabularInline]
    list_display = ('id', 'first_name', 'last_name', 'phone_number', 'status')
    search_fields = ('first_name', 'last_name')
    list_filter = ('status',)
    ordering = ['first_name']


class DefaultGroupStatus(SimpleListFilter):
    title = _('Статус')

    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return TrainingGroup.GROUP_STATUSES

    def choices(self, cl):
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == lookup,
                'query_string': cl.get_query_string({
                    self.parameter_name: lookup,
                }, []),
                'display': title,
            }

    def queryset(self, request, queryset):
        if self.value() in (TrainingGroup.STATUS_SECTION, TrainingGroup.STATUS_FEW, TrainingGroup.STATUS_4IND):
            return queryset.filter(status=self.value())
        elif self.value() is None:
            return queryset.filter(status=TrainingGroup.STATUS_GROUP)


def make_group_orange(modeladmin, request, queryset):
    queryset.update(level=TrainingGroup.LEVEL_ORANGE)


def make_group_green(modeladmin, request, queryset):
    queryset.update(level=TrainingGroup.LEVEL_GREEN)


make_group_orange.short_description = 'Сделать группу 🧡'
make_group_green.short_description = 'Сделать группу 🍏'


@admin.register(TrainingGroup)
class TrainingGroupAdmin(admin.ModelAdmin):

    form = TrainingGroupForm
    list_display = ('name', 'max_players', 'level')
    filter_horizontal = ('users',)
    list_filter = [DefaultGroupStatus]
    actions = [make_group_green, make_group_orange]


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


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('player', 'month', 'year', 'theory_amount', 'n_fact_visiting', 'fact_amount')
    list_filter = ('year', 'month', 'player')
    search_fields = ('player__first_name', 'player__last_name')
    readonly_fields = ('theory_amount', 'n_fact_visiting')


@admin.register(StaticData)
class StaticDataAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': forms.Textarea}
    }