from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from .models import Lead, Agent
from .forms import LeadModelForm, LeadForm
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView




class LandingPageView(TemplateView):
    template_name = 'landing.html'


class LeadListView(ListView):
     template_name = 'leads/lead_list.html'
     queryset = Lead.objects.all()
     context_object_name = 'leads'


class LeadDetailView(DetailView):
     template_name = 'leads/lead_detail.html'
     queryset = Lead.objects.all()
     context_object_name = 'lead'


class LeadCreateView(CreateView):
    form_class = LeadModelForm
    template_name = 'leads/lead_create.html'

    def get_success_url(self):
        return reverse('lead-list')


class LeadUpdateView(UpdateView):
    form_class = LeadModelForm
    template_name = 'leads/lead_update.html'
    queryset = Lead.objects.all()

    def get_success_url(self):
        return reverse('lead-list')


class LeadDeleteView(DeleteView):
    template_name = 'leads/lead_delete.html'
    queryset = Lead.objects.all()

    def get_success_url(self):
        return reverse('lead-list')
