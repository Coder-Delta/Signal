from django.shortcuts import render
from .models import post
from .forms import PostForm, SignUpForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate

# Create your views here.

def home(request):
    return render(request, 'home.html')


def post_list(request):
    posts = post.objects.all().order_by('-created_at')
    return render(request, 'post_list.html', {'posts': posts})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'post_form.html', {'form': form})

@login_required
def post_edit(request, pk):
    post_instance = get_object_or_404(post, pk=pk , user=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post_instance)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.save()
            return redirect('post_list')
    else:
        form = PostForm(instance=post_instance)
    return render(request, 'post_form.html', {'form': form})

@login_required
def post_delete(request, pk):
    post_instance = get_object_or_404(post, pk=pk , user=request.user)
    if request.method == 'POST':
        post_instance.delete()
        return redirect('post_list')
    return render(request, 'post_confirm_delete.html', {'post': post_instance})

from django.contrib.auth import login

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])  # ✅ correct method name
            user.save()
            login(request, user)  # ✅ correct function name (no space)
            return redirect('post_list')
    else:
        form = SignUpForm()
    return render(request, 'registration/register.html', {'form': form})


def start(request):
    posts = post.objects.all().order_by('-created_at')[:5]
    return render(request, 'start.html', {'posts': posts})