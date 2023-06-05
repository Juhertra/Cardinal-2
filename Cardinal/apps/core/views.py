from django.views import View
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.contrib.auth.models import Group

from apps.report.models import Client, ReportDataFiller, Vulnerability
from .forms import CustomUserCreationForm

from django.db.models import Count, Case, When, IntegerField

from django.contrib.auth import login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm



from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.db.models import Count, Case, When, IntegerField
from apps.report.models import Client, ReportDataFiller, Vulnerability

# class HomePageView(LoginRequiredMixin, View):
#     template_name = 'base.html'

#     def get(self, request, *args, **kwargs):
#         if request.user.is_authenticated:
#             # Fetch the reports and clients with a single query each
#             reports = ReportDataFiller.objects.filter(user=request.user)
#             clients = Client.objects.filter(user=request.user)

#             # Fetch the count of vulnerabilities directly with a single query
#             vulnerability_counts = Vulnerability.objects.filter(ReportDataFiller__user=request.user).aggregate(
#                 num_total_vulnerabilities=Count('id'),
#                 num_critical_vulnerabilities=Count(Case(When(severity='Critical', then=1), output_field=IntegerField())),
#                 num_high_vulnerabilities=Count(Case(When(severity='High', then=1), output_field=IntegerField())),
#                 num_medium_vulnerabilities=Count(Case(When(severity='Medium', then=1), output_field=IntegerField())),
#                 num_low_vulnerabilities=Count(Case(When(severity='Low', then=1), output_field=IntegerField())),
#             )

#             context = {  
#                 'num_reports': reports.count(),  
#                 'num_clients': clients.count(),
#                 'num_vulnerabilities': vulnerability_counts['num_total_vulnerabilities'],
#                 'num_critical_vulnerabilities': vulnerability_counts['num_critical_vulnerabilities'],
#                 'num_high_vulnerabilities': vulnerability_counts['num_high_vulnerabilities'],
#                 'num_medium_vulnerabilities': vulnerability_counts['num_medium_vulnerabilities'],
#                 'num_low_vulnerabilities': vulnerability_counts['num_low_vulnerabilities'],
#                 'most_vulnerabilities_client': vulnerability_counts.get('most_vulnerabilities_client', None),
#                 'most_critical_vulnerabilities_client': vulnerability_counts.get('most_critical_vulnerabilities_client', None),
#                 'most_high_vulnerabilities_client': vulnerability_counts.get('most_high_vulnerabilities_client', None),
#                 'most_medium_vulnerabilities_client': vulnerability_counts.get('most_medium_vulnerabilities_client', None),
#                 'most_low_vulnerabilities_client': vulnerability_counts.get('most_low_vulnerabilities_client', None),
#                 'clients': clients,
#             }
#         else:
#             context = {}

#         return render(request, self.template_name, context)

from django.views import View
from django.shortcuts import render

class HomePageView(View):
    template_name = 'base.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)



class MainView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'base.html')


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return redirect('main')


class ContactView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'core/contact.html')


class CustomLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = 'core/registration/login.html'
    success_url = reverse_lazy('base.html')

    def get_success_url(self):
        return reverse('main')


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'core/registration/signup.html'
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()

        # Assign the selected roles to the user
        roles = self.request.POST.getlist('roles')
        for role in roles:
            group = Group.objects.get(pk=role)
            user.groups.add(group)
        
        # Set the user's role based on their first group
        if user.groups.exists():
            user.role = user.groups.all()[0].name
            user.save()

        login(self.request, user)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['roles'] = Group.objects.all()
        return context
