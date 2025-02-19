from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import Group
from django.contrib.auth import login, logout
from users.forms import CustomRegistrationForm, AssignRoleForm, CreateGroupForm, CustomPasswordChangeForm, CustomPasswordResetForm, CustomPasswordResetConfirmForm, EditProfileForm
from django.contrib import messages
from django.contrib import messages
from users.forms import LoginForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Prefetch
from django.contrib.auth.views import  LoginView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.views.generic import TemplateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from users.models import CustomUser
from django.views.generic import CreateView,ListView
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views import View

CustomUser = get_user_model()

class EditProfileView(UpdateView):
    model = CustomUser
    form_class = EditProfileForm
    template_name = 'accounts/update_profile.html'
    context_object_name = 'form'

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        form.save()
        return redirect('profile')


def is_admin(user):
    return user.groups.filter(name='Admin').exists()



class SignUpView(CreateView):
    form_class = CustomRegistrationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('sign-in')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data.get('password1'))
        user.is_active = False

        if self.request.FILES:
            user.profile_image = self.request.FILES.get('profile_image')

        user.save()
        messages.success(self.request, 'A confirmation mail has been sent. Please check your email.')

        return HttpResponseRedirect(self.get_success_url())  

    def get_success_url(self):
        return self.success_url

    
class CustomLoginView(LoginView):
    form_class = LoginForm

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        return next_url if next_url else super().get_success_url()
    
    
class ChangePassword(PasswordChangeView):
    template_name = 'accounts/password_change.html'
    form_class = CustomPasswordChangeForm


class SignOutView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('sign-in')
    
class ActivateUserView(View):
    def get(self, request, user_id, token):
        try:
            user = CustomUser .objects.get(id=user_id)
            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                return redirect('sign-in')
            else:
                return HttpResponse('Invalid Id or token')

        except CustomUser .DoesNotExist:
            return HttpResponse('User  not found')
        
        
class AdminDashboardView(UserPassesTestMixin, ListView):
    model = CustomUser 
    template_name = 'admin/dashboard.html'
    context_object_name = 'users'
    no_permission = 'no-permission'

    def test_func(self):
        return self.request.user.is_authenticated and is_admin(self.request.user)

    def get_queryset(self):
        users = CustomUser .objects.prefetch_related(
            Prefetch('groups', queryset=Group.objects.all(), to_attr='all_groups')
        ).all()
        
        for user in users:
            if user.all_groups:
                user.group_name = user.all_groups[0].name
            else:
                user.group_name = 'No Group Assigned'
        
        return users
    
class AssignRoleView(UserPassesTestMixin, View):
    no_permission = 'no-permission'

    def test_func(self):
        return self.request.user.is_authenticated and is_admin(self.request.user)

    def get(self, request, user_id):
        user = CustomUser .objects.get(id=user_id)
        form = AssignRoleForm()
        return render(request, 'admin/assign_role.html', {"form": form, "user": user})

    def post(self, request, user_id):
        user = CustomUser .objects.get(id=user_id)
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear() 
            user.groups.add(role)
            messages.success(request, f"User  {user.username} has been assigned to the {role.name} role")
            return redirect('admin_dashboard')

        return render(request, 'admin/assign_role.html', {"form": form, "user": user})

class CreateGroupView(UserPassesTestMixin, CreateView):
    form_class = CreateGroupForm
    template_name = 'admin/create_group.html'
    login_url = 'no-permission'

    def test_func(self):
        return self.request.user.is_authenticated and is_admin(self.request.user)

    def form_valid(self, form):
        group = form.save()
        messages.success(self.request, f"Group {group.name} has been created successfully")
        return redirect('create-group')

    def form_invalid(self, form):
        return self.render_to_response({'form': form})


class GroupListView(UserPassesTestMixin, ListView):
    model = Group
    template_name = 'admin/group_list.html'
    context_object_name = 'groups'

    login_url = 'no-permission'

    def test_func(self):
        return self.request.user.is_authenticated and is_admin(self.request.user)

    def get_queryset(self):
        return Group.objects.prefetch_related('permissions').all()


class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['username'] = user.username
        context['email'] = user.email
        context['name'] = user.get_full_name()
        context['phone_number'] = user.phone_number
        context['profile_image'] = user.profile_image

        context['member_since'] = user.date_joined
        context['last_login'] = user.last_login
        return context


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'registration/reset_password.html'
    success_url = reverse_lazy('sign-in')
    html_email_template_name = 'registration/reset_email.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['protocol'] = 'https' if self.request.is_secure() else 'http'
        context['domain'] = self.request.get_host()
        return context

    def form_valid(self, form):
        messages.success(
            self.request, 'A Reset email sent. Please check your email')
        return super().form_valid(form)


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomPasswordResetConfirmForm
    template_name = 'registration/reset_password.html'
    success_url = reverse_lazy('sign-in')

    def form_valid(self, form):
        messages.success(
            self.request, 'Password reset successfully')
        return super().form_valid(form)
    
class NoPermissionView(View):
    def get(self, request):
        return render(request, "no-permission.html")
    
    
class ShowEventView(View):
    def get(self, request):
        return render(request, "show_event_list.html")
