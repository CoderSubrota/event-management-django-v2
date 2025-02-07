from django.contrib.auth.decorators import user_passes_test

# Helper function to check user roles
def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def is_organizer(user):
    return user.groups.filter(name='Organizer').exists()

def is_participant(user):
    return user.groups.filter(name='Participant').exists()

# Decorators for access control
def admin_required(view_func):
    return user_passes_test(is_admin, login_url='sign-in')(view_func)

def organizer_required(view_func):
    return user_passes_test(lambda u: is_admin(u) or is_organizer(u), login_url='sign-in')(view_func)

def participant_required(view_func):
    return user_passes_test(lambda u: is_admin(u) or is_organizer(u) or is_participant(u), login_url='sign-in')(view_func)
