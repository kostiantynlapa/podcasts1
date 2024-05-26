from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render
from .models import Post
from blog.models import Post, Commentary, User
from django.db.models import Q


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class UserCreateView(generic.CreateView):
    model = User
    form_class = RegisterForm
    template_name = "registration/sign-up.html"
    success_url = reverse_lazy("blog:index")


class PostListView(generic.ListView):
    model = Post
    ordering = ["-created_time"]
    template_name = "blog/index.html"
    paginate_by = 5


class PostDetatilView(generic.DetailView):
    model = Post
    template_name = "blog/post_detail.html"


def podcast_list(request):
    sort_by = request.GET.get('sort_by', 'created_time')
    search_query = request.GET.get('search', '')
    post_list = Post.objects.all()

    if search_query:
        post_list = post_list.filter(Q(title__icontains=search_query) | Q(content__icontains=search_query))

    print(f"Sorting by: {sort_by}, Search query: {search_query}")

    post_list = post_list.order_by(sort_by)

    return render(request, 'index.html', {
        'post_list': post_list,
        'sort_by': sort_by,
        'search_query': search_query,
    })

class CommentaryCreateView(LoginRequiredMixin, generic.CreateView):
    model = Commentary
    template_name = "blog/create-comment.html"
    fields = ("content", )

    def post(self, request, *args, **kwargs):
        user = request.user
        pk = kwargs.get("pk")
        post = get_object_or_404(Post, pk=pk)
        text = request.POST["content"]
        if text:
            Commentary.objects.create(user=user, post=post, content=text)
            return redirect("blog:post-detail", pk=pk)
