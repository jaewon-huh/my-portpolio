#from django.shortcuts import render
from django.views.generic import ListView,DetailView  #ListView 클래스로 포스트 목록페이지 만들기 +DetailView
from .models import Post #models.py에 정의된 Post모델을 임포트

class PostList(ListView):
    model = Post
    ordering ='-pk'
   #template_name = 'blog/post_list.html'
#아래는 FBV방식
#def index(request):
#   posts = Post.objects.all().order_by('-pk')   #모든 Post레코드를 가져와 posts에 저장

#    return render(
#        request,
#        'blog/post_list.html',   #blog/post_list.html 파일에 화면에 출력할 내용
#       {
#            'posts': posts,    #posts를 딕셔너리로 추가
#        }
#    )
#def single_post_page(request, pk) :
#    post = Post.objects.get(pk=pk)
#
#    return render(
#       request,
#       'blog/post_detail.html',
#       {
#            'post' :post,
#       }
#        )
class PostDetail(DetailView):
    model = Post

    #render() : 요청이 들어오면 주소를 반환해준다