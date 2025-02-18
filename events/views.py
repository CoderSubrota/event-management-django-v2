from django.shortcuts import render,get_object_or_404, redirect
from events.forms import Add_Event,Create_Participant_Form,Add_Category
from django.db.models import Count,Q
from django.utils.timezone import now
from .models import Add_Event_Model, Create_Participant_Model, Category_Model,RSVP_Model
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import FormView,UpdateView,DeleteView,CreateView
from django.urls import reverse_lazy
from django.views.generic import ListView,TemplateView,DetailView,View

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

class AddEventView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    template_name = "add_event.html"
    form_class = Add_Event
    success_url = reverse_lazy('add_event')

    def test_func(self):
        return is_organizer or is_admin

    def form_valid(self, form):
        form.save()
        return self.render_to_response(self.get_context_data(form=form, message="Event added successfully!"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context
    
class CreateParticipantView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    template_name = 'create_participant.html'
    form_class = Create_Participant_Form
    success_url = reverse_lazy('create_participant')  # Adjust the URL name as needed

    def test_func(self):
        return is_organizer or is_admin

    def form_valid(self, form):
        form.save()
        return self.render_to_response(self.get_context_data(form=form, message='Participant added successfully!'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context
    
class CreateCategoryView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    template_name = 'create_category.html'
    form_class = Add_Category
    success_url = reverse_lazy('create_category')  # Adjust the URL name as needed

    def test_func(self):
        return is_organizer or is_admin

    def form_valid(self, form):
        form.save()
        return self.render_to_response(self.get_context_data(form=form, message='Category added successfully!'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context
    
class OptimizedEventListView(ListView):
    model = Add_Event_Model
    template_name = 'home.html'
    context_object_name = 'events'

    def get_queryset(self):
        events = Add_Event_Model.objects.select_related('category').prefetch_related('events')
        category = self.request.GET.get('category')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        if category:
            events = events.filter(category__name=category)
        if start_date and end_date:
            events = events.filter(date__range=[start_date, end_date])

        total_participants = events.annotate(participant_count=Count('events')).aggregate(
            total=Count('events')
        )['total']

        self.total_participants = total_participants if total_participants else 0

        return events

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_participants'] = self.total_participants
        context['categories'] = Category_Model.objects.all()

        # Handle search functionality
        query = self.request.GET.get('search', '')
        if query:
            context['search_events'] = Add_Event_Model.objects.filter(
                Q(name__icontains=query) | Q(location__icontains=query)
            )
        else:
            context['search_events'] = Add_Event_Model.objects.none() 

        return context
    

class OrganizerDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Calculate dashboard statistics
        context['total_participants'] = Create_Participant_Model.objects.count()
        context['total_events'] = Add_Event_Model.objects.count()
        context['upcoming_events'] = Add_Event_Model.objects.filter(date__gte=now().date()).count()
        context['past_events'] = Add_Event_Model.objects.filter(date__lt=now().date()).count()
        context['todays_events'] = Add_Event_Model.objects.filter(date=now().date())

        return context


# -------------------- EVENT VIEWS -------------------- #
class EventListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Add_Event_Model
    template_name = 'event_list.html'
    context_object_name = 'events'

    def test_func(self):
        return is_organizer or is_admin

    def get_queryset(self):
        return Add_Event_Model.objects.select_related('category').all()

    
class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Add_Event_Model
    form_class = Add_Event  
    template_name = 'update_event.html'
    success_url = reverse_lazy('event_list')  

    def test_func(self):
        return is_organizer or is_admin

    def get_object(self, queryset=None):
        return get_object_or_404(Add_Event_Model, pk=self.kwargs['pk'])
    
class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Add_Event_Model
    template_name = 'event_confirm_delete.html'
    success_url = reverse_lazy('event_list') 

    def test_func(self):
        return is_organizer or is_admin

    def get_object(self, queryset=None):
        return get_object_or_404(Add_Event_Model, pk=self.kwargs['pk'])

# -------------------- PARTICIPANT VIEWS -------------------- #
class ParticipantListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Create_Participant_Model
    template_name = 'participant_list.html'
    context_object_name = 'participants'  

    def test_func(self):
        return is_organizer or is_admin

    def get_queryset(self):
        return Create_Participant_Model.objects.prefetch_related('event_assign').all()


class ParticipantCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Create_Participant_Model
    form_class = Create_Participant_Form  
    template_name = 'create_participant.html'
    success_url = reverse_lazy('participant_list') 

    def test_func(self):
        return is_organizer or is_admin

    def form_valid(self, form):
        return super().form_valid(form)
    
class ParticipantUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Create_Participant_Model
    form_class = Create_Participant_Form
    template_name = 'update_participant.html'
    success_url = reverse_lazy('participant_list') 

    def test_func(self):
        return is_organizer or is_admin

    def get_object(self, queryset=None):
        return get_object_or_404(Create_Participant_Model, pk=self.kwargs['pk'])

class ParticipantDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Create_Participant_Model
    template_name = 'participant_confirm_delete.html'
    success_url = reverse_lazy('participant_list') 

    def test_func(self):
        return is_organizer or is_admin

    def get_object(self, queryset=None):
        return get_object_or_404(Create_Participant_Model, pk=self.kwargs['pk'])

# -------------------- CATEGORY VIEWS -------------------- #
class CategoryListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Category_Model
    template_name = 'category_list.html'
    context_object_name = 'categories'

    def test_func(self):
        return is_organizer or is_admin

    def get_queryset(self):
        return Category_Model.objects.all()
    
class CategoryCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Category_Model
    form_class = Add_Category  
    template_name = 'create_category.html'
    success_url = reverse_lazy('category_list')  

    def test_func(self):
        return is_organizer or is_admin

    def form_valid(self, form):
        return super().form_valid(form)
    
class CategoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Category_Model
    form_class = Add_Category  
    template_name = 'update_category.html'
    success_url = reverse_lazy('category_list')

    def test_func(self):
        return is_organizer or is_admin

    def get_object(self, queryset=None):
        return get_object_or_404(Category_Model, pk=self.kwargs['pk'])
    
class CategoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Category_Model
    template_name = 'category_confirm_delete.html'
    success_url = reverse_lazy('category_list') 

    def test_func(self):
        return is_organizer or is_admin

    def get_object(self, queryset=None):
        return get_object_or_404(Category_Model, pk=self.kwargs['pk'])
    
class RSVPEventView(LoginRequiredMixin, View):
    def post(self, request, event_id):
        event = get_object_or_404(Add_Event_Model, id=event_id)
        
        if RSVP_Model.objects.filter(user=request.user, event=event).exists():
            messages.error(request, "You have already RSVP'd for this event.")
            return redirect('event_rsvps_dashboard')
        
        RSVP_Model.objects.create(user=request.user, event=event)
        
        send_mail(
            "Event RSVP Confirmation",
            f"You have successfully RSVP'd for {event.name}.",
            "itsectorcommunication@gmail.com",
            [request.user.email],
            fail_silently=True,
        )

        messages.success(request, "RSVP confirmed. A confirmation email has been sent.")
        return redirect('event_rsvps_dashboard')
    

class RSVPsView(LoginRequiredMixin, ListView):
    model = Add_Event_Model
    template_name = 'event_dashboard.html'  
    context_object_name = 'events' 

    def get_queryset(self):
        return Add_Event_Model.objects.filter(rsvp_model__user=self.request.user)

class EventDetailView(DetailView):
    model = Add_Event_Model
    template_name = 'event_detail.html'
    context_object_name = 'event'  

    def get_object(self, queryset=None):
        return get_object_or_404(Add_Event_Model, id=self.kwargs['event_id'])
