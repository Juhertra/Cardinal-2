from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

import json
import os
import logging
from datetime import datetime

from .forms import ReportForm
from apps.core.models import ReportPermissions
from .models import (Attachment, Category, Client, Conclusion,
                     ExecutiveSummary, ReportSummary,
                     ReportTemplateLayout, Review, Reviewer,
                     TestedEnvironment, Tester, Tool, Vulnerability,
                     ReportDataFiller)

logger = logging.getLogger(__name__)

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path = os.path.join(PROJECT_ROOT, "report", "json", "default_template.json")

def load_default_template():
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        logger.error(f"Default template file not found at {file_path}")
        return {}


default_template = load_default_template()


class MainView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = 'login'
    permission_required = ReportPermissions.CAN_VIEW_MAIN.value

    def get(self, request):
        return render(request, 'report/main.html')


class ClientsView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = 'login'
    permission_required = ReportPermissions.CAN_VIEW_CLIENT.value

    def get(self, request):
        try:
            clients = Client.objects.filter(user=request.user)

            context = {
                'clients': clients
            }
            return render(request, 'report/clients.html', context)
        except Client.DoesNotExist:
            logger.error(f"Client with id {request.user} does not exist")
            return JsonResponse({"error": f"Client with id {request.user} does not exist."}, status=404)


class AddClientView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = 'login'
    permission_required = ReportPermissions.CAN_ADD_CLIENT.value

    def post(self, request):
        try:
            name = request.POST.get('name')
            contact_person = request.POST.get('contact_person')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            address = request.POST.get('address')
            start_date_str = request.POST.get('start_date', '')
            if not start_date_str:
                raise ValueError("Start date is required.")

            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()

            logger.debug(f"Received data: {name}, {contact_person}, {email}, {phone}, {address}")

            new_client = Client(
                user=request.user,
                name=name,
                contact_person=contact_person,
                email=email,
                phone=phone,
                address=address,
                start_date=start_date
            )
            new_client.save()

            logger.info(f"New client saved with ID: {new_client.id}")

            response_data = {
                'client': {
                    'id': new_client.id,
                    'name': new_client.name,
                    'contact_person': new_client.contact_person,
                    'email': new_client.email,
                    'phone': new_client.phone,
                    'address': new_client.address,
                }
            }
            return JsonResponse(response_data)

        except ValueError as ve:
            logger.error(f"Error while parsing start_date: {str(ve)}")
            return JsonResponse({"error": "Invalid start_date format. Please use YYYY-MM-DD."}, status=400)
        except Exception as e:
            logger.error(f"Error while saving client data: {str(e)}")
            return JsonResponse({"error": "Error occurred while saving client data."}, status=400)


class CreateReportTemplateView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = 'login'
    permission_required =  ReportPermissions.CAN_CREATE_REPORT.value

    def get(self, request):
        """
        View to create a report template. Users must have the 'can_create_report' permission to access this view
        """
        available_templates = ReportTemplateLayout.objects.filter(user=request.user)
        default_template = load_default_template()
        context = {
            'default_template': default_template,
            'available_templates': available_templates,
        }
        return render(request, 'report/report_template.html', context)


class GetTemplateDataView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = 'login'
    permission_required = ReportPermissions.CAN_VIEW_TEMPLATE.value

    def get(self, request, template_id):
        """
        Function to get the template data based on a given template id
        """
        try:
            template = ReportTemplateLayout.objects.get(id=template_id)
            sections = {}

            for section_id in template.section_order:
                if section_id in default_template:
                    sections[section_id] = default_template[section_id]
                else:
                    sections[section_id] = {
                        'name': section_id,
                        'fields': {},
                    }

            data = {
                "sections": sections,
                "custom_sections": template.custom_sections,
            }
            return JsonResponse(data)
        except ReportTemplateLayout.DoesNotExist:
            logger.error(f"ReportTemplateLayout with id {template_id} does not exist")
            return JsonResponse({"error": f"ReportTemplateLayout with id {template_id} does not exist."}, status=404)


class SaveReportTemplateView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = 'login'
    permission_required = ReportPermissions.CAN_SAVE_TEMPLATE.value

    def post(self, request):
        logger.info(f"User authenticated: {request.user.is_authenticated}")
        logger.info(f"User has permission: {request.user.has_perm('core.can_save_template')}")
        logger.info(f"Required permissions: {self.get_permission_required()}")

        """
        View to save a report template. Users must have the 'can_save_report' permission to access this view
        """
        if request.method == 'POST':
            try:
                # Get the template data from the request
                section_order = json.loads(request.POST.get('section_order'))
                if not section_order:
                    raise ValueError("Section order is required.")

                user = request.user
                # Get custom sections from the section_order
                custom_sections = [section for section in section_order if section not in default_template]

                # Create a new ReportTemplateLayout instance and set the fields
                template = ReportTemplateLayout()
                # Save custom sections as JSON in the ReportTemplateLayout instance
                template.custom_sections = json.dumps(custom_sections)
                template.section_order = section_order
                template.user = user
                template.name = request.POST.get('template_name')  # Add this line to set the template name
                template.save()

                logger.info(f"Saved new report template with ID: {template.id}")
                return JsonResponse({'status': 'success', 'message': 'Template saved successfully'})
            except ValueError as ve:
                logger.error(f"Error while saving report template: {str(ve)}")
                return JsonResponse({'status': 'error', 'message': 'Invalid request data'}, status=400)
            except Exception as e:
                logger.error(f"Error while saving report template: {str(e)}")
                return JsonResponse({'status': 'error', 'message': 'Unexpected error occurred.'}, status=400)
        else:
            logger.warning("Received non-POST request in save_report_template")

            return HttpResponseNotAllowed(['POST'])


