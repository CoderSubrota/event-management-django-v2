from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth import authenticate, logout,login
from users.forms import SignUpForm, AssignRoleForm, CreateGroupForm,Add_Participant
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from events.models import Add_Event_Model

# ------------------
def is_organizer(user):
    return user.groups.filter(name='Organizer').exists()

def is_admin(user):
    if user.is_authenticated:
        return user.groups.filter(name='Admin').exists()
    else:
        print(f"User {user} is not authenticated")
        return False

def is_participant(user):
    return user.groups.filter(name='Participant').exists()
# ---------------------- 
def sign_up(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.is_active = False 
            user.save()
            messages.success(request, "A confirmation mail has been sent. Please check your email.")
            return redirect("sign-in") 
        else:
            
            return render(request, 'registration/sign-up.html', {
                'form': form, 
                'message': 'Please follow the instructions and fix the errors in the form.'
            })
    else:
        form = SignUpForm()

    return render(request, 'registration/sign-up.html', {'form': form})

# add participant 

def add_participant(request):
    if request.method == "POST":
        form = Add_Participant(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.is_active = False 
            user.save()
            messages.success(request, "A confirmation mail has been sent. Please check your email.")
            return redirect("sign-in") 
        else:
            
            return render(request, 'registration/add_participant.html', {
                'form': form, 
                'message': 'Please follow the instructions and fix the errors in the form.'
            })
    else:
        form = Add_Participant()

    return render(request, 'registration/add_participant.html', {'form': form})


def sign_in(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user) 
            return redirect("home")
        else:
            return render(request, 'registration/sign-in.html', {'message': 'Invalid credential'})
    return render(request, 'registration/sign-in.html')


@login_required(login_url="sign-in")
def sign_out(request):
    if request.method == "POST":
        logout(request)
        return redirect("sign-in")

def activate_account(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect("sign-in")
        else:
            return HttpResponse("<p style='color:red;'>Invalid token</p>")
    except User.DoesNotExist:
        return HttpResponse("<p style='color:red;'>User not found</p>")

@login_required(login_url="sign-in")
@user_passes_test(is_admin, login_url='sign-in')
def assign_role(request, user_id):
    user = get_object_or_404(User, id=user_id)
    form = AssignRoleForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        role_name = form.cleaned_data.get("role")
        group = get_object_or_404(Group, name=role_name)
        user.groups.clear()
        user.groups.add(group)
        messages.success(request, f"User {user.username} has been assigned to the {group.name} role.")
        return redirect("admin_dashboard")
    return render(request, "admin/assign_role.html", {"form": form, "user": user})

@login_required(login_url="sign-in") 
@user_passes_test(is_admin, login_url="sign-in")
def admin_dashboard(request):
    users = User.objects.all()
    return render(request, "admin/dashboard.html", {'users': users})


@login_required(login_url="sign-in")
@user_passes_test(is_admin, login_url='sign-in') 
def create_group(request):
    form = CreateGroupForm()
    if request.method == "POST":
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success(request, f"Group {group.name} has been created successfully")
            return redirect("create-group")
    return render(request, "admin/create_group.html", {"form": form})


@login_required(login_url="sign-in")
@user_passes_test(is_admin, login_url='sign-in') 
def group_list(request):
    groups = Group.objects.all()
    return render(request, "admin/group_list.html", {'groups': groups})

@login_required
@user_passes_test(lambda u: is_admin(u) or is_organizer(u) or is_participant(u), login_url='sign-in')
def view_events(request):
    return render(request, "events/event_list.html")

@login_required
@user_passes_test(is_admin, login_url='sign-in')
def send_email(request):
    subject = "Welcome to My Website"
    message = "Thank you for signing up!"
    recipient_list = ["kepoy83095@andinews.com"]
    send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list, fail_silently=False)
    return render(request, "email_sent.html", {"message": "Email sent successfully!"})

@login_required
@user_passes_test(is_admin, login_url='sign-in')
def manage_users(request):
    return render(request, "admin/dashboard.html")

@login_required
@user_passes_test(is_organizer, login_url='sign-in')
def create_event(request):
    return render(request, "events/add_event.html")

@login_required
@user_passes_test(is_participant or is_admin or is_organizer, login_url='sign-in')
def show_event_list(request):
    events = Add_Event_Model.objects.all()
    return render(request,'show_event_list.html',{'events':events})
