from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from PIL import Image
from .models import Repair, Feedback
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
# Create your views here.


class RepairListView(ListView):
    model = Repair
    template_name = 'repairadar_app/home.html'
    context_object_name = 'repairs'
    ordering = ['-dateLogged']
    paginate_by = 2

class RepairDetailView(DetailView):
    model = Repair

class RepairCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = Repair
    fields = ['repairTitle', 'repairDescription', 'repairUrgency', 'repairLocation', 'repairImage']

    def form_valid(self, form):
        title = form.cleaned_data['repairTitle']
        desc = form.cleaned_data['repairDescription']
        urgency = form.cleaned_data['repairUrgency']
        location = form.cleaned_data['repairLocation']

        send_mail(
            subject='Repair Radar - A New Issue Has Been Logged',
            message=f'Issue: {title}\nDescription: {desc}\nUrgency: {urgency}\nLocation: {location} \n Visit http://www.repairradar.co.za/ to view more details',
            from_email='thomasdevilliers@gmail.com',
            recipient_list=['thomasdv69420@gmail.com'],
            #recipient_list=['staff-email@example'],
        )

        send_mail(
            subject='Repair Radar - Your Repair Request Has Been Logged',
            message=f'Issue: {title}\nDescription: {desc}\nUrgency: {urgency}\nLocation: {location} \n Visit http://www.repairradar.co.za/ to view more details',
            from_email='thomasdevilliers@gmail.com',
            recipient_list=[self.request.user.username + '@sun.ac.za'],
            #recipient_list=['staff-email@example'],
        )
        form.instance.suNumber = self.request.user
        return super().form_valid(form)


        
class RepairUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Repair
    fields = ['repairStatus']
    

    def test_func(self):
        repair = self.get_object()
        if self.request.user.username == 'staff' or self.request.user.username == 'tom':
            return True
        return False

class RepairDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Repair
    success_url = '/'

    def test_func(self):
        repair = self.get_object()
        if self.request.user.username == 'staff' or self.request.user.username == 'tom':
            return True
        return False

class UserRepairListView(LoginRequiredMixin, ListView):
    model = Repair
    template_name = 'repairadar_app/user_repairs.html'
    context_object_name = 'repairs'
    ordering = ['-dateLogged']
    paginate_by = 2

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Repair.objects.filter(suNumber=user).order_by('-dateLogged')


class FeedbackListView(ListView):
    model = Feedback
    template_name = 'repairadar_app/feedback.html'
    context_object_name = 'feedbacks'
    paginate_by = 3

class FeedbackDetailView(DetailView):
    model = Feedback

class FeedbackCreateView(LoginRequiredMixin, CreateView):
    model = Feedback
    fields = ['problemDescription', 'resolutionDescription', 'problemLink', 'feedbackTime', 'feedbackCommunication', 'feedbackOverallSatisfaction', 'feedbackAdditional']
    def form_valid(self, form):
        probdesc = form.cleaned_data['problemDescription']
        resdesc = form.cleaned_data['resolutionDescription']
        overall = form.cleaned_data['feedbackOverallSatisfaction']
        addcom = form.cleaned_data['feedbackAdditional']

        send_mail(
            subject='Repair Radar - You Have New Feedback',
            message=f'Problem Description: {probdesc}\nResolution Description: {resdesc}\nOverall Satisfaction: {overall}\nAdditional Comments: {addcom}\nVisit http://www.repairradar.co.za/feedback/ to view more details',
            from_email='thomasdevilliers@gmail.com',
            recipient_list=['thomasdv69420@gmail.com'],
            #recipient_list=['staff-email@example'],
        )

        send_mail(
            subject='Repair Radar - Your Feedback Has Been Recieved',
            message=f'Problem Description: {probdesc}\nResolution Description: {resdesc}\nOverall Satisfaction: {overall}\nAdditional Comments: {addcom}\nVisit http://www.repairradar.co.za/feedback/ to view more details',
            from_email='thomasdevilliers@gmail.com',
            recipient_list=[self.request.user.username + '@sun.ac.za'],
            #recipient_list=['staff-email@example'],
        )
        return super().form_valid(form)

class OrderRepairsByUrgencyView(ListView):
    model = Repair
    template_name = 'repairadar_app/order_repairs_by_status.html'
    context_object_name = 'repairs'
    paginate_by = 2

class UncompleteRepairsView(ListView):
    model = Repair
    template_name = 'repairadar_app/uncomplete_repairs.html'
    context_object_name = 'repairs'
    paginate_by = 2

@login_required
def resolutionChart(request):
    feedbacks = Feedback.objects.all()
    ratings_count_overall = {
        '5 Stars': 0,
        '4 Stars': 0,
        '3 Stars': 0,
        '2 Stars': 0,
        '1 Star': 0
    }

    for feedback in feedbacks:
        ratings_count_overall[feedback.feedbackOverallSatisfaction] += 1
    
    ratings_count_time = {
        'Longer Than Expected': 0,
        'Reasonable Amount Of Time': 0,
        'Promptly Resolved': 0,
    }

    for feedback in feedbacks:
        ratings_count_time[feedback.feedbackTime] += 1

    ratings_count_communication = {
        '5 Stars': 0,
        '4 Stars': 0,
        '3 Stars': 0,
        '2 Stars': 0,
        '1 Star': 0
    }

    for feedback in feedbacks:
        ratings_count_communication[feedback.feedbackCommunication] += 1


    context = {
        'ratings_count_overall': ratings_count_overall,
        'ratings_count_time': ratings_count_time,
        'ratings_count_communication': ratings_count_communication,
    }
    return render(request, 'repairadar_app/resolution_chart.html', context=context)

@login_required
def repairChart(request):
    repairs = Repair.objects.all()
    status_count = {
        'Submitted': 0,
        'Processing': 0,
        'Under Review': 0,
        'Waiting For Parts': 0,
        'Complete': 0,
    }

    for repair in repairs:
        status_count[repair.repairStatus] += 1

    urgency_count = {
        'Low': 0,
        'Medium': 0,
        'High': 0,
    }

    for repair in repairs:
        urgency_count[repair.repairUrgency] += 1

    context = {
        'status_count': status_count,
        'urgency_count': urgency_count
    }
    return render(request, 'repairadar_app/repair_chart.html', context=context)

def faq(request):
    return render(request, 'repairadar_app/faq.html')