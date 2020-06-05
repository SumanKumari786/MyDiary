from django.contrib import messages, auth
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from Diary.forms import ProfileUpdate, UserUpdate, CommentForm
from Diary.models import Post, PostComment, Like


def fun(request):
    return render(request, "Diary/index.html")


def about(request):
    return render(request, "Diary/about.html")

def contact(request):
    return render(request, "Diary/contact.html")


def logout(request):
    auth.logout(request)
    return redirect('/')


def register(request):
    if request.method == 'POST':
        fn = request.POST['fname']
        ln = request.POST['lname']
        un = request.POST['usname']
        pass1 = request.POST['password1']
        pass2 = request.POST['password2']
        em = request.POST['email']

        if pass1 == pass2:

            if User.objects.filter(username=un).exists():
                messages.info(request, 'Username already Taken')
                return redirect('/register')
            elif User.objects.filter(email=em).exists():
                messages.info(request, 'Email already Taken')
                return redirect('/register')
            else:
                user = User.objects.create_user(first_name=fn, last_name=ln, username=un, password=pass1, email=em, )
                user.save()
                messages.info(request, 'You are register succesfully please LOGIN')
                return redirect('/login')
        else:
            messages.info(request, 'Password does not match')

        return redirect('/register')

    else:
        return render(request, "Diary/Register.html")


def login(request):
    if request.method == 'POST':
        n = request.POST['name']
        pass1 = request.POST['pass']

        user = auth.authenticate(username=n, password=pass1)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'invalid credentials')
            return redirect('/register')
    else:
        return render(request, "Diary/login.html")


@login_required(login_url='/login/')
def view_profile(request):
    return render(request, "Diary/View_Profile.html")


@login_required(login_url='/login/')
def update_profile(request):
    if request.method == 'POST':

       u_form = UserUpdate(request.POST, instance=request.user)
       p_form = ProfileUpdate(request.POST, request.FILES, instance=request.user.myprofile)

       if u_form.is_valid() and p_form.is_valid():
          u_form.save()
          p_form.save()
          messages.success(request, 'Your Profile is updated Successfully')
          return redirect('/view_profile')
       else:
           messages.error(request, 'Something wrong:')
    else:
       u_form = UserUpdate(instance=request.user)
       p_form = ProfileUpdate(instance=request.user.myprofile)
    context = {
       'u_form': u_form,
       'p_form': p_form
    }
    return render(request, "Diary/Update_Profile.html", context)


@login_required(login_url='/login/')
def changePass(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            v = form.save()
            update_session_auth_hash(request, v)
            messages.success(request, 'Your password change successfully')
    else:
        form = PasswordChangeForm(request.user)
    params = {
        'form': form,
    }
    return render(request, "Diary/changePass.html", params)


class PostListView(ListView):
    model = Post
    template_name = 'Diary/view.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 3


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = Post
    fields = ['title', 'status', 'slug', 'content']

    def form_valid(self, form):
        form.instance.name = self.request.user
        return super().form_valid(form)


class PostUpdateView(UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'status', 'slug', 'content']

    def form_valid(self, form):
        form.instance.name = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.name:
            return True
        return False


class PostDeleteView(UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/view_status'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.name:
            return True
        return False


@login_required(login_url='/login/')
def view_status(request):
    posts = Post.objects.filter(name=request.user)
    paginator = Paginator(posts, 1)
    page = request.GET.get('page')  # page variable is used to get page number that we passing in view
    # ?page=2
    posts = paginator.get_page(page)  # to access the items in page use get_page method
    params = {'posts': posts}
    return render(request, "Diary/myposts.html", params)


@login_required(login_url='/login/')
def private(request):
    posts = Post.objects.filter(name=request.user)
    paginator = Paginator(posts, 1)
    page = request.GET.get('page')  # page variable is used to get page number that we passing in view
    # ?page=2
    posts = paginator.get_page(page)  # to access the items in page use get_page method
    params = {'posts': posts}
    return render(request, "Diary/private.html", params)


def continuepost(request, slug):
    post = Post.objects.filter(slug=slug).first()
    comments = PostComment.objects.filter(post=post, reply=None)

    if request.method == 'POST':
        commentform = CommentForm(request.POST or None)
        if commentform.is_valid():
            comment = request.POST.get('comment')
            reply_id = request.POST.get('comment_sno')
            comment_qs = None
            if reply_id:
                comment_qs = PostComment.objects.get(sno=reply_id)
            postcomment = PostComment.objects.create(post=post, user=request.user, comment=comment, reply=comment_qs)
            postcomment.save()
    else:
        commentform = CommentForm()

    context = {'post': post, 'comments': comments, 'commentform': commentform}
    return render(request, "Diary/continue.html", context)


def like_post(request):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)
        post = get_object_or_404(Post, id=post_id)
        if user in post_obj.liked.all():
            post_obj.liked.remove(user)
            messages.warning(request, 'You Unlike The Post')
        else:
            post_obj.liked.add(user)
            messages.success(request, 'You Like The Post')
        like, created = Like.objects.get_or_create(user=user, post=post)

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'

        like.save()
    #return redirect('Diary:like_post')
    #return redirect("/")
    return render(request, "Diary/like.html")
