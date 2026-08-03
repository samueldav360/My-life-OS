from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.db.models import Count
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
import json
from datetime import date, datetime, timedelta
from .models import (
    Category, Habit, HabitLog, 
    TimeBlock, Event, 
    Goal, Milestone, 
    JournalEntry, 
    UserSettings,
    ScheduleTemplate
)

@login_required
def dashboard(request):
    today = date.today()
    now = datetime.now().time()
    
    habits_today = Habit.objects.filter(user=request.user, is_active=True)
    logs_today = HabitLog.objects.filter(habit__in=habits_today, date=today)
    
    completed_count = logs_today.filter(is_completed=True).count()
    total_habits = habits_today.count()
    progress = int((completed_count / total_habits) * 100) if total_habits > 0 else 0

    global_streak = 0
    check_date = today if completed_count > 0 else today - timedelta(days=1)
    
    for _ in range(365):
        has_completed = HabitLog.objects.filter(habit__user=request.user, date=check_date, is_completed=True).exists()
        if has_completed:
            global_streak += 1
            check_date -= timedelta(days=1)
        else:
            break

    today_events = Event.objects.filter(user=request.user, date=today).order_by('start_time')
    current_block = today_events.filter(start_time__lte=now, end_time__gt=now).first()
    next_block = today_events.filter(start_time__gt=now).first()
    current_goal = Goal.objects.filter(user=request.user).first()

    last_7_dates = [today - timedelta(days=i) for i in range(6, -1, -1)]
    dias_espanol = {0: 'Lun', 1: 'Mar', 2: 'Mié', 3: 'Jue', 4: 'Vie', 5: 'Sáb', 6: 'Dom'}
    
    chart_labels = [dias_espanol[d.weekday()] for d in last_7_dates]
    chart_data_list = []
    
    for d in last_7_dates:
        completados = HabitLog.objects.filter(
            habit__user=request.user, date=d, is_completed=True
        ).count()
        chart_data_list.append(completados)

    context = {
        'today': today,
        'progress': progress,
        'completed_count': completed_count,
        'total_habits': total_habits,
        'logs_today': logs_today,         # ¡AQUÍ ESTÁ HECHO HOY!
        'global_streak': global_streak,   # ¡AQUÍ ESTÁ LA RACHA!
        'current_block': current_block,
        'next_block': next_block,
        'current_goal': current_goal,
        'chart_labels': json.dumps(chart_labels),
        'chart_data': json.dumps(chart_data_list),
    }
    
    return render(request, 'core/dashboard.html', context)

@login_required
def habits_page(request):
    today = date.today()
    habits = Habit.objects.filter(user=request.user, is_active=True)
    categories = Category.objects.all()

    for habit in habits:
        log = HabitLog.objects.filter(habit=habit, date=today).first()
        habit.today_completed = log.is_completed if log else False

        streak = 0
        check_date = today if habit.today_completed else today - timedelta(days=1)
        
        for _ in range(365): 
            day_log = HabitLog.objects.filter(habit=habit, date=check_date, is_completed=True).exists()
            if day_log:
                streak += 1
                check_date -= timedelta(days=1)
            else:
                break 
                
        habit.streak = streak
    start_date = today - timedelta(days=119)

    logs_heatmap = HabitLog.objects.filter(
        habit__user=request.user, 
        date__gte=start_date, 
        is_completed=True
    ).values('date').annotate(count=Count('id'))
    
    log_dict = {log['date']: log['count'] for log in logs_heatmap}
    
    heatmap_data = []
    total_active_habits = habits.count()
    
    for i in range(119, -1, -1):
        d = today - timedelta(days=i)
        completed_count = log_dict.get(d, 0)
        pct = int((completed_count / total_active_habits) * 100) if total_active_habits > 0 else 0
        heatmap_data.append({'date': d, 'pct': pct})

    return render(request, 'core/habits.html', {
        'habits': habits, 
        'categories': categories,
        'today': today,
        'heatmap_data': heatmap_data
    })

