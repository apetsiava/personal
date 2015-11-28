from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView, FormView
from django.core.urlresolvers import reverse_lazy
from .models import *
from .forms import *
from django.core.exceptions import PermissionDenied

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
    paginate_by = 5

class BarDetailView(DetailView):
    model = Bar
    template_name = 'bar/bar_detail.html'

    def get_context_data(self, **kwargs):
       context = super(BarDetailView, self).get_context_data(**kwargs)
       bar = Bar.objects.get(id=self.kwargs['pk'])
       comments = Comment.objects.filter(bar=bar)
       context['comments'] = comments
       return context

class BarUpdateView(UpdateView):
    model = Bar
    template_name = 'bar/bar_form.html'
    fields = ['title', 'description']

    def get_object(self, *args, **kwargs):
        object = super(BarUpdateView, self).get_object(*args, **kwargs)
        if object.user != self.request.user:
            raise PermissionDenied()
        return object

class BarDeleteView(DeleteView):
    model = Bar
    template_name = 'bar/bar_confirm_delete.html'
    success_url = reverse_lazy('bar_list')

    def get_object(self, *args, **kwargs):
        object = super(BarDeleteView, self).get_object(*args, **kwargs)
        if object.user != self.request.user:
            raise PermissionDenied()
        return object

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

class CommentUpdateView(UpdateView):
    model = Comment
    pk_url_kwarg = 'comment_pk'
    template_name = 'comment/comment_form.html'
    fields = ['text']

    def get_success_url(self):
        return self.object.bar.get_absolute_url()

    def get_object(self, *args, **kwargs):
        object = super(CommentUpdateView, self).get_object(*args, **kwargs)
        if object.user != self.request.user:
            raise PermissionDenied()
        return object

class CommentDeleteView(DeleteView):
    model = Comment
    pk_url_kwarg = 'comment_pk'
    template_name = 'comment/comment_confirm_delete.html'

    def get_success_url(self):
        return self.object.bar.get_absolute_url()

    def get_object(self, *args, **kwargs):
        object = super(CommentDeleteView, self).get_object(*args, **kwargs)
        if object.user != self.request.user:
            raise PermissionDenied()
        return object

class VoteFormView(FormView):
    form_class = VoteForm

    def form_valid(self, form):
        user = self.request.user
        bar = Bar.objects.get(pk=form.data["bar"])
        try:
          comment = Comment.objects.get(pk=form.data["comment"])
          prev_votes = Vote.objects.filter(user=user, comment=comment)
          has_voted = (prev_votes.count()>0)
          if not has_voted:
            Vote.objects.create(user=user, comment=comment)
          else:
            prev_votes[0].delete()
          return redirect(reverse('bar', args=[form.data["bar"]]))
        except:
          prev_votes = Vote.objects.filter(user=user, bar=bar)
          has_voted = (prev_votes.count()>0)
        if not has_voted:
            Vote.objects.create(user=user, bar=bar)
        else:
            prev_votes[0].delete()
        return redirect('bar_list')

class UserDetailView(DetailView):
    model = User
    slug_field = 'username'
    template_name = 'user/user_detail.html'
    context_object_name = 'user_in_view'

    def get_context_data(self, **kwargs):
      context = super(UserDetailView, self).get_context_data(**kwargs)
      user_in_view = User.objects.get(username=self.kwargs['slug'])
      bars = Bar.objects.filter(user=user_in_view)
      context['bar'] = bars
      comments = Comment.objects.filter(user=user_in_view)
      context['comments'] = comments
      return context

class UserUpdateView(UpdateView):
    model = User
    slug_field = "username"
    template_name = "user/user_form.html"
    fields = ['email', 'first_name', 'last_name']

    def get_success_url(self):
        return reverse('user_detail', args=[self.request.user.username])

    def get_object(self, *args, **kwargs):
        object = super(UserUpdateView, self).get_object(*args, **kwargs)
        if object != self.request.user:
            raise PermissionDenied()
        return object

class UserDeleteView(DeleteView):
    model = User
    slug_field = "username"
    template_name = 'user/user_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('logout')

    def get_object(self, *args, **kwargs):
        object = super(UserDeleteView, self).get_object(*args, **kwargs)
        if object != self.request.user:
            raise PermissionDenied()
        return object

    def delete(self, request, *args, **kwargs):
        user = super(UserDeleteView, self).get_object(*args)
        user.is_active = False
        user.save()
        return redirect(self.get_success_url())

class SearchBarListView(BarListView):
    def get_queryset(self):
        incoming_query_string = self.request.GET.get('query','')
        return Bar.objects.filter(title__icontains=incoming_query_string)
