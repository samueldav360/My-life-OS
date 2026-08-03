from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from core import views

urlpatterns = [

    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),

    path('', views.dashboard, name='dashboard'),

    path('habitos/', views.habits_page, name='habits'),
    path('habitos/agregar/', views.add_habit, name='add_habit'),
    path('habitos/toggle/', views.toggle_habit, name='toggle_habit'), 
    path('habitos/eliminar/<int:habit_id>/', views.delete_habit, name='delete_habit'),

    path('agenda/', views.agenda_page, name='agenda'),
    path('agenda/crear-plantilla/', views.create_template, name='create_template'),
    path('agenda/plantilla/<int:template_id>/', views.template_detail, name='template_detail'),
    path('agenda/plantilla/<int:template_id>/agregar-bloque/', views.add_timeblock, name='add_timeblock'),
    path('agenda/plantilla/<int:template_id>/usar-hoy/', views.apply_template, name='apply_template'),
    path('agenda/plantilla/<int:template_id>/borrar-bloque/<int:block_id>/', views.delete_timeblock, name='delete_timeblock'),

    path('objetivos/', views.goals_page, name='goals'),
    path('objetivos/agregar/', views.add_goal, name='add_goal'),
    path('objetivos/<int:goal_id>/', views.goal_detail, name='goal_detail'),
    path('objetivos/<int:goal_id>/hito/agregar/', views.add_milestone, name='add_milestone'),
    path('hito/<int:milestone_id>/toggle/', views.toggle_milestone, name='toggle_milestone'),

    path('diario/', views.journal_page, name='journal'),
    path('diario/guardar/', views.save_journal, name='save_journal'),

    path('configuracion/', views.settings_page, name='settings'),
    path('configuracion/guardar/', views.save_settings, name='save_settings'),
    path('configuracion/exportar/', views.export_data, name='export_data'),
    path('configuracion/limpiar/', views.clear_data, name='clear_data'),
]
