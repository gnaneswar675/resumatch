from django.shortcuts import render, redirect, get_object_or_404
from .models import Applicant, FraudCheck
from .forms import SignupForm, ResumeFraudForm, ApplicantForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
import os
from .static_jobs import STATIC_JOBS

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
    form = ApplicantForm()
    return render(request, 'joblist.html', {'form': form, 'jobs': STATIC_JOBS})

# -------------------------------
# Job Application View
# -------------------------------
def apply_job(request, job_id):
    # Find the job from STATIC_JOBS based on the job_id
    job = next((job for job in STATIC_JOBS if job['id'] == job_id), None)

    if job is None:
        return redirect('job_list')  # Redirect to the job list if job is not found

    if request.method == 'POST':
        form = ApplicantForm(request.POST, request.FILES)
        if form.is_valid():
            applicant = form.save(commit=False)
            applicant.job_title = job['title']  # Assign the job title to the applicant
            applicant.save()
            return redirect('result_view', pk=applicant.id)  # Redirect to the result view for eligibility check
    else:
        form = ApplicantForm()

    context = {
        'form': form,
        'job': job,  # Pass job data to the form
    }
    return render(request, 'apply_job.html', context)

# -------------------------------
# Scoreboard View
# -------------------------------
def scoreboard_view(request, job_id):
    job = next((job for job in STATIC_JOBS if job['id'] == job_id), None)
    if not job:
        return render(request, '404.html', status=404)

    # Fetch applicants who are eligible and order them by their score
    eligible_applicants = Applicant.objects.filter(
        job_title=job["title"], is_eligible=True
    ).order_by('-score')

    return render(request, 'scoreboard.html', {
        'job': job,
        'applicants': eligible_applicants
    })

# -------------------------------
# Application Result View (Eligibility & Score Calculation)
# -------------------------------
def result_view(request, pk):
    applicant = get_object_or_404(Applicant, pk=pk)
    job = next((job for job in STATIC_JOBS if job['title'] == applicant.job_title), None)

    if not job:
        return render(request, '404.html', status=404)

    resume_path = applicant.resume.path
    resume_text = extract_text_from_resume(resume_path)

    # Check eligibility and score
    eligible, score = check_eligibility_and_score(resume_text, job["description"])
    skill_gaps = analyze_skill_gap(resume_text, job["description"])
    learning_resources = get_learning_resources(skill_gaps)

    # Update the applicant with the eligibility and score
    applicant.is_eligible = eligible
    applicant.score = score
    applicant.save()  # Save updated applicant details

    recommended_jobs = recommend_jobs_for_resume(resume_text, STATIC_JOBS)

    return render(request, "result.html", {
        "applicant": applicant,
        "job": job,
        "eligible": eligible,
        "score": score,
        "recommended_jobs": recommended_jobs,
        "skill_gaps": skill_gaps,
        "learning_resources": learning_resources,
    })
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
