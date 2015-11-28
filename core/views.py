from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from .models import *

# Create your views here.
class Home(TemplateView):
    template_name = "home.html"

class BarCreateView(CreateView):
    model = Bar
    template_name = "bar/bar_form.html"
    fields = ['title', 'description']
    success_url = reverse_lazy('bar_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(BarCreateView, self).form_valid(form)

class BarListView(ListView):
    model = Bar
    template_name = "bar/bar_list.html"

class BarDetailView(DetailView):
    model = Bar
    template_name = 'bar/bar_detail.html'

class BarUpdateView(UpdateView):
    model = Bar
    template_name = 'bar/bar_form.html'
    fields = ['title', 'description']

class BarDeleteView(DeleteView):
    model = Bar
    template_name = 'bar/bar_confirm_delete.html'
    success_url = reverse_lazy('bar_list')

class CommentCreateView(CreateView):
    model = Comment
    template_name = "comment/comment_form.html"
    fields = ['text']

    def get_success_url(self):
        return self.object.bar.get_absolute_url()

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.bar = Bar.objects.get(id=self.kwargs['pk'])
        return super(CommentCreateView, self).form_valid(form)