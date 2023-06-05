from enum import Enum, auto
from django.contrib.auth.models import UserManager as DefaultUserManager
from django.contrib.auth.models import Permission, Group, AbstractUser
from django.db.models.signals import post_migrate
from django.db import models

class CustomUserManager(DefaultUserManager):
    def get_by_natural_key(self, username):
        return self.get(**{self.model.USERNAME_FIELD: username})


class CustomUser(AbstractUser):
    role = models.CharField(max_length=255, blank=True, null=True)


class ReportPermissions(Enum):
    CAN_CREATE_REPORT = 'core.can_create_report'
    CAN_EDIT_REPORT = 'core.can_edit_report'
    CAN_VIEW_REPORT = 'core.can_view_report'
    CAN_SAVE_REPORT = 'core.can_save_report'
    CAN_DELETE_REPORT = 'core.can_delete_report'
    CAN_ADD_REPORT = 'core.can_add_report'
    CAN_APPROVE_REPORT = 'core.can_approve_report'

    CAN_CREATE_TEMPLATE = 'core.can_create_template'
    CAN_EDIT_TEMPLATE = 'core.can_edit_template'
    CAN_VIEW_TEMPLATE = 'core.can_view_template'
    CAN_SAVE_TEMPLATE = 'core.can_save_template'
    CAN_DELETE_TEMPLATE = 'core.can_delete_template'
    CAN_ADD_TEMPLATE = 'core.can_add_template'
    CAN_APPROVE_TEMPLATE = 'core.can_approve_template'

    CAN_CREATE_CLIENT = 'core.can_create_client'
    CAN_EDIT_CLIENT = 'core.can_edit_client'
    CAN_VIEW_CLIENT = 'core.can_view_client'
    CAN_SAVE_CLIENT = 'core.can_save_client'
    CAN_DELETE_CLIENT = 'core.can_delete_client'
    CAN_ADD_CLIENT = 'core.can_add_client'
    CAN_APPROVE_CLIENT = 'core.can_approve_client'

    CAN_VIEW_MAIN = 'core.can_view_main'




class Report(models.Model):
    # Model fields
    
    class Meta:
            permissions = [
                (ReportPermissions.CAN_CREATE_REPORT.value, "can create report"),
                (ReportPermissions.CAN_EDIT_REPORT.value, "can edit report"),
                (ReportPermissions.CAN_VIEW_REPORT.value, "can view report"),
                (ReportPermissions.CAN_SAVE_REPORT.value, "can save report"),
                (ReportPermissions.CAN_DELETE_REPORT.value,  "can delete report"),
                (ReportPermissions.CAN_ADD_REPORT.value, "can add report"),
                (ReportPermissions.CAN_APPROVE_REPORT.value, "can approve report"),

                (ReportPermissions.CAN_CREATE_TEMPLATE.value, "can create template"),
                (ReportPermissions.CAN_EDIT_TEMPLATE.value, "can edit template"),
                (ReportPermissions.CAN_VIEW_TEMPLATE.value, "can view template"),
                (ReportPermissions.CAN_SAVE_TEMPLATE.value, "can save template"),
                (ReportPermissions.CAN_DELETE_TEMPLATE.value, "can delete template"),
                (ReportPermissions.CAN_ADD_TEMPLATE.value, "can add template"),
                (ReportPermissions.CAN_APPROVE_TEMPLATE.value, "can approve template"),

                (ReportPermissions.CAN_CREATE_CLIENT.value, "can create client"),
                (ReportPermissions.CAN_EDIT_CLIENT.value, "can edit client"),
                (ReportPermissions.CAN_VIEW_CLIENT.value, "can view client") ,
                (ReportPermissions.CAN_SAVE_CLIENT.value, "can save client") ,
                (ReportPermissions.CAN_DELETE_CLIENT.value, "can delete client"),
                (ReportPermissions.CAN_ADD_CLIENT.value, "can add client"),
                (ReportPermissions.CAN_APPROVE_CLIENT.value, "can approve client"),

                (ReportPermissions.CAN_VIEW_MAIN.value, "can view main"),

            ]


def create_groups(sender=None, **kwargs):
    print("Running create_groups")
    admin_permissions = Permission.objects.filter(
        content_type__app_label='core',
        codename__startswith='can_'
    )
    print(f"Admin permissions: {admin_permissions}")

    user_permissions = Permission.objects.filter(
        content_type__app_label='core',
        codename__in=[
            'can_view_report', 
            'can_add_report', 
            'can_edit_report',
            'can_view_template', 
            'can_add_template',
            'can_edit_template',
            'can_view_client', 
            'can_add_client', 
            'can_edit_client'
        ]
    )
    reviewer_permissions = Permission.objects.filter(
        content_type__app_label='core',
        codename__in=[
            'can_view_report',
            'can_approve_report',
            'can_view_template',
            'can_approve_template',
            'can_view_client',
            'can_approve_client'
        ]
    )
    tester_permissions = Permission.objects.filter(
        content_type__app_label='core',
        codename__in=[
            'can_view_report', 
            'can_add_report', 
            'can_edit_report', 
            'can_save_report',
            'can_view_template', 
            'can_add_template',
            'can_edit_template',
            'can_save_template',
            'can_view_client', 
            'can_add_client', 
            'can_edit_client', 
            'can_save_client'
        ]
    )

    admin_group, _ = Group.objects.get_or_create(name='Admin')
    admin_group.permissions.set(admin_permissions)

    user_group, _ = Group.objects.get_or_create(name='User')
    user_group.permissions.set(user_permissions)

    reviewer_group, _ = Group.objects.get_or_create(name='Reviewer')
    reviewer_group.permissions.set(reviewer_permissions)

    tester_group, _ = Group.objects.get_or_create(name='Tester')
    tester_group.permissions.set(tester_permissions)

post_migrate.connect(create_groups, sender=CustomUser)

