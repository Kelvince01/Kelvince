from .models import Article

def articles_archive(request):
    return {
        'all_posts': Article.objects.order_by('-created_on'),
    }