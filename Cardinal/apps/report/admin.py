from django.contrib import admin
from .models import (Attachment, Category, Client, Conclusion,
                     ExecutiveSummary, ReportDataFiller, ReportSummary,
                     ReportTemplateLayout, Review, Reviewer, TestedEnvironment,
                     Tester, Tool, Vulnerability)

# Register your models here.
admin.site.register(Attachment)
admin.site.register(Category)
admin.site.register(Client)
admin.site.register(Conclusion)
admin.site.register(ExecutiveSummary)
admin.site.register(ReportDataFiller)
admin.site.register(ReportSummary)
admin.site.register(ReportTemplateLayout)
admin.site.register(Review)
admin.site.register(Reviewer)
admin.site.register(TestedEnvironment)
admin.site.register(Tester)
admin.site.register(Tool)
# admin.site.register(User)
admin.site.register(Vulnerability)

