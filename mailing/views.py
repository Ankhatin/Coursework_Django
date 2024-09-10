import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DetailView, DeleteView
from mailing.forms import NewsletterForm, MessageForm, ClientForm
from mailing.models import Newsletter, Message, Client, Blog
from django.urls import reverse_lazy, reverse

from mailing.services import *


class IndexView(TemplateView):
    template_name = 'mailing/index.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        work_status = ['created', 'launched']
        context_data['count_of_newsletter'] = Newsletter.objects.all().count()
        context_data['count_of_active'] = Newsletter.objects.filter(status__in=work_status).count()
        context_data['count_of_unique_clients'] = len(set(Client.objects.all()))
        blogs = get_cached_blogs()
        random_blogs = random.sample(list(blogs), 3)
        context_data['blogs'] = random_blogs
        return context_data


class ReportView(LoginRequiredMixin, TemplateView):
    template_name = 'mailing/report_mailings.html'
    login_url = '/users/login/'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        user = self.request.user
        newsletters = Newsletter.objects.filter(owner=user)
        queryset = Attempt.objects.filter(newsletter__in=newsletters).order_by('date_attempt')
        if (context_data['view'].request.GET.get("start_date") and
                context_data['view'].request.GET.get("end_date")):
            start_date = datetime.fromisoformat(context_data['view'].request.GET['start_date'])
            end_date = datetime.fromisoformat(context_data['view'].request.GET['end_date'])
            context_data['object_list'] = queryset.filter(date_attempt__gte=start_date).filter(date_attempt__lte=end_date).order_by('date_attempt')
            context_data['start_date'] = start_date
            context_data['end_date'] = end_date
        else:
            context_data['object_list'] = queryset
        return context_data


class NewsletterListView(LoginRequiredMixin, ListView):
    model = Newsletter
    login_url = '/users/login/'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        block = context_data['view'].request.GET.get("block")
        unblock = context_data['view'].request.GET.get("unblock")
        if block:
            pk = context_data['view'].request.GET.get("block")
            newsletter_to_block = Newsletter.objects.get(pk=pk)
            newsletter_to_block.status = 'completed'
            newsletter_to_block.save()
        elif unblock:
            pk = context_data['view'].request.GET.get("unblock")
            newsletter_to_unblock = Newsletter.objects.get(pk=pk)
            newsletter_to_unblock.status = 'launched'
            newsletter_to_unblock.save()
        return context_data


class NewsletterCreateView(LoginRequiredMixin, CreateView):
    model = Newsletter
    form_class = NewsletterForm
    login_url = '/users/login/'
    success_url = reverse_lazy('mailing:newsletter_list')

    def form_valid(self, form):
        user = self.request.user
        mailing = form.save()
        mailing.user = user
        mailing.save()
        if mailing.status != Newsletter.COMPLETED:
            add_job_to_scheduler(mailing)
        return super().form_valid(form)


class NewsletterUpdateView(LoginRequiredMixin, UpdateView):
    model = Newsletter
    form_class = NewsletterForm
    login_url = '/users/login/'
    success_url = reverse_lazy('mailing:newsletter_list')

    def form_valid(self, form):
        mailing = form.save()
        if mailing.status != Newsletter.COMPLETED:
            add_job_to_scheduler(mailing)
        return super().form_valid(form)


class NewsletterDetailView(LoginRequiredMixin, DetailView):
    model = Newsletter

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        clients = self.object.clients.all()
        context_data['clients'] = clients
        return context_data


class NewsletterDeleteView(LoginRequiredMixin, DeleteView):
    model = Newsletter
    login_url = '/users/login/'
    success_url = reverse_lazy('mailing:newsletter_list')


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    login_url = '/users/login/'


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    login_url = '/users/login/'
    success_url = reverse_lazy('mailing:message_list')

    def form_valid(self, form):
        user = self.request.user
        message = form.save()
        message.user = user
        message.save()
        return super().form_valid(form)


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    login_url = '/users/login/'


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    login_url = '/users/login/'
    success_url = reverse_lazy('mailing:message_list')


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    login_url = '/users/login/'
    success_url = reverse_lazy('mailing:message_list')


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    login_url = '/users/login/'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        user = self.request.user
        clients = user.clients.all()
        context_data['object_list'] = clients
        return context_data


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    login_url = '/users/login/'
    success_url = reverse_lazy('mailing:client_list')

    def form_valid(self, form):
        user = self.request.user
        client = form.save()
        client.user = user
        client.save()
        return super().form_valid(form)


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    login_url = '/users/login/'


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    login_url = '/users/login/'
    success_url = reverse_lazy('mailing:client_list')


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    login_url = '/users/login/'
    success_url = reverse_lazy('mailing:client_list')


class BlogDetailView(DetailView):
    model = Blog

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        blog = self.object
        blog.count_review += 1
        blog.save()
        return context_data
