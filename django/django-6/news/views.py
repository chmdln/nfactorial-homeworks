from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect 
from django.utils.timezone import now
from django.urls import reverse
from django.contrib.auth import login
from django.contrib.auth.models import Group 
from django.contrib.auth.decorators import login_required, permission_required
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from .serializers import NewsSerializer

from .forms import NewsForm, CommentForm, EditNewsForm, UserSignupForm, UserLoginForm
from .models import News, Comment 


######################### Django part 6 #########################
class NewsListAPIView(generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer 

class NewsCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = request.data.copy()
        data['author'] = request.user.id  
        serializer = NewsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class NewsDetailAPIView(generics.RetrieveAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if obj.author != request.user:
            self.message = "Unauthorized to delete the news."
            return False
        return True


class NewsDeleteAPIView(generics.DestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def delete(self, request, *args, **kwargs):
        news = self.get_object()
        if news.author != request.user:
            return Response({"detail": "Unauthorized to delete the news."}, status=status.HTTP_403_FORBIDDEN)
        return super().delete(request, *args, **kwargs)


######################### Django part 6 #########################



# Create your views here.
def signup(request):
    if request.method == "POST":
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save()

            default_group, created = Group.objects.get_or_create(name='default')
            user.groups.add(default_group)

            login(request, user)
            return redirect("news:news_list")
    else:
        form = UserSignupForm()
    return render(
        request=request, 
        template_name="news/registration/signup.html", 
        context={"form": form}
    )


def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data["user"]
            login(request, user)
            return redirect("news:news_list")
    else:
        form = UserLoginForm()
    
    return render(
        request=request, 
        template_name="news/registration/login.html", 
        context={"form": form}
    )


def news_list(request):
    news_list = News.objects.order_by("-created_at")
    return render(
        request=request, 
        template_name="news/news_list.html", 
        context={"news_list": news_list}
    )


# @permission_required("news.add_comment")
# don't use decorator, since unauthenticated users can't view the news or comments 
def news_detail(request, news_id):
    news_item = get_object_or_404(News, id=news_id)
    comments = news_item.comments.order_by("-created_at")

    if request.method == "POST":
        # only authenticated or those with perms can add comment
        if request.user.is_authenticated or request.user.has_perm("news.add_comment"):
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.created_at = now()  
                comment.news = news_item
                comment.author = request.user
                comment.save()
                return HttpResponseRedirect(reverse("news:news_detail", args=(news_item.id,)))
        else:
            return HttpResponseRedirect(reverse("login")) 
    else:
        form = CommentForm() if request.user.is_authenticated else ""

    return render(
        request=request, 
        template_name="news/news_detail.html", 
        context={
            "news": news_item, 
            "comments": comments,
            "comment_form": form
        }
    )


@login_required(login_url="/login/")
@permission_required("news.add_news", login_url="/login/")
def news_form(request):
    if request.method == "POST":
        form = NewsForm(request.POST)
        if form.is_valid():
            news_item = form.save(commit=False)
            news_item.created_at = now()  
            news_item.author = request.user
            news_item.save()
            return HttpResponseRedirect(reverse("news:news_detail", args=(news_item.id,)))
    else:
        form = NewsForm()
    return render(
        request=request, 
        template_name="news/news_form.html", 
        context={"form": form}
    )


@login_required(login_url="/login/")
# @permission_required("news.change_news", raise_exception=True)
def news_edit(request, news_id):
    news_item = get_object_or_404(News, id=news_id)

    # Only the author or a user with permission can proceed
    if request.user == news_item.author or (request.user != news_item.author and request.user.has_perm("news.change_news")):
        if request.method == "POST":
            form = EditNewsForm(request.POST, instance=news_item)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse("news:news_detail", args=(news_item.id,)))
        else:
            form = EditNewsForm(instance=news_item)
        
        return render(
            request=request, 
            template_name="news/news_form_edit.html", 
            context={"news": news_item, "form": form}
        )

    # Redirect unauthorized users
    return redirect("news:news_detail", news_id=news_id)
    


@login_required(login_url="/login/")
# @permission_required("news.delete_news", login_url="/login/")
def news_delete(request, news_id):
    news_item = get_object_or_404(News, id=news_id)
    if request.method == "POST":
        # delete news if current user is the author
        if request.user == news_item.author or (request.user != news_item.author and request.user.has_perm("news.delete_news")):
            news_item.delete()
            return HttpResponseRedirect(reverse("news:news_list"))
        return redirect("news:news_list")
   
        
def comment_delete(request, news_id, comment_id):
    comment_item = get_object_or_404(Comment, id=comment_id)
    if request.method == "POST":
        # delete comment if current user is the author
        if request.user == comment_item.author or (request.user != comment_item.author and request.user.has_perm("news.delete_comment")):
            comment_item.delete()
            return HttpResponseRedirect(reverse("news:news_detail", args=(news_id,))) 
    return redirect("news:news_detail", news_id=news_id)   


