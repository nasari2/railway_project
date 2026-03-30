from django.shortcuts import render
from rest_framework import viewsets
from .models import Task, Leave
from .serializers import TaskSerializer, LeaveSerializer

from django.shortcuts import render, redirect, get_object_or_404

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class LeaveViewSet(viewsets.ModelViewSet):
    queryset = Leave.objects.all()
    serializer_class = LeaveSerializer

# Create your views here.

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, Task

@api_view(['GET'])
def dashboard_api(request):
    total_workers = User.objects.count()
    completed_tasks = Task.objects.filter(status='completed').count()
    pending_tasks = Task.objects.filter(status='pending').count()

    return Response({
        "total_workers": total_workers,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks
    })



from datetime import date

@api_view(['POST'])
def mark_attendance(request):
    user_id = request.data.get('user_id')
    worked = request.data.get('worked')  # True/False

    Task.objects.create(
        user_id=user_id,
        title="Daily Work",
        status='completed' if worked else 'pending',
        date=date.today()
    )

    return Response({"message": "Attendance marked"})


from django.shortcuts import render
from .models import User, Task, Leave

def dashboard(request):
    total_workers = User.objects.count()
    completed_tasks = Task.objects.filter(status='completed').count()
    pending_tasks = Task.objects.filter(status='pending').count()
    total_leaves = Leave.objects.count()

    return render(request, 'dashboard.html', {
        'total_workers': total_workers,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'total_leaves': total_leaves
    })

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import User


# Home page
def home(request):
    return render(request, 'home.html')


# Login page
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            # Redirect based on role
            if user.role == 'admin':
                return redirect('/dashboard/')
            else:
                return redirect('/dashboard/')

        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')

from django.http import HttpResponse

def api_home(request):
    return HttpResponse("<h1>🚆 Railway API Running</h1>")


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def home(request):
    return render(request, 'home.html')




from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # 🔥 Role-based redirect
            if user.role == 'admin':
                return redirect('/admin-dashboard/')
            else:
                return redirect('/worker-dashboard/')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')


from django.shortcuts import render
from .models import Task,Leave

def worker_dashboard(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'workforce/worker_dashboard.html', {'tasks': tasks})

def apply_leave(request):
    if request.method == 'POST':
        Leave.objects.create(
            user=request.user,
            from_date=request.POST['from_date'],
            to_date=request.POST['to_date'],
            reason=request.POST['reason']
        )
        return redirect('worker-dashboard/')
    return render(request, 'workforce/apply_leave.html')

def status_view(request):
    tasks = Task.objects.filter(user=request.user)
    leaves = Leave.objects.filter(user=request.user)
    return render(request, 'workforce/status.html', {'tasks': tasks, 'leaves': leaves})


def apply_leave(request):
    if request.method == 'POST':
        Leave.objects.create(
            user=request.user,           # ✅ link leave to logged-in worker
            from_date=request.POST['from_date'],
            to_date=request.POST['to_date'],
            reason=request.POST['reason']
        )
        return redirect('worker_dashboard')
    return render(request, 'workforce/apply_leave.html')


from django.shortcuts import render
from .models import User, Task, Leave

# views.py (can still be inside workforce/views.py)
from django.shortcuts import render
from .models import User, Task, Leave
from django.shortcuts import render, redirect
from .models import User, Task, Leave

def admin_dashboard(request):
    workers = User.objects.filter(role='worker')

    tasks = Task.objects.all()
    leaves = Leave.objects.all()

    context = {
        'workers': workers,
        'total_workers': workers.count(),
        'tasks': tasks,
        'total_tasks': tasks.count(),
        'completed_tasks': tasks.filter(status='Completed').count(),
        'pending_tasks': tasks.filter(status='Pending').count(),
        'total_leaves': leaves.count(),
        'pending_leaves': leaves.filter(status='Pending').count(),
        'pending_leaves_list': leaves.filter(status='Pending'),
    }

    return render(request, 'workforce/admin_dashboard.html', context)


def approve_leave(request, leave_id):
    leave = Leave.objects.get(id=leave_id)
    leave.status = 'approved'
    leave.save()
    return redirect('admin_dashboard')


def reject_leave(request, leave_id):
    leave = Leave.objects.get(id=leave_id)
    leave.status = 'rejected'
    leave.save()
    return redirect('admin_dashboard')

# Assign task to worker
from django.shortcuts import get_object_or_404, redirect, render

