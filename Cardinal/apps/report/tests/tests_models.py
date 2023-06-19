from django.test import TestCase
from apps.core.models import CustomUser

from ..models import Category, Vulnerability, Client, ReportTemplateLayout, Attachment, ExecutiveSummary, \
    ReportSummary, Tool, TestedEnvironment, Conclusion, Tester, Reviewer, Review, ReportDataFiller


class ReportModelsTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword', role='tester')

    def test_client_model(self):
        client = Client.objects.create(user=self.user, name='Test Client')
        self.assertEqual(str(client), 'Test Client')

    def test_report_template_layout_model(self):
        template = ReportTemplateLayout.objects.create(user=self.user)
        self.assertEqual(str(template), f'ReportTemplateLayout {template.id}')

    def test_report_data_filler_model(self):
        report = ReportDataFiller.objects.create(user=self.user, report_name='Test Report')
        self.assertEqual(str(report), f'ReportDataFiller {report.id}')


class ModelTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword', role='tester')

    def test_category_model(self):
        category = Category.objects.create(name='Test Category')
        self.assertEqual(str(category), 'Test Category')

    def test_vulnerability_model(self):
        category = Category.objects.create(name='Test Category')
        vulnerability = Vulnerability.objects.create(category=category, name='Test Vulnerability')
        self.assertEqual(str(vulnerability), 'Test Vulnerability')

    def test_attachment_model(self):
        client = Client.objects.create(user=self.user, name='Test Client')
        report = ReportDataFiller.objects.create(user=self.user, client=client, report_name='Test Report')
        attachment = Attachment.objects.create(report=report)
        self.assertEqual(str(attachment), f'Attachment {attachment.id}')

    def test_executive_summary_model(self):
        client = Client.objects.create(user=self.user, name='Test Client')
        report = ReportDataFiller.objects.create(user=self.user, client=client, report_name='Test Report')
        summary = ExecutiveSummary.objects.create(report=report)
        self.assertEqual(str(summary), f'ExecutiveSummary {summary.id}')

    def test_report_summary_model(self):
        client = Client.objects.create(user=self.user, name='Test Client')
        report = ReportDataFiller.objects.create(user=self.user, client=client, report_name='Test Report')
        summary = ReportSummary.objects.create(report=report)
        self.assertEqual(str(summary), f'ReportSummary {summary.id}')

    def test_tool_model(self):
        tool = Tool.objects.create(name='Test Tool')
        self.assertEqual(str(tool), 'Test Tool')

    def test_tested_environment_model(self):
        environment = TestedEnvironment.objects.create(environment='Test Environment')
        self.assertEqual(str(environment), 'Test Environment')

    def test_conclusion_model(self):
        conclusion = Conclusion.objects.create(text='Test Conclusion')
        self.assertEqual(str(conclusion), 'Test Conclusion')

    def test_tester_model(self):
        tester = Tester.objects.create(user=self.user)
        self.assertEqual(str(tester), self.user.username)

    def test_reviewer_model(self):
        reviewer = Reviewer.objects.create(user=self.user)
        self.assertEqual(str(reviewer), self.user.username)

    def test_review_model(self):
        client = Client.objects.create(user=self.user, name='Test Client')
        report = ReportDataFiller.objects.create(user=self.user, client=client, report_name='Test Report')
        reviewer = Reviewer.objects.create(user=self.user)
        review = Review.objects.create(report=report, reviewer=reviewer, date=date.today())
        self.assertEqual(str(review), f'Review {review.id}')

    def test_report_data_filler_model(self):
        client = Client.objects.create(user=self.user, name='Test Client')
        tester = Tester.objects.create(user=self.user)
        reviewer = Reviewer.objects.create(user=self.user)
        report = ReportDataFiller.objects.create(
            user=self.user,
            client=client,
            report_name='Test Report',
            tester=tester,
            reviewer=reviewer
        )
        self.assertEqual(str(report), 'Test Report by testuser')
