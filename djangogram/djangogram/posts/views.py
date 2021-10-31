from django.shortcuts import render, get_object_or_404
from djangogram.users.models import User as user_model
from . import models

from .forms import CreatePostForm, CommentForm

# Create your views here.
def index(request):
    return render(request, 'posts/base.html')

def post_create(request):
    if request.method == 'GET':
        form = CreatePostForm()
        return render(request, 'posts/post_create.html', {"form": form})
    
    elif request.method == 'POST':
        if request.user.is_authenticated: # 인증되었는지 확인
            user = get_object_or_404(user_model, pk=request.user.id)

            # 해당 부분 대신 CreatePostForm 로 대체
            # image = request.FILES['image']
            # caption = request.POST['caption']

            # new_post = models.Post.objects.create(
            #     author = user,
            #     image = image,
            #     caption = caption
            # )
            # new_post.save()

            form = CreatePostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = user
                post.save()
            else:
                print(form.errors)

            return render(request, 'posts/main.html')

        else:
            return render(request, 'users/main.html')
            
            