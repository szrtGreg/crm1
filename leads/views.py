from django.shortcuts import render, redirect, reverse
from django.core.mail import send_mail
from django.http import HttpResponse
from .models import Category, Lead, Agent
from .forms import AssignAgentForm, LeadCategoryUpdateForm, LeadModelForm, CustomUserCreationForm
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
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
     context_object_name = 'leads'

     def get_context_data(self, **kwargs):
        context = super(LeadListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organisor:
            qs = Lead.objects.filter(organisation = user.userprofile, agent__isnull=True)
            context.update({
                'unassigned_leads': qs
            })
        return context


     def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            qs = Lead.objects.filter(organisation = user.userprofile, agent__isnull=False)
        else:
            qs = Lead.objects.filter(agent=user.agent, agent__isnull=False)
        return qs


class LeadDetailView(LoginRequiredMixin, DetailView):
     template_name = 'leads/lead_detail.html'
     context_object_name = 'lead'
     
     def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            qs = Lead.objects.filter(organisation = user.userprofile)
        else:
            qs = Lead.objects.filter(agent=user.agent)
        return qs


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

    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            return Lead.objects.filter(organisation = user.userprofile)

    def get_success_url(self):
        return reverse('lead-list')


class LeadDeleteView(OrganisorAndLoginRequiredMixin, DeleteView):
    template_name = 'leads/lead_delete.html'

    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            return Lead.objects.filter(organisation = user.userprofile)

    def get_success_url(self):
        return reverse('lead-list')



class AssignAgentView(OrganisorAndLoginRequiredMixin, FormView):
    template_name = 'leads/assign_agent.html'
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            'request': self.request
        })
        return kwargs

    def form_valid(self, form):
        agent = form.cleaned_data['agent']
        lead = Lead.objects.get(id=self.kwargs['pk'])
        lead.agent = agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)


    def get_success_url(self):
        return reverse('lead-list')


class CategoryListView(LoginRequiredMixin, ListView):
    template_name = 'leads/category_list.html'
    context_object_name = 'category_list'

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        
        user = self.request.user
        if user.is_organisor:
            qs = Lead.objects.filter(organisation = user.userprofile)
        else:
            qs = Lead.objects.filter(organisation = user.agent.organisation)

        context.update({
            'unassigned_lead_count': qs.filter(category__isnull=True).count()
        })

        return context

    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            qs = Category.objects.filter(organisation = user.userprofile)
        else:
            qs = Category.objects.filter(organisation = user.agent.organisation)
        return qs

    
class CategoryDetailView(LoginRequiredMixin, DetailView):
    template_name = 'leads/category_detail.html'
    context_object_name = 'category'


    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            qs = Category.objects.filter(organisation = user.userprofile)
        else:
            qs = Category.objects.filter(organisation = user.agent.organisation)
        return qs


    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        qs = Lead.objects.filter(category=self.get_object())
        context.update({
            'leads': qs
        })

        return context

    
class LeadCategoryUpdateView(LoginRequiredMixin, UpdateView):
    form_class = LeadCategoryUpdateForm
    template_name = 'leads/lead_category_update.html'

    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            qs = Lead.objects.filter(organisation = user.userprofile)
        else:
            qs = Lead.objects.filter(agent=user.agent)
        return qs

    def get_success_url(self):
        return reverse('lead-detail', kwargs={'pk': self.get_object().id })
