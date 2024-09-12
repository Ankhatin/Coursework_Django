from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DetailView, DeleteView
from mailing.models import Blog
from django.urls import reverse_lazy, reverse
from django.shortcuts import render


class BlogListView(ListView):
    model = Blog
    template_name = 'blogs/blog_list.html'


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blogs/blog_detail.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        blog = self.object
        blog.count_review += 1
        blog.save()
        return context_data
