from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TaskViewSet, LeaveViewSet,
    dashboard_api, mark_attendance,
    dashboard, home, user_login,
    worker_dashboard, apply_leave, status_view, admin_dashboard

)
from rest_framework_simplejwt.views import TokenObtainPairView
from . import views
from django.contrib.auth.views import LogoutView

router = DefaultRouter()
router.register('tasks', TaskViewSet)
router.register('leaves', LeaveViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/dashboard/', views.dashboard_api),
    path('api/attendance/', views.mark_attendance),
    path('api/login/', TokenObtainPairView.as_view(), name='api-login'),

    # 🔹 Website routes
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login_view'),  # make sure this exists

    # Worker
    path('worker-dashboard/', views.worker_dashboard, name='worker_dashboard'),
    path('apply-leave/', views.apply_leave, name='apply_leave'),
    path('worker-dashboard/status/', views.status_view, name='worker_status'),
    path('worker-register/', views.worker_register, name='worker_register'),

    # Admin
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('leave/approve/<int:leave_id>/', views.approve_leave, name='approve_leave'),
    path('leave/reject/<int:leave_id>/', views.reject_leave, name='reject_leave'),
    path('assign-task/', views.assign_task, name='assign_task'),
    path('complete-task/<int:task_id>/', views.complete_task, name='complete_task'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('workers/', views.worker_list, name='worker_list'),
     path('tasks/', views.task_list, name='task_list'), 
     path('completed-tasks/', views.completed_task_list, name='completed_task_list'),
     path('pending-tasks/', views.pending_task_list, name='pending_task_list'),
     path('all-leaves/', views.all_leaves_list, name='all_leaves_list'),
     path('pending-leaves/', views.pending_leaves_list, name='pending_leaves_list'),
    
]