class LoadTemplateSectionsView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = 'login'
    permission_required = ReportPermissions.CAN_CREATE_REPORT.value

    @staticmethod
    def get_template_sections(template_id, user):
        """
        Function to load the template sections based on a given template id.
        """
        try:
            report_template = ReportTemplateLayout.objects.get(id=template_id, user=user)
            sections = report_template.section_order
            custom_sections = report_template.custom_sections
            return {'sections': sections, 'custom_sections': custom_sections}
        except ReportTemplateLayout.DoesNotExist:
            logger.error(f"ReportTemplateLayout with id {template_id} does not exist")
            return {'error': f"ReportTemplateLayout with id {template_id} does not exist."}

    def get(self, request, template_id):
        return JsonResponse(self.get_template_sections(template_id, request.user))



class CancelTemplateView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = 'login'
    permission_required = ReportPermissions.CAN_SAVE_TEMPLATE.value

    def get(self, request):
        """
        View for cancelling the template creation and redirecting to the create_report_template view.
        """
        logger.info("Template creation cancelled, redirecting to create_report_template view")
        return redirect('create_report_template')


class SaveReportView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = 'login'
    permission_required = ReportPermissions.CAN_SAVE_REPORT.value

    def post(self, request):
        """
        View to save a report. Accepts only POST requests.
        """
        logger.info("Received request to save report")
        if request.method == "POST":
            try:
                data = json.loads(request.body)
                if not data:
                    raise ValueError("Request data is required.")

                report_name = data.get("name")
                if not report_name:
                    raise ValueError("Report name is required.")

                report_description = data.get("description", "")
                report_sections = data.get("sections")

                if not report_sections:
                    raise ValueError("Report sections are required.")

                # Check if the report name already exists
                existing_report = ReportDataFiller.objects.filter(user=request.user, report_name=report_name).first()

                if existing_report:
                    # Update the existing report
                    existing_report.report_name = report_name
                    existing_report.report_description = report_description
                    existing_report.report_sections = report_sections
                    existing_report.save()
                    logger.info(f"Report updated with ID: {existing_report.id}")
                    return JsonResponse({"success": True, "exists": True})
                else:
                    # Save the new report
                    new_report = ReportDataFiller(
                        user=request.user,
                        report_name=report_name,
                        report_description=report_description,
                        report_sections=report_sections
                    )
                    new_report.save()
                    logger.info(f"Saved new report with ID: {new_report.id}")
                    return JsonResponse({"success": True, "exists": False})
            except ValueError as ve:
                logger.error(f"Error while saving report: {str(ve)}")
                return JsonResponse({"success": False, "error": str(ve)}, status=400)
            except Exception as e:
                logger.error(f"Error while saving report: {str(e)}")
                return JsonResponse({"success": False, "error": "Unexpected error occurred."}, status=400)

        logger.warning("Received non-POST request in save_report")
        return JsonResponse({"success": False})


class ReportFormView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = 'login'
    permission_required = ReportPermissions.CAN_CREATE_REPORT.value

    def get(self, request, template_id=None):
        """
        View to handle report form submission. Users must have the 'can_create_report' permission to access this view.
        """
        categories = Category.objects.all()
        clients = Client.objects.all()
        vulnerabilities = Vulnerability.objects.all()
        attachments = Attachment.objects.all()
        executive_summaries = ExecutiveSummary.objects.all()
        report_summaries = ReportSummary.objects.all()
        tools = Tool.objects.all()
        tested_environments = TestedEnvironment.objects.all()
        conclusions = Conclusion.objects.all()
        testers = Tester.objects.all()
        reviewers = Reviewer.objects.all()
        reviews = Review.objects.all()

        # Check if the default report template exists, and create it if it doesn't
        report_template = LoadTemplateSectionsView.get_template_sections(template_id, request.user)
        
        if request.method == 'POST':
            try:
                form = ReportForm(request.POST)
                if form.is_valid():
                    new_report = form.save(commit=False)
                    new_report.custom_fields = request.POST['custom_fields']
                    new_report.fields_order = request.POST['fields_order']
                    new_report.save()
                    form.save_m2m()  # This is needed to save ManyToMany fields
                    
                    logger.info(f"New report form saved with ID: {new_report.id}")
                    return HttpResponseRedirect('/success/')  # Replace '/success/' with the desired URL
                else:
                    raise ValueError("Invalid form data.")
            except ValueError as ve:
                logger.error(f"Error while saving report form: {str(ve)}")
                return HttpResponse(f"Error while saving report form: {str(ve)}", status=400)
        else:
            form = ReportForm()
        
        context = {
            'form': form,
            'categories': categories,
            'clients': clients,
            'vulnerabilities': vulnerabilities,
            'report_templates': ReportTemplateLayout.objects.filter(user=request.user),
            'attachments': attachments,
            'executive_summaries': executive_summaries,
            'report_summaries': report_summaries,
            'tools': tools,
            'tested_environments': tested_environments,
            'conclusions': conclusions,
            'testers': testers,
            'reviewers': reviewers,
            'reviews': reviews,
            'report_template': report_template,
        }
        return render(request, 'report/reports.html', context)
