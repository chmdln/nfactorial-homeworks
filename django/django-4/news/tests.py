from django.test import TestCase
from .models import News, Comment


# Create your tests here.

class NewsModelTests(TestCase):
    def test_has_comments_true(self):
        news = News.objects.create(title="Test news", content="Test content")
        comment = Comment.objects.create(content="Test comment", news=news)
        self.assertIs(True, news.has_comments())

    def test_has_comments_false(self):
        news = News.objects.create(title="Test news", content="Test content")
        self.assertIs(False, news.has_comments())


class NewsViewsTests(TestCase): 
    # test for news_list view
    def test_news_list_descending_order(self):
        news1 = News.objects.create(title="Test news 1", content="Test content 1")
        news2 = News.objects.create(title="Test news 2", content="Test content 2")

        response = self.client.get("/news/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "news/news_list.html")
        self.assertQuerySetEqual(response.context["news_list"], [news2, news1])

    # test for news_detail view 
    def test_news_detail(self):
        news = News.objects.create(title="Test news details", content="Test content details")
        comment1 = Comment.objects.create(content="Test comment for news details", news=news)
        response = self.client.get(f"/news/{news.id}/")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "news/news_detail.html")
        self.assertEqual(response.context["news"], news)    
        self.assertContains(response, "Test news details")
        self.assertContains(response, "Test content details")
        self.assertContains(response, "Test comment for news details")

    
    def test_news_detail_descending_comments(self):
        news = News.objects.create(title="Test news details", content="Test content details")
        comment1 = Comment.objects.create(content="Test comment for news details 1", news=news)
        comment2 = Comment.objects.create(content="Test comment for news details 2", news=news)
        response = self.client.get(f"/news/{news.id}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["comments"]), 2)
        self.assertQuerySetEqual(response.context["comments"], [comment2, comment1])
        self.assertContains(response, "Test comment for news details 1")
        self.assertContains(response, "Test comment for news details 2")