from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from django.db.models import Count,Q
from .models import Event,Category
from .forms import EventForm,CategoryForm,AssignRoleForm,CreateGroupForm
from django.utils.timezone import now
from datetime import date
from django.contrib.auth.models import User,Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import logout
from django.views import View
from django.contrib.auth.mixins import PermissionRequiredMixin,LoginRequiredMixin
from django.views.generic import ListView,DeleteView,TemplateView
from django.urls import reverse_lazy
# Create your views here.

from django.contrib.auth import get_user_model
User = get_user_model()

def is_admin(user):
    return user.is_superuser or user.groups.filter(name='Admin').exists()



def is_organizer(user):
    return user.groups.filter(name='Organizer').exists()


# @user_passes_test(is_admin, login_url='no-permission')
# def home(request):
#     all_category = Category.objects.annotate(
#         total_event=Count('reverse_category', distinct=True),
#         total_participant=Count('reverse_category__participant', distinct=True) 
#     )

#     return render(request,'home.html',{'all_category':all_category})

class HomeView(LoginRequiredMixin,PermissionRequiredMixin,TemplateView):
    template_name='home.html'
    permission_required = 'auth.view_group'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["all_category"] = Category.objects.annotate(
        total_event=Count('reverse_category', distinct=True),
        total_participant=Count('reverse_category__participant', distinct=True) 
        )
        return context
    
    



