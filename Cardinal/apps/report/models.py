from datetime import date
from django.conf import settings
from django.utils import timezone
from django.db import models
from django.db.models import JSONField

IN_PROGRESS = 'in_progress'
PENDING_REVIEW = 'pending_review'
COMPLETED = 'completed'
STATUS_CHOICES = [
    (IN_PROGRESS, 'In Progress'),
    (PENDING_REVIEW, 'Pending Review'),
    (COMPLETED, 'Completed')
]

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural="Categories"

    def __str__(self):
        return self.name

class Vulnerability(models.Model):
    category = models.ForeignKey(Category, related_name='vulnerabilities', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    severity = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)
    mitigation = models.TextField(blank=True)
    date_found = models.DateTimeField(default=timezone.now)
    date_fixed = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name_plural="Vulnerabilities"

    def __str__(self):
        return self.name

class Client(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    start_date = models.DateField()

    class Meta:
        verbose_name_plural="Clients"

    def __str__(self):
            return self.name
    @property
    def days_since_start(self):
        return (date.today() - self.start_date).days

class ReportTemplateLayout(models.Model):
    name = models.CharField(max_length=255)
    section_order = JSONField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    custom_sections = models.TextField(blank=True)

    def __str__(self):
        return f'Report Template for user {self.user.username} - {self.name}'

class Attachment(models.Model):
    report = models.ForeignKey('ReportDataFiller', on_delete=models.CASCADE)
    file = models.FileField(upload_to='report_attachments/')

class ExecutiveSummary(models.Model):
    report = models.OneToOneField('ReportDataFiller', on_delete=models.CASCADE)
    summary = models.TextField()

class ReportSummary(models.Model):
    report = models.OneToOneField('ReportDataFiller', on_delete=models.CASCADE)
    summary = models.TextField()

class Tool(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural="Tools"

    def __str__(self):
        return self.name

class TestedEnvironment(models.Model):
    environment = models.TextField()

class Conclusion(models.Model):
    text = models.TextField()

class Tester(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural="Testers"

    def __str__(self):
        return self.user.username

class Reviewer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural="Reviewers"

    def __str__(self):
        return self.user.username

class Review(models.Model):
    report = models.ForeignKey('ReportDataFiller', on_delete=models.CASCADE)
    reviewer = models.ForeignKey(Reviewer, on_delete=models.PROTECT, related_name='reviews')
    date = models.DateTimeField()
    comment = models.TextField()


# Fill the actual data in the reports
class ReportDataFiller(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('pending_review', 'Pending Review'),
        ('completed', 'Completed')
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    report_name = models.CharField(max_length=255)
    report_description = models.TextField(blank=True)
    report_sections = JSONField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=IN_PROGRESS)
    approval = models.BooleanField()
    tester = models.OneToOneField(Tester, on_delete=models.CASCADE)
    reviewer = models.OneToOneField(Reviewer, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    version = models.IntegerField(default=1)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.report_name} by {self.user.username}'
