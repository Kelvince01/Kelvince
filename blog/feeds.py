from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Article
from django.urls import reverse
from django.utils.feedgenerator import Atom1Feed


class LatestArticlesFeed(Feed):
    title = "Kelvince"
    link = ""
    description = "New posts of my blog."

    def items(self):
        return Article.objects.filter(status=1)

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.description, 30)

    def item_content(self, item):
        return truncatewords(item.content, 30)

    # Only needed if the model has no get_absolute_url method
    # def item_link(self, item):
    #     return reverse("article", args=[item.slug])

class MyFeed(Feed):
    feed_type = Atom1Feed