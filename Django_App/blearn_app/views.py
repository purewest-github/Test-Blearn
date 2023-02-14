from typing import List
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from blearn_app.models import Content
from .forms import ContentForm
# Create your views here.

def signupfunc(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.create_user(username,'',password)
            return redirect('login')
        except IntegrityError:
            return render(request,'signup.html', {'error':'このユーザーはすでに登録されています'})
    # return redirect('login')
    return render(request, 'signup.html')

def loginfunc(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('list')
        else:
            # return render(request,'signup.html', {})
            return  redirect('signup')
    return render(request,'login.html', {})

# def listfunc(request):
#     object_list = BoardModel.objects.all()
#     return render(request, 'list.html',{'object_list':object_list})
#     # object = get_object_or_404(User, pk=pk)
#     # return render(request, 'list.html', {'object':object})

def logoutfunc(request):
    logout(request)
    return redirect('login')

# def detailfunc(request,pk):
#     object = get_object_or_404(BoardModel, pk=pk)
#     return render(request, 'detail.html', {'object':object})


class ContentCreate(CreateView):
    template_name = 'create.html'
    form_class = ContentForm
    success_url = reverse_lazy('list')

    # 投稿者ユーザーとリクエストユーザーを紐付ける
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ContentList(LoginRequiredMixin, ListView):
    template_name = 'list.html'
    model = Content

    def get_queryset(self):
        return Content.objects.filter(user=self.request.user)

class ContentDetail(DetailView):
    template_name = 'detail.html'
    model = Content

class ContentUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'update.html'
    # fieldに入っているデータをModelから持ってくるのに必要
    model = Content
    form_class = ContentForm

    def get_success_url(self, **kwargs):
        '''編集完了後の遷移先'''
        pk = self.kwargs["pk"]
        return reverse_lazy('detail', kwargs={"pk":pk})

    def test_func(self, **kwargs):
        '''アクセスできるユーザーを制限'''
        pk = self.kwargs["pk"]
        post = Content.objects.get(pk=pk)
        return (post.user == self.request.user)

class ContentDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    '''投稿削除ページ'''
    model = Content
    template_name = 'delete.html'
    success_url = reverse_lazy('list')

    def test_func(self, **kwargs):
        '''アクセスできるユーザーを制限'''
        pk = self.kwargs["pk"]
        post = Content.objects.get(pk=pk)
        return (post.user == self.request.user)

        # 表示するfieldをHTML上で決める