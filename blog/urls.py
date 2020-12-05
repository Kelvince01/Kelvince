from django.urls import path
from . import views
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import ArticleSitemap
from .feeds import LatestArticlesFeed

sitemaps = {
    "articles": ArticleSitemap,
}

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),

    path('search/', views.search, name='search'),
    path('articles', views.articles, name='articles'),
    path('articles/<slug:slug>/', views.article, name='article'),

    path('category/<slug:slug>/', views.category, name='category'),
    path('categories', views.categories, name='categories'),

    path('tags', views.tags, name='tags'),
    path('tag/<slug:slug>/', views.tag, name="tag"),
    path('archives', views.archives, name='archives'),

    path('portifolio', views.portifolio, name='portifolio'),
    path('terms_of_service', views.terms_of_service, name='terms_of_service'),
    path('privacy_policy', views.privacy_policy, name='privacy_policy'),

    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    path("feed/rss", LatestArticlesFeed(), name="article_feed"),
]