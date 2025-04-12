from django.shortcuts import render, redirect, get_object_or_404
from .models import Job, Applicant, FraudCheck
from .forms import SignupForm, ResumeFraudForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
import os

# ML utilities
from .ml.predict_eligibility import extract_text_from_resume, check_eligibility_and_score
from .ml.recommend_jobs import recommend_jobs_for_resume
from .ml.fraud_detection import is_resume_fraudulent
from .ml.skill_gap import analyze_skill_gap
from .ml.improvement_resources import get_learning_resources

# -------------------------------
# Job List (Homepage View)
# -------------------------------
def index(request):
    return render(request, 'index.html')
def job_list(request):
    jobs = Job.objects.all()
    return render(request, 'joblist.html', {'jobs': jobs})

# -------------------------------
# Job Application View
# -------------------------------
# views.py (relevant parts updated)

@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        resume_file = request.FILES.get('resume')

        if not resume_file:
            messages.error(request, "Please upload a valid resume.")
            return redirect(request.path)

        applicant = Applicant.objects.create(
            job=job,
            name=name,
            email=email,
            resume=resume_file
        )

        resume_path = applicant.resume.path
        recommendations = []

        if os.path.exists(resume_path):
            resume_text = extract_text_from_resume(resume_path)
            eligible, score = check_eligibility_and_score(resume_text, job.description)

            applicant.resume_text = resume_text
            applicant.is_eligible = eligible
            applicant.score = score

            if not eligible:
                all_jobs = Job.objects.exclude(id=job.id)
                recommended = recommend_jobs_for_resume(resume_text, all_jobs)
                applicant.recommendations = [int(job['id']) for job in recommended]

        else:
            applicant.is_eligible = False
            applicant.score = 0

        applicant.save()
        return redirect('result_view', pk=applicant.id)

    return render(request, 'apply_job.html', {'job': job})


def scoreboard_view(request, job_id):
    job = get_object_or_404 (Job, id=job_id)
    eligible_applicants = Applicant.objects.filter (job=job, is_eligible=True).order_by ('-score')

    context = {
        'job': job,
        'applicants': eligible_applicants
    }
    return render (request, 'scoreboard.html', context)
def result_view(request, pk):
    applicant = get_object_or_404 (Applicant, pk=pk)
    job = get_object_or_404 (Job, id=applicant.job.id)

    resume_path = applicant.resume.path
    resume_text = extract_text_from_resume (resume_path)

    eligible, score = check_eligibility_and_score (resume_text, job.description)

    skill_gaps = analyze_skill_gap (resume_text, job.description)
    learning_resources = get_learning_resources (skill_gaps)

    recommended_jobs = recommend_jobs_for_resume (resume_text, Job.objects.exclude (id=job.id))

    context = {
        "applicant": applicant,
        "job": job,
        "eligible": eligible,
        "score": score,
        "recommended_jobs": recommended_jobs,
        "skill_gaps": skill_gaps,
        "learning_resources": learning_resources,
    }

    return render (request, "result.html", context)


# -------------------------------
# Resume Fraud Detection View
# -------------------------------
def fraud_check_view(request):
    result = None
    is_checked = False

    if request.method == 'POST':
        form = ResumeFraudForm(request.POST, request.FILES)
        if form.is_valid():
            resume = form.cleaned_data['resume']
            save_dir = os.path.join(settings.MEDIA_ROOT, "fraud_check")
            os.makedirs(save_dir, exist_ok=True)
            temp_path = os.path.join(save_dir, resume.name)

            with open(temp_path, 'wb+') as dest:
                for chunk in resume.chunks():
                    dest.write(chunk)

            if os.stat(temp_path).st_size == 0:
                messages.error(request, "The submitted file is empty.")
                return redirect('fraud_check')

            is_fraud = is_resume_fraudulent(temp_path)
            FraudCheck.objects.create(resume=resume, result=is_fraud)
            result = is_fraud
            is_checked = True
            os.remove(temp_path)
        else:
            messages.error(request, "Invalid form.")
    else:
        form = ResumeFraudForm()

    return render(request, 'fraud_check.html', {
        'form': form,
        'result': result,
        'is_checked': is_checked
    })


# -------------------------------
# Signup View
# -------------------------------
def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Signup successful. Please log in.")
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

# -------------------------------
# Login View
# -------------------------------
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('job_list')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# -------------------------------
# Logout View
# -------------------------------
def logout_view(request):
    logout(request)
    return redirect('index')
