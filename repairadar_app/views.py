from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from PIL import Image
from .models import Repair, Feedback
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# Create your views here.


class RepairListView(ListView):
    model = Repair
    template_name = 'repairadar_app/home.html'
    context_object_name = 'repairs'
    ordering = ['-dateLogged']

class RepairDetailView(DetailView):
    model = Repair

class RepairCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = Repair
    fields = ['repairTitle', 'repairDescription','repairUrgency', 'repairLocation', 'repairImage']

    def form_valid(self, form):
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

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Repair.objects.filter(suNumber=user).order_by('-dateLogged')


class FeedbackListView(ListView):
    model = Feedback
    template_name = 'repairadar_app/feedback.html'
    context_object_name = 'feedbacks'

class FeedbackCreateView(LoginRequiredMixin, CreateView):
    model = Feedback
    fields = ['problemDescription', 'resolutionDescription', 'problemLink', 'feedbackTime', 'feedbackCommunication', 'feedbackOverallSatisfaction', 'feedbackAdditional']

class OrderRepairsByUrgencyView(ListView):
    model = Repair
    template_name = 'repairadar_app/order_repairs_by_status.html'
    context_object_name = 'repairs'

def resolution_chart(request):
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

    context = {
        'ratings_count_overall': ratings_count_overall,
        'ratings_count_time': ratings_count_time
    }
    return render(request, 'repairadar_app/resolution_chart.html', context=context)


