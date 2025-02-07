from django.shortcuts import render,get_object_or_404, redirect
from events.forms import Add_Event,Create_Participant_Form,Add_Category
from django.db.models import Count,Q
from django.utils.timezone import now
from .models import Add_Event_Model, Create_Participant_Model, Category_Model,RSVP_Model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.contrib import messages
# Create your views here.

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

@login_required
@user_passes_test(is_organizer or is_admin,login_url="sign-in")
def add_event_form(request):
    show_form = Add_Event()
    if request.method == "POST":
        form = Add_Event(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return render(request, "add_event.html", {
                "form": show_form,
                "message": "Event added successfully!"
            })

    return render(request, "add_event.html", {"form": show_form})

@login_required
@user_passes_test(is_organizer or is_admin,login_url="sign-in")
def  create_participant_view(request):
     form_view =  Create_Participant_Form()
     
     if request.method == "POST":
        form = Create_Participant_Form(request.POST)
        if form.is_valid() :
           form.save()

        context = {
            'form':form_view ,
            'message':'Participant added successfully !!',
        }
        return render(request, 'create_participant.html', context)

     return render(request, 'create_participant.html', {'form':form_view})
 
@login_required
@user_passes_test(is_organizer or is_admin,login_url="sign-in")
def create_category(request):
     form_view =  Add_Category()
     
     if request.method == "POST":
        form = Add_Category(request.POST)
        if form.is_valid() :
           form.save()

        context = {
            'form':form_view ,
            'message':'Category added successfully !!'
        }
        return render(request, 'create_category.html', context)

     return render(request, 'create_category.html', {'form':form_view})
 
# filter events data 
def optimized_event_list(request):
    # Fetch events with their categories and participants
    events = Add_Event_Model.objects.select_related('category').prefetch_related('events')

    # Apply filtering based on category and date range
    category = request.GET.get('category')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if category:
        events = events.filter(category__name=category)  
    if start_date and end_date:
        events = events.filter(date__range=[start_date, end_date]) 

    # Aggregate query to count the total number of participants across all events
    total_participants = events.annotate(participant_count=Count('events')).aggregate(
        total=Count('events')
    )['total']
    
    categories = Category_Model.objects.all()
    
    query = request.GET.get('search', '')  
    search_events = Add_Event_Model.objects.all()

    if query:
        search_events = search_events.filter(Q(name__icontains=query) | Q(location__icontains=query))


    return render(request, 'home.html', {
        'events': events,
        'search_events':search_events,
        'total_participants': total_participants if total_participants else 0,
        'categories':categories,
    })

@login_required
# @user_passes_test(is_organizer or is_admin or is_participant,login_url="sign-in")
def organizer_dashboard(request):
    total_participants = Create_Participant_Model.objects.count()
    total_events = Add_Event_Model.objects.count()
    upcoming_events = Add_Event_Model.objects.filter(date__gte=now().date()).count()
    past_events = Add_Event_Model.objects.filter(date__lt=now().date()).count()
    todays_events = Add_Event_Model.objects.filter(date=now().date())

    return render(request, 'dashboard.html', {
        'total_participants': total_participants,
        'total_events': total_events,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'todays_events': todays_events,
    })



# -------------------- EVENT VIEWS -------------------- #
@login_required
@user_passes_test(is_organizer or is_admin,login_url="sign-in")
def event_list(request):
    events = Add_Event_Model.objects.select_related('category').all()
    return render(request, 'event_list.html', {'events': events})

@login_required
@user_passes_test(is_organizer or is_admin,login_url="sign-in")
def event_create(request):
    if request.method == "POST":
        form = Add_Event(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = Add_Event()
    return render(request, 'event_form.html', {'form': form})

@login_required
@user_passes_test(is_organizer or is_admin,login_url="sign-in")
def event_update(request, pk):
    event = get_object_or_404(Add_Event_Model, pk=pk)
    if request.method == "POST":
        form = Add_Event(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = Add_Event(instance=event)
    return render(request, 'update_event.html', {'form': form})

@login_required
@user_passes_test(is_organizer or is_admin,login_url="sign-in")
def event_delete(request, pk):
    event = get_object_or_404(Add_Event_Model, pk=pk)
    if request.method == "POST":
        event.delete()
        return redirect('event_list')
    return render(request, 'event_confirm_delete.html', {'event': event})


# -------------------- PARTICIPANT VIEWS -------------------- #
@login_required
@user_passes_test(is_organizer or is_admin,login_url="sign-in")
def participant_list(request):
    participants = Create_Participant_Model.objects.prefetch_related('event_assign').all()
    return render(request, 'participant_list.html', {'participants': participants})

@login_required
@user_passes_test(is_organizer or is_admin,login_url="sign-in")
def participant_create(request):
    if request.method == "POST":
        form = Create_Participant_Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('participant_list')
    else:
        form = Create_Participant_Form()
    return render(request, 'create_participant.html', {'form': form})

@login_required
@user_passes_test(is_organizer or is_admin,login_url="sign-in")
def participant_update(request, pk):
    participant = get_object_or_404(Create_Participant_Model, pk=pk)
    if request.method == "POST":
        form = Create_Participant_Form(request.POST, instance=participant)
        if form.is_valid():
            form.save()
            return redirect('participant_list')
    else:
        form = Create_Participant_Form(instance=participant)
    return render(request, 'update_participant.html', {'form': form})

@login_required
@user_passes_test(is_organizer or is_admin,login_url="sign-in")
def participant_delete(request, pk):
    participant = get_object_or_404(Create_Participant_Model, pk=pk)
    if request.method == "POST":
        participant.delete()
        return redirect('participant_list')
    return render(request, 'participant_confirm_delete.html', {'participant': participant})


# -------------------- CATEGORY VIEWS -------------------- #
@login_required
@user_passes_test(is_organizer or is_admin,login_url="sign-in")
def category_list(request):
    categories = Category_Model.objects.all()
    return render(request, 'category_list.html', {'categories': categories})

@login_required
@user_passes_test(is_organizer or is_admin,login_url="sign-in")
def category_create(request):
    if request.method == "POST":
        form = Add_Category(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = Add_Category()
    return render(request, 'create_category.html', {'form': form})

@login_required
@user_passes_test(is_organizer or is_admin,login_url="sign-in")
def category_update(request, pk):
    category = get_object_or_404(Category_Model, pk=pk)
    if request.method == "POST":
        form = Add_Category(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = Add_Category(instance=category)
    return render(request, 'update_category.html', {'form': form})

@login_required
@user_passes_test(is_organizer or is_admin,login_url="sign-in")
def category_delete(request, pk):
    category = get_object_or_404(Category_Model, pk=pk)
    if request.method == "POST":
        category.delete()
        return redirect('category_list')
    return render(request, 'category_confirm_delete.html', {'category': category})

@login_required
def rsvp_event(request, event_id):
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


def my_rsvps(request):
    events = Add_Event_Model.objects.filter(rsvp_model__user=request.user)  
    return render(request, 'event_dashboard.html', {'events': events})


def event_detail(request, event_id):
    event = get_object_or_404(Add_Event_Model, id=event_id)
    return render(request, 'event_detail.html', {'event': event})

