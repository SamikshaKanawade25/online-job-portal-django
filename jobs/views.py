from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import UserProfile, Job, Application
from .forms import SignUpForm, JobForm


# ---------- Authentication ----------

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            UserProfile.objects.create(user=user, role=form.cleaned_data['role'])
            messages.success(request, 'Account created! Please log in.')
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'jobs/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('job_list')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'jobs/login.html')


def logout_view(request):
    logout(request)
    return redirect('job_list')


# ---------- Jobs ----------

def job_list(request):
    query = request.GET.get('q')
    jobs = Job.objects.all().order_by('-posted_date')
    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) | Q(location__icontains=query) | Q(company_name__icontains=query)
        )

    applied_job_ids = []
    if request.user.is_authenticated:
        applied_job_ids = Application.objects.filter(applicant=request.user).values_list('job_id', flat=True)

    return render(request, 'jobs/job_list.html', {
        'jobs': jobs, 'query': query, 'applied_job_ids': applied_job_ids
    })


@login_required
def job_post(request):
    profile = UserProfile.objects.get(user=request.user)
    if profile.role != 'employer':
        messages.error(request, 'Only employers can post jobs.')
        return redirect('job_list')

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user
            job.save()
            return redirect('job_list')
    else:
        form = JobForm()
    return render(request, 'jobs/job_form.html', {'form': form})


@login_required
def job_edit(request, pk):
    job = get_object_or_404(Job, pk=pk, employer=request.user)
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('job_list')
    else:
        form = JobForm(instance=job)
    return render(request, 'jobs/job_form.html', {'form': form})


@login_required
def job_delete(request, pk):
    job = get_object_or_404(Job, pk=pk, employer=request.user)
    if request.method == 'POST':
        job.delete()
        return redirect('job_list')
    return render(request, 'jobs/job_confirm_delete.html', {'job': job})


# ---------- Applications ----------

@login_required
def apply_job(request, pk):
    profile = UserProfile.objects.get(user=request.user)
    if profile.role != 'seeker':
        messages.error(request, 'Only job seekers can apply.')
        return redirect('job_list')

    job = get_object_or_404(Job, pk=pk)
    Application.objects.get_or_create(job=job, applicant=request.user)
    messages.success(request, 'Applied successfully!')
    return redirect('job_list')


@login_required
def my_applications(request):
    applications = Application.objects.filter(applicant=request.user).select_related('job')
    return render(request, 'jobs/my_applications.html', {'applications': applications})


@login_required
def job_applicants(request, pk):
    job = get_object_or_404(Job, pk=pk, employer=request.user)
    applications = job.applications.select_related('applicant')
    return render(request, 'jobs/job_applicants.html', {'job': job, 'applications': applications})
