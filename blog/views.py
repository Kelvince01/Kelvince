from django.contrib import messages
from django.shortcuts import redirect, render
from .models import Article, Category, Contact
from django.shortcuts import render, get_object_or_404
from .forms import CommentForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from taggit.models import Tag
from django.db.models import Q
from django.core.mail import send_mail

def index(request):
    articles = Article.objects.filter(status=1).order_by('-created_on')
    popular_articles = Article.objects.filter(status=1).order_by('-views')[0:3]
    popular_articles_home = Article.objects.filter(status=1).order_by('-views')[0:5]

    tags = Article.tags.all()
    categories = Category.objects.all()

    paginator = Paginator(articles, 10)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        article_list = paginator.page(page)
    except PageNotAnInteger:
            # If page is not an integer deliver the first page
        article_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        article_list = paginator.page(paginator.num_pages)

    context = {
        'article_list': article_list,
        'tags': tags,
        'categories': categories,
        'popular_articles': popular_articles,
        'popular_articles_home': popular_articles_home
    }

    return render(request, 'pages/index.html', context)

def about(request):
    context = {
        "title" : "About",
        "description" : "About the author Kelvince",
        "image": "https://kelvince.com/static/images/author.png",
        "url": "about",
        "created_on": "11/11/2020"
    }

    return render(request, 'pages/about.html', context=context)

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']

        contact = Contact(name=name, email=email, message=message)

        contact.save()

        send_mail("Website Contact", message, 'kelvince05@gmail.com', [ email, 'kelvince05@outlook.com'], fail_silently=False)

        messages.success(request, 'Your message has been sent, expect a feedback soon')

        return redirect('/contact')
    else:
        contact = Contact()
        #messages.error(request, 'Your message has not been sent, check fields!')
    
    context = {
        'contact': contact,
        "title" : "Portifolio",
        "description" : "Kelvince projects and works",
        "image": "https://kelvince.com/static/images/author.png",
        "url": "portifolio",
        "created_on": "11/11/2020"
    }

    return render(request, 'pages/contact.html', context=context)

def article(request, slug):
    template_name = 'pages/article.html'
    article = get_object_or_404(Article, slug=slug)
    article.increase_views()
    #tag = get_object_or_404(Tag, slug=slug)
    comments = article.comments.filter(active=True)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = article
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    context = {
        'article':article,
        'comments':comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
        "title" : article.title,
        "description" : article.description,
        "image": article.thumbnail,
        "url": "articles/"+article.slug,
        "created_on": article.created_on,
        "content": article.content
    }
    return render(request, template_name, context)

def articles(request):
    articles = Article.objects.filter(status=1).order_by('-created_on')
    popular_articles = Article.objects.filter(status=1).order_by('-views')[0:3]
    paginator = Paginator(articles, 4)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        article_list = paginator.page(page)
    except PageNotAnInteger:
            # If page is not an integer deliver the first page
        article_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        article_list = paginator.page(paginator.num_pages)

    context = {
        'article_list': article_list,
        'popular_articles': popular_articles
    }

    return render(request, 'pages/articles.html', context)

def recent_articles():
    recent_articles = Article.objects.filter(status=1).order_by('-created_on')[0:3]

    return recent_articles

def popular_articles(request):
    popular_articles = Article.objects.filter(status=1).order_by('-views')[0:3]

    return popular_articles

def search(request):
    query = request.GET.get('q','')
    #The empty string handles an empty "request"
    if query:
            queryset = (Q(title__icontains=query))
            #I assume "text" is a field in your model
            #i.e., text = model.TextField()
            #Use | if searching multiple fields, i.e., 
            #queryset = (Q(text__icontains=query))|(Q(other__icontains=query))
            results = Article.objects.filter(queryset).distinct()
    else:
       results = []
    return render(request, 'pages/search.html', {'results':results, 'query':query})

    #You can also set context = {'results':results, 'query':query} after 
    #the else: (same indentation as return statement), and 
    #use render(request, 'home.html', context) if you prefer. 

def categories(request):
    """this will get all categories, you can do some filtering if you need (e.g. excluding categories without posts in it
    
    Keyword arguments:
    argument -- categories
    Return: categories
    """
    popular_articles = Article.objects.filter(status=1).order_by('-views')[0:3]
    
    categories = Category.objects.all()

    return render(request, 'pages/categories.html', {'categories': categories, 'popular_articles': popular_articles})

def category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    context_dict = {}
    popular_articles = Article.objects.filter(status=1).order_by('-views')[0:3]

    try:
        category = Category.objects.get(slug=slug)
        context_dict['category_title'] = category.title
        articles = Article.objects.filter(category=category)
        context_dict['articles'] = articles
        context_dict['category'] = category
        context_dict['popular_articles'] = popular_articles
    except Category.DoesNotExist:
        pass
    #return render(request, 'pages/category.html', {'category': category})
    return render(request, 'pages/category.html', context_dict)

def tags(request):
    """The listing for tagged articles."""
    """template_name = "pages/tags.html"

    def get_queryset(self):
        return Article.objects.filter(tags__slug=self.kwargs.get("slug")).all()

    def get_context_data(self, **kwargs):
        context = super(tags, self).get_context_data(**kwargs)
        context["tag"] = self.kwargs.get("slug")
        return context"""
    popular_articles = Article.objects.filter(status=1).order_by('-views')[0:3]
    tags = Article.tags.all()

    return render(request, 'pages/tags.html', {'tags': tags, 'popular_articles': popular_articles})

def tag(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    # Filter posts by tag name  
    articles = Article.objects.filter(tags=tag)
    popular_articles = Article.objects.filter(status=1).order_by('-views')[0:3]
    context = {
        'tag':tag,
        'articles':articles,
        'popular_articles': popular_articles
    }
    return render(request, 'pages/tag.html',context)

def archives(request):
    entry_list = Article.objects.order_by('created_on')
    popular_articles = Article.objects.filter(status=1).order_by('-views')[0:3]

    return render(request, 'pages/archives.html', 
              {'entry_list':entry_list, 'popular_articles': popular_articles})

def portifolio(request):
    context = {
        "title" : "Portifolio",
        "description" : "Kelvince projects and works",
        "image": "https://kelvince.com/static/images/author.png",
        "url": "portifolio",
        "created_on": "11/11/2020"
    }
    return render(request, 'pages/portifolio.html', context=context)

def terms_of_service(request):
    return render(request, 'pages/terms_of_service.html')

def privacy_policy(request):
    return render(request, 'pages/privacy_policy.html')