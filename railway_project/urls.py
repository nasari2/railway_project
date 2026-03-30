from django.contrib import admin
from django.urls import path, include
from workforce.views import home, login_view, admin_dashboard, worker_dashboard
from workforce import views
from django.contrib.auth.views import LogoutView 
app_name = 'workforce' 

urlpatterns = [
     path('admin/', admin.site.urls),

    # Home page
    path('', views.home, name='home'),

    # Login pages
    path('login/admin/', views.admin_login, name='admin_login'),
    path('login/worker/', views.worker_login, name='worker_login'),

    # Dashboards
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('worker-dashboard/', views.worker_dashboard, name='worker_dashboard'),

    # Leave & status
    path('apply-leave/', views.apply_leave, name='apply_leave'),
    path('worker-dashboard/status/', views.status_view, name='worker_status'),
     path('', include('workforce.urls')),
     #   path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
        path('admin/', admin.site.urls),
     path('login/', login_view, name='login'),
    # ✅ ADD LOGOUT HERE
    path('logout/', LogoutView.as_view(next_page='/login/'), name='logout'),
]