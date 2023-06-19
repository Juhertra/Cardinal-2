from django.test import TestCase, Client
from django.urls import reverse
from apps.core.models import CustomUser
from datetime import date, datetime
import json

from ..views import MainView, ClientsView, AddClientView, CreateReportTemplateView, GetTemplateDataView, \
    SaveReportTemplateView, LoadTemplateSectionsView, CancelTemplateView, SaveReportView, ReportFormView

from ..models import ReportTemplateLayout 


class ReportViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword', role='tester')
        self.client.login(username='testuser', password='testpassword')

    def test_main_view(self):
        url = reverse('main_report')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'report/main.html')

    def test_clients_view(self):
        url = reverse('clients')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'report/clients.html')

    def test_add_client_view(self):
        url = reverse('add_client')
        data = {
            'name': 'Test Client',
            'contact_person': 'John Doe',
            'email': 'test@example.com',
            'phone': '1234567890',
            'address': 'Test Address',
            'start_date': datetime.now().strftime('%Y-%m-%d')
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        response_data = json.loads(response.content)
        self.assertEqual(response_data['client']['name'], 'Test Client')

    def test_create_report_template_view(self):
        url = reverse('create_report_template')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'report/report_template.html')

    def test_get_template_data_view(self):
        template = ReportTemplateLayout.objects.create(user=self.user)
        url = reverse('get_template_data', args=[template.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        response_data = json.loads(response.content)
        self.assertIn('sections', response_data)

    def test_save_report_template_view(self):
        url = reverse('save_report_template')
        data = {
            'section_order': json.dumps(['section1', 'section2']),
            'template_name': 'Test Template'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        response_data = json.loads(response.content)
        self.assertEqual(response_data['status'], 'success')

    def test_load_template_sections_view(self):
        template = ReportTemplateLayout.objects.create(user=self.user)
        url = reverse('load_template_sections', args=[template.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        response_data = json.loads(response.content)
        self.assertIn('sections', response_data)

    def test_cancel_template_view(self):
        url = reverse('cancel_template')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('create_report_template'))

    def test_save_report_view(self):
        url = reverse('save_report')
        data = {
            'name': 'Test Report',
            'description': 'Test Description',
            'sections': {}
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])

    def test_report_form_view(self):
        url = reverse('create_report')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'report/reports.html')

    def test_report_form_view_with_template(self):
        template = ReportTemplateLayout.objects.create(user=self.user)
        url = reverse('create_report_with_template', args=[template.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'report/reports.html')

    def test_report_form_view_post(self):
        url = reverse('create_report')
        data = {
            'name': 'Test Report',
            'description': 'Test Description',
            'sections': {}
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/success/')  # Replace '/success/' with the desired URL