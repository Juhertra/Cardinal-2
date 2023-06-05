from django.urls import path
from . import views

urlpatterns = [
    path('main_report', views.MainView.as_view(), name='main_report'),
    path('create_report/', views.ReportFormView.as_view(), name='create_report'),
    path('create_report/<int:template_id>/', views.ReportFormView.as_view(), name='create_report_with_template'),
    path('save_report/', views.SaveReportView.as_view(), name='save_report'),
    path('create_report_template/', views.CreateReportTemplateView.as_view() , name='create_report_template'),
    path('load_template_sections/<int:template_id>/', views.LoadTemplateSectionsView.as_view(), name='load_template_sections'),
    path('get_template_data/<int:template_id>/', views.GetTemplateDataView.as_view(), name='get_template_data'),
    path('save_report_template/', views.SaveReportTemplateView.as_view(), name='save_report_template'),
    path('cancel_template/', views.CancelTemplateView.as_view(), name='cancel_template'),
    # path('add_client_view/', views.add_client_view, name='add_client_view'),
    path('add_client/', views.AddClientView.as_view(), name='add_client'),
    path('clients/', views.ClientsView.as_view(), name='clients'),
]

