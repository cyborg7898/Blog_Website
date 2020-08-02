from django.shortcuts import render,get_object_or_404
from django.views import generic
from .models import Post,Like,Comment
from .forms import CommentForm,BlogForm
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator

class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'

@login_required
def like_post(request):
    user=request.user
    if request.method=="POST":
        post_id=request.POST.get('post_id')
        post_obj=Post.objects.get(id=post_id)
        id=request.POST.get('post_id')
        if user in post_obj.liked.all():
            post_obj.liked.remove(user)
        else:
            post_obj.liked.add(user)
        like,created=Like.objects.get_or_create(user=user,post_id=post_id)

        if not created:
            if like.value=='Like':
                like.value='Unlike'
            else:
                like.value='Like'
        like.save()
    return redirect("post_detail",post_id)

@login_required
def post_detail(request, post_id):
    user=request.user
    context={
        'user':user
    }
    template_name = 'post_detail.html'
    post = get_object_or_404(Post, pk=post_id)
    # comments = post.comments.filter(name=request.user)
    comments = post.comments.filter(active=True)
    new_comment = None
    # Comment posted

    if request.method == 'POST':

        comment_form = CommentForm(data=request.POST)
        # if comments:
        #     messages.error(request,"Sorry one user can add only one comment")
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.name=request.user
            print()
            new_comment.save()
            return redirect("post_detail",post_id)
    else:
        comment_form = CommentForm()

    return render(request ,template_name,{'post': post,'user':user,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})
@login_required
def postblog(request):
    if request.method=="POST":
        blog_form=BlogForm(request.POST,initial={'author':request.user.username})
        if blog_form.is_valid():
            instance = blog_form.save(commit=False)
            instance.author = request.user
            instance.save()
            messages.success(request,("Blog Posted"))
            return redirect('home')
    else:
        blog_form=BlogForm()
    return render(request,'postblog.html',{'blog_form':blog_form})

def about(request):
    context={'about_text':"About us Page",
             }
    return render(request,'about.html',context)

def contact(request):
    context={'contact_text':"GitHub:https://github.com/cyborg7898/Blog_Website",
             }
    return render(request,'contact.html',context)




