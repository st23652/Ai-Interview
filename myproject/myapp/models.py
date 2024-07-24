from django.db import models

class Job(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=100)

class Candidate(models.Model):
    name = models.CharField(max_length=100)
    resume = models.FileField(upload_to='resumes/')
    parsed_resume = models.JSONField(null=True, blank=True)

class Interview(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    scheduled_time = models.DateTimeField()
    transcript = models.TextField(null=True, blank=True)
    emotional_state = models.JSONField(null=True, blank=True)
    cheating_detected = models.BooleanField(default=False)
    noise_reduction_applied = models.BooleanField(default=False)

    def __str__(self):
        return self.title