@user_passes_test(is_organizer, login_url='no-permission')
def create_event(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_event')
    else:
        form = EventForm()
    return render(request, 'all.html', {'form': form})

@user_passes_test(is_organizer, login_url='no-permission')
def create_category(request):
    if request.method =="POST":
        form=CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_category')
    else:
            form=CategoryForm()
    return render(request,'all.html',{'form':form})
            

@login_required
def all_events(request):
    query = request.GET.get('q')
    filter_option = request.GET.get('filter')

    all_event = Event.objects.all()

   
    if query:
        all_event = all_event.filter(
            Q(name__icontains=query) |
            Q(location__icontains=query) |
            Q(category__name__icontains=query)
        )


    if filter_option == 'today':
        all_event = all_event.filter(start_date=date.today())
    elif filter_option == 'past':
        all_event = all_event.filter(start_date__lt=date.today())
    elif filter_option == 'future':
        all_event = all_event.filter(start_date__gt=date.today())

    return render(request, 'organizer.html', {'all_event': all_event})

@user_passes_test(is_organizer, login_url='no-permission')
def edit_event(request, id):
    event = get_object_or_404(Event, id=id)

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('all_events') 
    else:
        form = EventForm(instance=event)

    return render(request, 'all.html', {'form': form})


# @user_passes_test(is_organizer, login_url='no-permission')
# def delete_event(request, id):
#     event = Event.objects.get(id=id)
#     event.delete()
#     return redirect('all_events')

class DeleteEvent(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    model=Event
    permission_required = 'work.delete_event'
    login_url='no-permission'
    success_url=reverse_lazy('all_events')




@user_passes_test(is_admin, login_url='no-permission')
def see_and_change_roles(request):
    all_user = User.objects.all()
    all_groups = Group.objects.all()

    if request.method == "POST":
        user_id = request.POST.get("user_id")
        new_group_id = request.POST.get("group_id")

        user = User.objects.get(id=user_id)
        new_group = Group.objects.get(id=new_group_id)

        user.groups.clear()
        user.groups.add(new_group)
        messages.success(request, f"{user.username} is now assigned to {new_group.name} role.")
        return redirect('see-and-change-roles')

    for user in all_user:
        groups = [g.name for g in user.groups.all()]
        # if user.is_superuser:
        #     groups.append("Admin")
        user.group_names = ", ".join(groups) or "No Group"

    return render(request, 'admin.html', {'all_user': all_user, 'all_groups': all_groups})

# def group_related_work(request):
#     all_group=Group.objects.all()
#     return render(request,'group.html',{'all_group':all_group})

# @user_passes_test(is_admin, login_url='no-permission')
# def show_group(request):
#     all_group=Group.objects.all()
#     return render(request,'group.html',{'all_group':all_group})

class ShowGroup(LoginRequiredMixin,PermissionRequiredMixin,ListView,View):
    model=Group
    template_name = 'group.html'
    context_object_name = 'all_group'
    login_url = 'no-permission'
    
    permission_required = 'auth.view_group'








@user_passes_test(is_admin, login_url='no-permission')
def create_group(request):
    if request.method == "POST":
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            permissions = form.cleaned_data['permissions']
           
            group, created = Group.objects.get_or_create(name=name)
            
        
            group.permissions.set(permissions)
            
            messages.success(request, f"Group '{name}' created successfully!")
            return redirect('create_group')
    else:
        form = CreateGroupForm()
    
    return render(request, 'create_group.html', {'form': form})

@user_passes_test(is_admin, login_url='no-permission')
def update_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    
    if request.method == "POST":
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group.name = form.cleaned_data['name']
            permissions = form.cleaned_data['permissions']
            group.permissions.set(permissions)
            group.save()
            
            messages.success(request, f"Group '{group.name}' updated successfully!")
            return redirect('group_related_work')
    else:
        form = CreateGroupForm(initial={
            'name': group.name,
            'permissions': group.permissions.all()
        })
    
    return render(request, 'update_group.html', {'form': form, 'group': group})


@user_passes_test(is_admin, login_url='no-permission')
def delete_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    
    if request.method == "POST":
        group.delete()
        messages.success(request, f"Group '{group.name}' deleted successfully!")
        return redirect('group_related_work')
    
    return render(request, 'delete_group.html', {'group': group})

@login_required
def rsvp_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.user in event.rsvps.all():
        messages.warning(request, "You have already booked this event!")
    else:
        event.rsvps.add(request.user)
        messages.success(request, "You have successfully booked this event!")

      
        subject = f"RSVP Confirmation for {event.name}"
        message = f"Hi {request.user.username},\n\nYou have successfully booked the event '{event.name}' happening on {event.start_date} at {event.location}.\n\nThank you!"
        recipient_list = [request.user.email]

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER, 
            recipient_list,
            fail_silently=False,
        )

    return redirect('dashboard')

# @login_required
# def dashboard(request):
#     events = Event.objects.all()
    
   
#     is_organizer = request.user.groups.filter(name='Organizer').exists()
#     is_admin = request.user.is_superuser
    
  
#     booked_event_ids = request.user.rsvp_events.values_list('id', flat=True)
    
#     return render(request, 'dashboard.html', {
#         'events': events,
#         'is_organizer': is_organizer,
#         'is_admin': is_admin,
#         'booked_event_ids': booked_event_ids
#     })


class DashboardView(LoginRequiredMixin, ListView):
    model=Event
    template_name = 'dashboard.html'
    context_object_name = 'events'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_organizer"] = self.request.user.groups.filter(name='Organizer').exists()
        context['is_admin'] = self.request.user.is_superuser
        context['booked_event_ids'] = self.request.user.rsvp_events.values_list('id', flat=True)
        return context
    



# @user_passes_test(is_admin, login_url='no-permission')
# def delete_participant(request, user_id):
#     participant = get_object_or_404(User, id=user_id)

#     if request.method == 'POST':
#         participant.delete()
#         messages.success(request, f'Participant "{participant.username}" has been deleted.')
#         return redirect('see-and-change-roles')

#     return render(request, 'delete_participant.html', {'participant': participant})

class DeleteParticipent(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    model=User
    permission_required = 'auth.delete_task'
    template_name='delete_participant.html'
    success_url = reverse_lazy('see-and-change-roles')


@login_required
def sign_out(request):
    logout(request)
    return redirect('sign-in')


