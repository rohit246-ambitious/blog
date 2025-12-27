
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from .models import Blog, Category, Comment
from django.db.models import Q

def posts_by_category(request, category_id):
    #fetch the posts that belong to the given category_id
    posts = Blog.objects.filter(category_id=category_id, status="Published")

    #undifined category handling
    try:
       category = Category.objects.get(pk=category_id)
    except:
       return redirect('home')
    
    #this is an alternative way to handle undifined category using get_object_or_404
    #category = get_object_or_404(Category, pk=category_id)
    context = {
        'posts': posts,
        'category': category
    }
    return render(request, 'posts_by_category.html', context)

def blogs(request, slug):
   single_blog = get_object_or_404(Blog, slug=slug, status="Published")
   if request.method == 'POST':
        comment = Comment()
        comment.user = request.user
        comment.blog = single_blog
        comment.comment = request.POST['comment']
        comment.save()
        return HttpResponseRedirect(request.path_info)

   #comment 
   comments = Comment.objects.filter(blog=single_blog)
   comment_count = comments.count()
   context = {
       'single_blog': single_blog,
       'comments': comments,
        'comment_count': comment_count
   }
   return render(request, 'blogs.html', context)

def search(request):
    keyword = request.GET.get('keyword')
    if keyword:
        posts = Blog.objects.filter(Q(title__icontains=keyword) | Q(short_description__icontains=keyword) | Q(blog_body__icontains=keyword), status="Published")
    else:
        posts = Blog.objects.none()
    context = {
        'posts': posts,
        'keyword': keyword
    }
    return render(request, 'search.html', context)