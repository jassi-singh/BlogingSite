from django.shortcuts import render,reverse,get_object_or_404,redirect
from django.views.generic import (TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView,FormView)
from .models import Post,Comment,Mygroup
from .forms import PostForm,CommentForm,MygroupForm
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
    
    
class PostCreateView(LoginRequiredMixin,CreateView):
    redirect_field_name = 'blog:postlist'

    form_class = PostForm
    model = Post

    def get_form_kwargs(self):
        kwargs = super(PostCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_initial(self):
        author = self.request.user   
        return {
            'author' : author
        }
    

class PostUpdateView(LoginRequiredMixin,UpdateView):
    redirect_field_name = 'blog:postlist'

    form_class = PostForm
    model = Post

    def get_form_kwargs(self):
        kwargs = super(PostUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    success_url = '/blog/post_list'

class Drafts(LoginRequiredMixin,ListView):
    model = Post
    
    def get_queryset(self):
        return Post.objects.filter(date_posted__isnull=True).filter(author__exact=self.request.user).order_by('-date_created')

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

class MygroupListView(ListView,FormMixin):
    model = Mygroup
    form_class = MygroupForm


    def get_success_url(self):
        return reverse('blog:mygrouplist')

    def get_context_data(self, **kwargs):
        context = super(MygroupListView, self).get_context_data(**kwargs)
        context['form'] = MygroupForm(initial={'admin' : self.request.user.id})
        return context

    def post(self, request, *args, **kwargs):
        form=self.get_form()
        form.save(commit=True)
        group = Mygroup.objects.all().last()
        group.member.add(request.user.id)
        group.save()
        return self.get(request, *args, **kwargs)

@login_required
def join_group(request,pk):
    group = get_object_or_404(Mygroup,pk=pk)
    group.member.add(request.user.id)
    group.save()
    return redirect('blog:mygrouplist')

@login_required
def leave_group(request,pk):
    group = get_object_or_404(Mygroup,pk=pk)
    group.member.remove(request.user.id)
    group.save()
    return redirect('blog:mygrouplist')

class MygroupDetailView(DetailView):
    model = Mygroup
    template_name = 'blog/mygroup.html'

    def get_context_data(self, **kwargs):
        context = super(MygroupDetailView,self).get_context_data(**kwargs)
        context["posts"] =  Post.objects.filter(group=self.kwargs['pk']).filter(date_posted__lte = timezone.now()).order_by('-date_posted')
        return context

@login_required
def delete_member(request,pk,sk):
    group = get_object_or_404(Mygroup,pk=pk)
    group.member.remove(sk)
    group.save()
    return redirect('blog:group', pk=pk)

@login_required
def delete_group(request,pk):
    Mygroup.objects.filter(id=pk).delete()
    return redirect('blog:mygrouplist')



