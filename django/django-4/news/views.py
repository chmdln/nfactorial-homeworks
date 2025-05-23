from django.views import View
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import now
from django.urls import reverse
from .forms import NewsForm, CommentForm, EditNewsForm
from .models import News


# Create your views here.

def news_list(request):
    news_list = News.objects.order_by("-created_at")
    return render(
        request=request, 
        template_name="news/news_list.html", 
        context={"news_list": news_list}
    )



def news_detail(request, news_id):
    news_item = get_object_or_404(News, id=news_id)
    comments = news_item.comments.order_by("-created_at")

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.created_at = now()  
            comment.news = news_item
            comment.save()
            return HttpResponseRedirect(reverse("news:news_detail", args=(news_item.id,)))
    else:
        form = CommentForm()

    return render(
        request=request, 
        template_name="news/news_detail.html", 
        context={
            "news": news_item, 
            "comments": comments,
            "comment_form": form
        }
    )


def news_form(request):
    if request.method == "POST":
        form = NewsForm(request.POST)
        if form.is_valid():
            news_item = form.save(commit=False)
            news_item.created_at = now()  
            news_item.save()
            return HttpResponseRedirect(reverse("news:news_detail", args=(news_item.id,)))
    else:
        form = NewsForm()
    return render(
        request=request, 
        template_name="news/news_form.html", 
        context={"form": form}
    )


class EditNewsView(View):
    def get(self, request, news_id):
        news_item = get_object_or_404(News, id=news_id)
        form = EditNewsForm(instance=news_item)
        return render(
            request=request, 
            template_name="news/news_form_edit.html", 
            context={"news": news_item, "form": form}
        )
    
    def post(self, request, news_id):
        news_item = get_object_or_404(News, id=news_id)
        form = EditNewsForm(request.POST, instance=news_item)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("news:news_detail", args=(news_item.id,)))
        return render(
            request=request, 
            template_name="news/news_detail.html", 
            context={
                "news": news_item, 
                "comments": news_item.comments,
                "comment_form": form
            }
        )

