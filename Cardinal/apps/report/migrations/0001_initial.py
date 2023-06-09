# Generated by Django 4.2 on 2023-05-03 13:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Attachment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("file", models.FileField(upload_to="report_attachments/")),
            ],
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
            ],
            options={
                "verbose_name_plural": "Categories",
            },
        ),
        migrations.CreateModel(
            name="Client",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("contact_person", models.CharField(max_length=255)),
                ("email", models.EmailField(max_length=254)),
                ("phone", models.CharField(max_length=20)),
                ("address", models.TextField()),
                ("start_date", models.DateField()),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Clients",
            },
        ),
        migrations.CreateModel(
            name="Conclusion",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="ExecutiveSummary",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("summary", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="ReportDataFiller",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("custom_fields", models.TextField(blank=True, null=True)),
                ("fields_order", models.TextField(blank=True, null=True)),
                ("version", models.IntegerField(default=1)),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_modified", models.DateTimeField(auto_now=True)),
                ("scope", models.TextField()),
                ("methodology", models.TextField()),
                ("recommendations", models.TextField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("in_progress", "In Progress"),
                            ("pending_review", "Pending Review"),
                            ("completed", "Completed"),
                        ],
                        max_length=20,
                    ),
                ),
                ("approval", models.BooleanField()),
                ("is_published", models.BooleanField(default=False)),
                ("attachments", models.ManyToManyField(to="report.attachment")),
                (
                    "client",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="report.client"
                    ),
                ),
                (
                    "conclusion",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="report.conclusion",
                    ),
                ),
                (
                    "executive_summary",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="report.executivesummary",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TestedEnvironment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("environment", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="Tool",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
            ],
            options={
                "verbose_name_plural": "Tools",
            },
        ),
        migrations.CreateModel(
            name="Vulnerability",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("severity", models.CharField(blank=True, max_length=20, null=True)),
                ("description", models.TextField(null=True)),
                ("mitigation", models.TextField(null=True)),
                ("date_found", models.DateTimeField(default=django.utils.timezone.now)),
                ("date_fixed", models.DateTimeField(blank=True, null=True)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="vulnerabilities",
                        to="report.category",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Vulnerabilities",
            },
        ),
        migrations.CreateModel(
            name="Tester",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Testers",
            },
        ),
        migrations.CreateModel(
            name="Reviewer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Reviewers",
            },
        ),
        migrations.CreateModel(
            name="Review",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateTimeField()),
                ("comment", models.TextField()),
                (
                    "report",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="report.reportdatafiller",
                    ),
                ),
                (
                    "reviewer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="reviews",
                        to="report.reviewer",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ReportTemplateLayout",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("section_order", models.JSONField()),
                ("custom_sections", models.TextField(blank=True, null=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ReportSummary",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("summary", models.TextField()),
                (
                    "report",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="report.reportdatafiller",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="reportdatafiller",
            name="report_summary",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to="report.reportsummary"
            ),
        ),
        migrations.AddField(
            model_name="reportdatafiller",
            name="reviewer",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to="report.reviewer"
            ),
        ),
        migrations.AddField(
            model_name="reportdatafiller",
            name="tested_environment",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                to="report.testedenvironment",
            ),
        ),
        migrations.AddField(
            model_name="reportdatafiller",
            name="tester",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to="report.tester"
            ),
        ),
        migrations.AddField(
            model_name="reportdatafiller",
            name="tools_used",
            field=models.ManyToManyField(to="report.tool"),
        ),
        migrations.AddField(
            model_name="reportdatafiller",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="reportdatafiller",
            name="vulnerabilities",
            field=models.ManyToManyField(to="report.vulnerability"),
        ),
        migrations.AddField(
            model_name="executivesummary",
            name="report",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                to="report.reportdatafiller",
            ),
        ),
        migrations.AddField(
            model_name="attachment",
            name="report",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="report.reportdatafiller",
            ),
        ),
    ]
