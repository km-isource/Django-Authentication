from django.shortcuts import render, redirect
from .forms import RegisterForm, PostForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User, Group
from .models import Post

# Create your views here.
@login_required(login_url='/login')
def home(request):
    posts = Post.objects.all()
    if request.method == "POST":
        post_id = request.POST.get("post-id")
        user_id = request.POST.get("user-id")
        # unban_user_id = request.POST.get("unban-user-id")
        
        if post_id:
            post = Post.objects.filter(id=post_id).first()
            if post and (post.author == request.user or request.user.has_perm("main.delete_post")):
                post.delete()
        elif user_id:
            user = User.objects.filter(id=user_id).first()
            if user and request.user.is_staff:
                for group_name in ['default', 'mod']:
                    try:
                        group = Group.objects.get(name=group_name)
                        group.user_set.remove(user)
                    except Group.DoesNotExist:
                        pass
        
        # elif unban_user_id:
        #     user = User.objects.filter(id=unban_user_id).first()
        #     if user and request.user.is_staff:
        #         try:
        #             group = Group.objects.get(name='default')
        #             group.user_set.add(user)
        #         except Group.DoesNotExist:
        #             pass
        
    return render(request, "main/home.html", {'posts': posts})

@login_required(login_url='/login/')
@permission_required("main.add_post", login_url='/login/', raise_exception=True)
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('/home')
    else:
        form = PostForm()
    return render(request, 'main/create_post.html', {'form': form})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'post_detail.html', {'post': post})

def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect ('/home')
    else:
        form = RegisterForm()
        
    return render(request, 'registration/sign_up.html', {'form': form})

def LogOut(request):
    logout(request)
    return redirect("/login/")



