from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm

from blog.models import Blog
from blog.forms import CreateBlogForm


class IndexView(TemplateView):
    template_name = "blog/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['posts'] = Blog.objects.all().order_by('-posted')[:10]
        return context


def create_blog(request):
    if request.method == 'POST':
        form = CreateBlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            if request.user.is_authenticated():
                blog.author = request.user
            blog.save()
            return HttpResponseRedirect('/blog/')
    else:
        form = CreateBlogForm()

    return render(request, 'blog/create_blog.html', {'form': form})


class CreateUser(FormView):
    template_name = 'blog/user_create_form.html'
    form_class = UserCreationForm
    success_url = '/blog/'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = True
        user.save()
        return super(CreateUser, self).form_valid(form)
