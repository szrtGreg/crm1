from django.shortcuts import render, redirect, reverse
from django.core.mail import send_mail
from django.http import HttpResponse
from .models import Lead, Agent
from .forms import LeadModelForm, CustomUserCreationForm
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from agents.mixins import OrganisorAndLoginRequiredMixin


class SignupView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'

    def get_success_url(self):
        return reverse('login')


class LandingPageView(TemplateView):
    template_name = 'landing.html'


class LeadListView(LoginRequiredMixin, ListView):
     template_name = 'leads/lead_list.html'
     queryset = Lead.objects.all()
     context_object_name = 'leads'


class LeadDetailView(LoginRequiredMixin, DetailView):
     template_name = 'leads/lead_detail.html'
     queryset = Lead.objects.all()
     context_object_name = 'lead'


class LeadCreateView(OrganisorAndLoginRequiredMixin, CreateView):
    form_class = LeadModelForm
    template_name = 'leads/lead_create.html'

    def form_valid(self, form):
        send_mail (
            subject = 'Lead subject',
            message = 'Lead message',
            from_email = 'test@test.com',
            recipient_list = ['test2@test.com']
        )
        return super(LeadCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('lead-list')


class LeadUpdateView(OrganisorAndLoginRequiredMixin, UpdateView):
    form_class = LeadModelForm
    template_name = 'leads/lead_update.html'
    queryset = Lead.objects.all()

    def get_success_url(self):
        return reverse('lead-list')


class LeadDeleteView(OrganisorAndLoginRequiredMixin, DeleteView):
    template_name = 'leads/lead_delete.html'
    queryset = Lead.objects.all()

    def get_success_url(self):
        return reverse('lead-list')
