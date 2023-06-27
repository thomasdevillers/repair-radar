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

class FeedbackListView(ListView):
    model = Feedback
    template_name = 'repairadar_app/feedback.html'
    context_object_name = 'feedbacks'

class FeedbackCreateView(LoginRequiredMixin, CreateView):
    model = Feedback
    fields = ['problemDescription', 'resolutionDescription', 'problemLink', 'feedbackTime', 'feedbackCommunication', 'feedbackOverallSatisfaction', 'feedbackAdditional']