def assign_task(request):
    if request.method == 'POST':
        user_id = request.POST.get('worker')
        title = request.POST.get('title')

        user = get_object_or_404(User, id=user_id)

        Task.objects.create(
            user=user,
            title=title,
            status='Pending'   # ✅ only this
        )

        return redirect('admin_dashboard')

    workers = User.objects.filter(role='worker')
    return render(request, 'workforce/assign_task.html', {'workers': workers})

def complete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.status = 'Completed'
    task.save()
    return redirect('worker_dashboard')



from django.shortcuts import render
from .models import Task, Leave

def worker_dashboard(request):
    # ✅ Filter tasks and leaves for the logged-in worker
    tasks = Task.objects.filter(user=request.user)
    leaves = Leave.objects.filter(user=request.user)

    context = {
        'tasks': tasks,
        'leaves': leaves
    }
    return render(request, 'workforce/worker_dashboard.html', context)

def apply_leave(request):
    if request.method == 'POST':
        # Link leave to logged-in user
        Leave.objects.create(
            user=request.user,   # ✅ use 'user', not 'worker'
            from_date=request.POST['from_date'],
            to_date=request.POST['to_date'],
            reason=request.POST['reason']
        )
        return redirect('worker_dashboard')
    return render(request, 'workforce/apply_leave.html')

def status_view(request):
    tasks = Task.objects.filter(user=request.user)
    leaves = Leave.objects.filter(user=request.user)
    return render(request, 'workforce/status.html', {'tasks': tasks, 'leaves': leaves})




from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import User, Task, Leave

# Home page
def home(request):
    return render(request, 'home.html')

# Admin login
def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.role == 'admin':
            login(request, user)
            return redirect('admin_dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid admin credentials', 'role': 'admin'})
    return render(request, 'login.html', {'role': 'admin'})

# Worker login
def worker_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.role == 'worker':
            login(request, user)
            return redirect('worker_dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid worker credentials', 'role': 'worker'})
        
    return render(request, 'login.html', {'role': 'worker'})


def assign_task(request):
    if request.method == 'POST':
        user_id = request.POST.get('worker')
        title = request.POST.get('title')
        status = request.POST.get('status')
        user = get_object_or_404(User, id=user_id)
        Task.objects.create(user=user, title=title, status=status)
        return redirect('admin_dashboard')
    
    workers = User.objects.filter(role='worker')
    return render(request, 'workforce/assign_task.html', {'workers': workers})



from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Task, Leave

# Worker registration
# workforce/views.py
from django.shortcuts import render, redirect
from .models import User

def worker_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        address = request.POST.get('address', '')
        job_title = request.POST.get('job_title', '')
        phone_number = request.POST.get('phone_number', '')

        User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role='worker',
            address=address,
            job_title=job_title,
            phone_number=phone_number
        )
        return redirect('login_view')
    return render(request, 'workforce/worker_register.html')


# Approve leave
def approve_leave(request, leave_id):
    leave = get_object_or_404(Leave, id=leave_id)
    leave.status = 'approved'
    leave.save()
    return redirect('admin_dashboard')


# Reject leave
def reject_leave(request, leave_id):
    leave = get_object_or_404(Leave, id=leave_id)
    leave.status = 'rejected'
    leave.save()
    return redirect('admin_dashboard')


# Assign task
def assign_task(request):
    if request.method == 'POST':
        user_id = request.POST.get('worker')
        title = request.POST.get('title')

        user = get_object_or_404(User, id=user_id)

        Task.objects.create(
            user=user,
            title=title,
            status='Pending'   # ✅ FIXED
        )

        return redirect('admin_dashboard')

    workers = User.objects.filter(role='worker')
    return render(request, 'workforce/assign_task.html', {'workers': workers})




from django.shortcuts import render
from .models import User

def worker_list(request):
    # Get all workers
    workers = User.objects.filter(role='worker')
    return render(request, 'workforce/worker_list.html', {'workers': workers})



from django.shortcuts import render
from .models import Task

def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'workforce/task_list.html', {'tasks': tasks})



from django.shortcuts import render
from .models import Task

def completed_task_list(request):
    tasks = Task.objects.filter(status='Completed')  # Only completed tasks
    return render(request, 'workforce/completed_task_list.html', {'tasks': tasks})




def pending_task_list(request):
    tasks = Task.objects.filter(status='Pending')  # Only pending tasks
    return render(request, 'workforce/pending_task_list.html', {'tasks': tasks})




def all_leaves_list(request):
    leaves = Leave.objects.all()  # Fetch all leaves
    return render(request, 'workforce/all_leaves_list.html', {'leaves': leaves})



def pending_leaves_list(request):
    leaves = Leave.objects.filter(status='pending')  # Only pending leaves
    return render(request, 'workforce/pending_leaves_list.html', {'leaves': leaves})