from django.shortcuts import render, redirect, reverse
from django.core.mail import send_mail
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
