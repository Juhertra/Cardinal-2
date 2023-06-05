from enum import Enum

class Role(Enum):
    ADMIN = "Admin"
    USER = "User"

CHOICES = [(role.value, role.value) for role in Role]

def is_admin(user):
    return user.groups.filter(name=Role.ADMIN.value).exists()

def is_user(user):
    return user.groups.filter(name=Role.USER.value).exists()

def is_tester(user):
    return user.groups.filter(name='Tester').exists()

def is_reviewer(user):
    return user.groups.filter(name='Reviewer').exists()
