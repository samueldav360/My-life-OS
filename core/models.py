from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
import zoneinfo

class Category(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7, default='#3B82F6')
    def __str__(self): return self.name

class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null= True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self): return self.name

class HabitLog(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    date = models.DateField()
    is_completed = models.BooleanField(default=False)
    class Meta:
        unique_together = ('habit','date')

class ScheduleTemplate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="Nombre de la plantilla")
    
    def __str__(self):
        return self.name

class TimeBlock(models.Model):
    template = models.ForeignKey(ScheduleTemplate, on_delete=models.CASCADE, related_name='blocks', null= True, blank = True)
    title = models.CharField(max_length=100, verbose_name="Título")
    start_time = models.TimeField(verbose_name="Hora de inicio")
    end_time = models.TimeField(verbose_name="Hora de fin")
    color_class = models.CharField(max_length=50, default='bg-blue-900/20 border-blue-800/50 text-blue-400')

    class Meta:
        ordering = ['start_time']

    def __str__(self):
        return f"{self.title} ({self.start_time} - {self.end_time})"
    
class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    is_special = models.BooleanField(default=False)
    stage = models.CharField(max_length=50, default='Rutina normal')

class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    progress = models.IntegerField(default=0)
    deadline = models.DateField(null=True, blank=True)
    
    def __str__(self): return self.name

class Milestone(models.Model):
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name='milestones')
    title = models.CharField(max_length=255)
    is_completed = models.BooleanField(default=False)

class JournalEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    reflection = models.TextField(blank=True, verbose_name="Reflexión del día")
    went_well = models.TextField(blank=True, verbose_name="Qué salió bien")
    to_improve = models.TextField(blank=True, verbose_name="Qué mejorar")
    quick_notes = models.TextField(blank=True, verbose_name="Notas rápidas")
    links = models.URLField(blank=True, verbose_name="Enlace adjunto")

    class Meta:
        unique_together = ('user', 'date')

    def __str__(self): return f"Diario - {self.date}"

class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    timezone = models.CharField(max_length=50, default='America/Bogota')
    
    THEMES = [
        ('dark', 'Oscuro'),
        ('light', 'Claro'),
    ]
    theme = models.CharField(max_length=10, choices=THEMES, default='dark', verbose_name="Tema")
    accent_color = models.CharField(max_length=7, default='#3B82F6', verbose_name="Color principal")
    
    def __str__(self):
        return f"Configuración de {self.user.username}"
    
class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            try:
                user_tz = request.user.settings.timezone 
                if user_tz:
                    timezone.activate(zoneinfo.ZoneInfo(user_tz))
            except Exception:
                timezone.deactivate()
        else:
            timezone.deactivate()
            
        return self.get_response(request)