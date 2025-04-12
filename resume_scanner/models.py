from django.db import models

class Job(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title


class Applicant(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    resume = models.FileField(upload_to='resumes/')
    submitted_at = models.DateTimeField(auto_now_add=True)
    resume_text = models.TextField(blank=True, null=True)

    # ML output fields
    is_eligible = models.BooleanField(default=False)
    score = models.FloatField(null=True, blank=True)

    is_fraud = models.BooleanField(default=False)
    skill_gap = models.JSONField(blank=True, null=True)
    course_links = models.JSONField(blank=True, null=True)
    recommendations = models.JSONField(blank=True, null=True)
    recommended_resources = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.job.title}"


class FraudCheck(models.Model):
    resume = models.FileField(upload_to='fraud_check/')
    result = models.BooleanField()  # True = Fraud, False = Genuine
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.resume.name} - {'Fraud' if self.result else 'Genuine'}"
