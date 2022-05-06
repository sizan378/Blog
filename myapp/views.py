import email

from django.shortcuts import render,get_object_or_404,redirect,Http404,HttpResponse
from .models import Author,Category,Article,Comment
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from .form import  createForm,createAuthor,commnetFrom,categoryForm,registerUser,CustomerRegistrationForm
from django.contrib import messages
from django.views import View
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail
from .token import activation_token
from django.core.mail import send_mail
from .require import renderPdf


def index(request):
    post=Article.objects.all()
    search=request.GET.get('q')
    if search:
        post=post.filter(
            Q(title__icontains=search) |
            Q(article_author__name__username__icontains=search) |
            Q(category__name__icontains=search) |
            Q(body__icontains=search)
        )
    paginator = Paginator(post, 4)  # Show 25 contacts per page.

    page_number = request.GET.get('page')
    total_article = paginator.get_page(page_number)
    contex={
        "post":total_article
    }
    return render(request,'index.html',contex)

def getauthor(request,name):
    post_author=get_object_or_404(User,username=name)
    auth=get_object_or_404(Author,name=post_author.id)
    post=Article.objects.filter(article_author=auth.id)
    paginator = Paginator(post, 4)  # Show 25 contacts per page.

    page_number = request.GET.get('page')
    total_article = paginator.get_page(page_number)
    contex={
        "auth":auth,
        "post":total_article
    }
    return render(request,'profile.html',contex)

def getsingle(request,id):
    post=get_object_or_404(Article,pk=id)
    get_comment=Comment.objects.filter(post=id)
    related=Article.objects.filter(category=post.category).exclude(id=id)[:2]
    form=commnetFrom(request.POST or None)
    if form.is_valid():
        instance=form.save(commit=False)
        instance.post=post
        instance.save()
    context={
        "post":post,
        "related":related,
        "form":form,
        "comment":get_comment,

    }
    return render(request,'single.html',context)

def getTopic(request,name):
    cat=get_object_or_404(Category,name=name)
    post=Article.objects.filter(category=cat.id)
    return render(request,'category.html',{"post":post,"cat":cat})


def getLogin(request):
    if request.user.is_authenticated:
        return redirect('blog:index')
    else:
        if request.method =="POST":
            username=request.POST.get('username')
            password=request.POST.get('password')
            auth=authenticate(username=username,password=password)
            if auth is not None:
                login(request,auth)
                return redirect('blog:index')
            else:
                messages.error(request, 'Username or Password wrong!😭😭😭😭😭')
    return render(request,'login.html')

def Logout(request):
    logout(request)
    return redirect('blog:index')

def getCreate(request):
    u=get_object_or_404(Author,name=request.user.id)
    form=createForm(request.POST or None,request.FILES or None)
    if form.is_valid():
        instance=form.save(commit=False)
        instance.article_author=u
        instance.save()
        return redirect('blog:index')
    return render(request,'create.html',{"form":form})

def getProfile(request):
    user=get_object_or_404(User, id=request.user.id)
    author_profile=Author.objects.filter(name=user.id)
    if author_profile:
        authorUser=get_object_or_404(Author,name=request.user.id)
        post=Article.objects.filter(article_author=authorUser.id)
        return render(request,'author.html',{"post":post,"user":authorUser})
    else:
        form=createAuthor(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.name=user
            instance.save()
            return redirect('blog:profile')
        return render(request,'create_author.html',{"form":form})

def getUpdate(request,id):
    u=get_object_or_404(Author,name=request.user.id)
    post=get_object_or_404(Article,pk=id)
    form=createForm(request.POST or None,request.FILES or None,instance=post)
    if form.is_valid():
        instance=form.save(commit=False)
        instance.article_author=u
        instance.save()
        messages.success(request, 'Update successfully complete 💚💚💚💚💚')
        return redirect('blog:profile')
    return render(request,'create.html',{"form":form})


def getDelete(request, id):
    post = get_object_or_404(Article, pk=id)
    post.delete()
    messages.warning(request, 'Delete successfully complete 💛💛💛💛💛')
    return redirect('blog:profile')

def getRegister(request):
    form=CustomerRegistrationForm(request.POST or None)
    if form.is_valid():
        instance=form.save(commit=False)
        instance.is_active=False
        instance.save()
        messages.success(request,'Registration is successfully completed')
        return redirect('blog:login')
    return render(request,'signup.html',{"form":form})

def getCategory(request):
    query=Category.objects.all()
    return render(request,'create_category.html',{"query":query})

def createTopic(request):
   if request.user.is_staff or request.user.is_superuser:
       form = categoryForm(request.POST or None)
       if form.is_valid():
           instance = form.save(commit=False)
           instance.save()
           return redirect('blog:category')
       return render(request, 'add_category.html', {"form": form})
   else:
       raise Http404('You are not authorized to access this page')

class pdf(View):
    def get(self,request,id):
        try:
            query=get_object_or_404(Article,id=id)
        except:
            Http404('Content Not Found')
            context={
                "query":query
            }
            article_pdf=renderPdf('pdf.html',context)
            return HttpResponse(article_pdf,content_type='applications/pdf')