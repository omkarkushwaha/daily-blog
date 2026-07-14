from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (ListView,DetailView,CreateView,UpdateView,DeleteView)
from django.contrib.auth.mixins import (LoginRequiredMixin,UserPassesTestMixin)
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import Post, Comment, Category
from .forms import PostForm, CommentForm, RegisterForm

class HomeView(ListView):
    model = Post
    template_name = "blog/home.html"
    context_object_name = "posts"
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get("q")
        queryset = Post.objects.all()

        if query:
            queryset = queryset.filter(title__icontains=query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q")
        return context



def about(request):
    return render(request, "blog/about.html")



class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        context["comments"] = Comment.objects.filter(post=post).order_by("-created_at")
        context["form"] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):

        self.object = self.get_object()

        if not request.user.is_authenticated:
            return redirect("login")
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = self.object
            comment.save()
            messages.success(request,"Comment added successfully.")
        return redirect("post_detail",pk=self.object.pk)

class CreatePostView(LoginRequiredMixin,CreateView):

    model = Post
    form_class = PostForm
    template_name = "blog/create_post.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request,"Blog created successfully.")
        return super().form_valid(form)
    
class UpdatePostView(

    LoginRequiredMixin,

    UserPassesTestMixin,

    UpdateView

):

    model = Post

    form_class = PostForm

    template_name = "blog/update_post.html"

    success_url = reverse_lazy("home")

    def test_func(self):

        post = self.get_object()

        return (

            self.request.user == post.author

            or

            self.request.user.is_superuser

        )

    def form_valid(self, form):

        messages.success(

            self.request,

            "Blog updated successfully."

        )

        return super().form_valid(form)
    
class DeletePostView(

    LoginRequiredMixin,

    UserPassesTestMixin,

    DeleteView

):

    model = Post

    template_name = "blog/delete_post.html"

    success_url = reverse_lazy("home")

    def test_func(self):

        post = self.get_object()

        return (

            self.request.user == post.author

            or

            self.request.user.is_superuser

        )

    def delete(

        self,

        request,

        *args,

        **kwargs

    ):

        messages.success(

            request,

            "Blog deleted successfully."

        )

        return super().delete(

            request,

            *args,

            **kwargs

        )
    
def register(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Account created successfully. Please login."
            )

            return redirect("login")

    else:

        form = RegisterForm()

    return render(
        request,
        "blog/register.html",
        {
            "form": form
        }
    )
    
def user_login(request):

    if request.method == "POST":

        form = AuthenticationForm(
            request,
            data=request.POST
        )

        if form.is_valid():

            user = form.get_user()

            login(request, user)

            messages.success(
                request,
                "Login successful."
            )

            return redirect("home")

    else:

        form = AuthenticationForm()

    return render(
        request,
        "blog/login.html",
        {
            "form": form
        }
    )
    
def user_logout(request):

    logout(request)

    messages.success(
    request,
    "You have been logged out."
    )

    return redirect("home")


@login_required
def profile(request):

    posts = Post.objects.filter(author=request.user)
    context = {"posts": posts,"total_posts": posts.count(),}
    return render(request,"blog/profile.html",context)

def category_posts(request, id):

    category = Category.objects.get(id=id)

    posts = Post.objects.filter(

        category=category

    )

    context = {

        "posts": posts,

        "query": "",

    }

    return render(

        request,

        "blog/home.html",

        context

    )