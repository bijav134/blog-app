import re
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls.base import reverse_lazy
from blog import forms
from django.core.mail import send_mail
import random
from django.conf import Settings
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse,reverse_lazy
from django.contrib.auth.decorators import login_required
from blog import models
from django.views.generic import (CreateView,UpdateView,ListView,DeleteView,DetailView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.shortcuts import get_object_or_404
# Create your views here.
def index(request):
    return render(request,'base.html')



user=0

def otp_verify(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        cotp = request.POST.get('conf_otp')

        if int(otp)==int(cotp):
            global user
            user.save()

            return HttpResponse('<h1> Successfully register </h1>')

def register(request):
    form = forms.UserModelForm()
    if request.method=='POST':
        form = forms.UserModelForm(request.POST)
        if form.is_valid():
            global user
            user = form.save(commit = False)
            password = request.POST.get('password')
            mail = request.POST.get('email')
            user.set_password(password)

            otp = random.randint(1111,9999)

            send_mail(
            'OTP Verification',
            f"Your OTP for registration is {otp}",
            'settings.EMAIL_HOST_USER',
            [mail],
            fail_silently=False,
            )

        dct = {'otp': otp}
        return render(request, 'registration/otp.html', dct)


        return HttpResponse('Registration successful')

    return render(request, 'registration/register.html', {'form': form})
#####################################################################################

def user_login(request):
    if request.method=='POST':
        username= request.POST.get('username')
        password= request.POST.get('password')

        user= authenticate(username=username, password=password)
        if user:

            if user.is_active:
                login(request,user)
                request.session['user_login']= True

                request.session['username']=username

                print('suceessful log in')

                return HttpResponseRedirect(reverse('app:index'))
        else:
            return HttpResponse('<h1>Invalid credential</h1>')


    return render(request, 'registration/web_login.html')


def user_logout(request):
    del request.session['user_login']
    del request.session['username']

    logout(request)

    return HttpResponseRedirect(reverse('app:index'))

###########################################################################
@login_required
def user_profile(request):
    form=forms.UserProfileForm()
    if request.method=='POST':
        form=forms.UserProfileForm(request.POST,request.FILES)
        if form.is_valid():
            profile=form.save(commit=False)
            username=request.session['username']
            user=models.User.objects.get(username=username)
            profile.user= user

            if 'prof_pic' in request.FILES:
                profile.prof_pic= request.FILES['prof_pic']

            profile.save()

        else:
            print(form.errors)
            return HttpResponse('<h1> Invalid Form  </h1>')
    return render(request, 'registration/profile.html', {'form':form})
#########################################################################################

class CreatePostView(LoginRequiredMixin,CreateView):
    model = models.Post
    login_url='/blogs/login/'
    #fields=('author','title','text')
    #redirect_field_name=""
    form_class=forms.PostModelForm

    def form_valid(self, form):
        if form.is_valid():

            obj=form.save(commit=False)
            username=self.request.session['username']
            user=models.User.objects.get(username=username)

            if obj.author == user:
                form=forms.PostModelForm(self.request.POST)
                return super().form_valid(form)
            
            else:
                return HttpResponse('<h1> Invalid Username </h1>')
        else:
            return HttpResponse('<h1> Invalid Form </h1>')

class PostDetailView(DetailView):
    model=models.Post


class PostListView(ListView):
    model=models.Post

    def get_queryset(self):
        return models.Post.objects.filter(published_date__lte = timezone.now()).order_by('-published_date')

class DraftListView(LoginRequiredMixin,ListView):
    model=models.Post
    login_url = '/blogs/login/'

    def get_queryset(self):
        username=self.request.session['username']
        user=models.User.objects.get(username=username)
        return models.Post.objects.filter(author=user,published_date__isnull = True).order_by('created_date')

class PostUpdateView(UpdateView):
    model=models.Post
    fields=('title','text')

class PostDeleteView(LoginRequiredMixin,DeleteView):
    model=models.Post
    login_url='/blogs/login/'
    success_url=reverse_lazy('app:post_list')

@login_required
def post_publish(request,pk):
    post=get_object_or_404(models.Post, pk=pk)

    post.publish()
    return HttpResponse('<h1> Post Published </h1>')

def add_comment(request,pk):
    if request.method=='POST':
        form=forms.CommentModelForm(request.POST)
        if form.is_valid():
            obj=form.save(commit=False)
            post=get_object_or_404(models.Post, pk=pk)

            obj.post=post
            obj.save()
            return HttpResponseRedirect(reverse('app:post_detail', kwargs= {'pk':pk}))
    else:
        form=forms.CommentModelForm()
        return render(request, 'blog/comment.html',{'form':form, 'pk':pk})