@login_required
def add_habit(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        if name:
            category = Category.objects.get(id=category_id) if category_id else None
            Habit.objects.create(user=request.user, name=name, category=category)
    return redirect('habits')

@login_required
def toggle_habit(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            habit_id = data.get('habit_id')
            is_completed = data.get('is_completed')

            habit = get_object_or_404(Habit, id=habit_id, user=request.user)
            
            log, created = HabitLog.objects.get_or_create(
                habit=habit,
                date=date.today()
            )
            
            log.is_completed = is_completed
            log.save()

            return JsonResponse({'status': 'success'})
        except Exception as e:
            print(f"Error guardando hábito: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
            
    return JsonResponse({'status': 'error'}, status=405)

@login_required
def delete_habit(request, habit_id):
    if request.method == 'POST':
        try:
            habit = get_object_or_404(Habit, id=habit_id, user=request.user)
            habit.delete()
            
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
            
    return JsonResponse({'status': 'error'}, status=405)

@login_required
def agenda_page(request):
    templates = ScheduleTemplate.objects.filter(user=request.user)
    today = date.today()
    
    today_events = Event.objects.filter(user=request.user, date=today).order_by('start_time')
    
    return render(request, 'core/agenda.html', {
        'templates': templates,
        'today': today,
        'today_events': today_events
    })

@login_required
def create_template(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            ScheduleTemplate.objects.create(user=request.user, name=name)
    return redirect('agenda')

@login_required
def template_detail(request, template_id):
    template = get_object_or_404(ScheduleTemplate, id=template_id, user=request.user)
    blocks = template.blocks.all()
    return render(request, 'core/template_detail.html', {'template': template, 'blocks': blocks})

@login_required
def add_timeblock(request, template_id):
    if request.method == 'POST':
        template = get_object_or_404(ScheduleTemplate, id=template_id, user=request.user)
        title = request.POST.get('title')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        
        if title and start_time and end_time:
            TimeBlock.objects.create(
                template=template,
                title=title,
                start_time=start_time,
                end_time=end_time
            )
    return redirect('template_detail', template_id=template_id)

@login_required
def delete_timeblock(request, template_id, block_id):
    template = get_object_or_404(ScheduleTemplate, id=template_id, user=request.user)
    block = get_object_or_404(TimeBlock, id=block_id, template=template)
    
    if request.method == 'POST':
        block.delete()
        
    return redirect('template_detail', template_id=template_id)

@login_required
def apply_template(request, template_id):
    template = get_object_or_404(ScheduleTemplate, id=template_id, user=request.user)
    today = date.today()
    
    stage_id = f"Plantilla: {template.name}"
    
    Event.objects.filter(
        user=request.user, 
        date=today, 
        stage=stage_id
    ).delete()
    
    for block in template.blocks.all():
        Event.objects.create(
            user=request.user,
            title=block.title,
            date=today,
            start_time=block.start_time,
            end_time=block.end_time,
            stage=stage_id
        )
    
    return redirect('agenda')

@login_required
def add_event(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        event_date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        stage = request.POST.get('stage', 'Rutina normal')
        if title and event_date:
            Event.objects.create(
                user=request.user,
                title=title,
                date=event_date,
                start_time=start_time,
                end_time=end_time,
                stage=stage
            )
    return redirect('agenda')

@login_required
def goals_page(request):
    goals = Goal.objects.filter(user=request.user).order_by('-progress')
    return render(request, 'core/goals.html', {'goals': goals})

@login_required
def add_goal(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        deadline = request.POST.get('deadline') or None
        if name:
            Goal.objects.create(
                user=request.user,
                name=name,
                description=description,
                deadline=deadline
            )
    return redirect('goals')

@login_required
def goal_detail(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id, user=request.user)
    milestones = goal.milestones.all().order_by('is_completed')
    return render(request, 'core/goal_detail.html', {'goal': goal, 'milestones': milestones})

@login_required
def add_milestone(request, goal_id):
    if request.method == 'POST':
        goal = get_object_or_404(Goal, id=goal_id, user=request.user)
        title = request.POST.get('title')
        if title:
            Milestone.objects.create(goal=goal, title=title)
    return redirect('goal_detail', goal_id=goal_id)

@login_required
def toggle_milestone(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        milestone_id = data.get('milestone_id')
        is_completed = data.get('is_completed')
        
        milestone = get_object_or_404(Milestone, id=milestone_id, goal__user=request.user)
        milestone.is_completed = is_completed
        milestone.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def journal_page(request):
    entry, created = JournalEntry.objects.get_or_create(
        user=request.user,
        date=date.today()
    )
    return render(request, 'core/journal.html', {'entry': entry})

@login_required
def save_journal(request):
    if request.method == 'POST':
        entry, created = JournalEntry.objects.get_or_create(
            user=request.user,
            date=date.today()
        )
        entry.reflection = request.POST.get('reflection', '')
        entry.went_well = request.POST.get('went_well', '')
        entry.to_improve = request.POST.get('to_improve', '')
        entry.quick_notes = request.POST.get('quick_notes', '')
        entry.links = request.POST.get('links', '')
        entry.save()
    return redirect('journal')

@login_required
def settings_page(request):
    settings, created = UserSettings.objects.get_or_create(user=request.user)
    return render(request, 'core/settings.html', {'settings': settings})

@login_required
def save_settings(request):
    if request.method == 'POST':
        settings, created = UserSettings.objects.get_or_create(user=request.user)
        settings.theme = request.POST.get('theme', 'dark')
        settings.accent_color = request.POST.get('accent_color', '#3B82F6')
        settings.save()
    return redirect('settings')

def export_data(request):
    data = {
        "user": request.user.username,
        "habits": list(Habit.objects.filter(user=request.user).values('name', 'category__name', 'is_active')),
        "habit_logs": list(HabitLog.objects.filter(habit__user=request.user).values('habit__name', 'date', 'is_completed')),
        "goals": list(Goal.objects.filter(user=request.user).values('name', 'progress', 'deadline')),
        "journal": list(JournalEntry.objects.filter(user=request.user).values('date', 'reflection', 'went_well', 'to_improve'))
    }
    
    response = HttpResponse(json.dumps(data, indent=4, ensure_ascii=False), content_type="application/json")
    response['Content-Disposition'] = 'attachment; filename="mylifeos_backup.json"'
    return response

@login_required
def clear_data(request):
    if request.method == 'POST':
        data_type = request.POST.get('data_type')
        if data_type == 'habits':
            Habit.objects.filter(user=request.user).delete()
        elif data_type == 'events':
            Event.objects.filter(user=request.user).delete()
        elif data_type == 'goals':
            Goal.objects.filter(user=request.user).delete()
        elif data_type == 'journal':
            JournalEntry.objects.filter(user=request.user).delete()
    return redirect('settings')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()       
            login(request, user)     
            return redirect('dashboard') 
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})
