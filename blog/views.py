from django.shortcuts import render,reverse,get_object_or_404,redirect
from django.views.generic import (TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView,FormView)
from .models import Post,Comment
from .forms import PostForm,CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.views.generic.edit import FormMixin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
# Create your views here.

class Home(TemplateView):
    template_name = 'blog/base.html'

class PostListView(ListView):
    model = Post
     
    def get_queryset(self):
        return Post.objects.filter(date_posted__lte = timezone.now()).order_by('-date_posted')

class PostDetailView(FormMixin, DetailView):
    template_name = 'blog/post_detail.html'
    model = Post

    form_class = CommentForm

    def get_success_url(self):
        return reverse('blog:postdetail', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['form'] = CommentForm(initial={'post': self.object})
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super(PostDetailView, self).form_valid(form)


class MyFormView(FormView):
    form_class = CommentForm
    success_url = 'blog:postdetail'
    
    
class PostCreateView(LoginRequiredMixin,CreateView):
    redirect_field_name = 'blog:postlist'

    form_class = PostForm
    model = Post

class PostUpdateView(LoginRequiredMixin,UpdateView):
    redirect_field_name = 'blog:postlist'

    form_class = PostForm
    model = Post

class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    success_url = '/blog/post_list'

class Drafts(LoginRequiredMixin,ListView):
    model = Post
    
    def get_queryset(self):
        return Post.objects.filter(date_posted__isnull=True).order_by('date_created')

class SignUpView(CreateView):
    success_url = reverse_lazy('login')
    form_class = UserCreationForm
    template_name = 'blog/signup.html'

@login_required 
def publish(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.published()
    post.save()
    return redirect("blog:postlist")
    
# @login_required    
# def add_comment_to_post(request,pk):
#     post = get_object_or_404(Post,pk=pk)
#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.post = post
#             comment.save()
#             return redirect('blog:postdetail',pk=pk)
#         else:
#             form = CommentForm()
#     return redirect('blog:postdetail', pk=post.id)

@login_required
def comment_approve(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    comment.approved_comment = True
    comment.save()
    return redirect('blog:postdetail',pk=comment.post.pk)

@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    post = comment.post.pk
    comment.delete()
    return redirect('blog:postdetail',pk=post)


