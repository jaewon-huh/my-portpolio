from django.shortcuts import render
from .models import Post  #models.py에 정의된 Post모델을 임포트
# Create your views here.

def index(request):
    posts = Post.objects.all().order_by('-pk')   #모든 Post레코드를 가져와 posts에 저장

    return render(
        request,
        'blog/index.html',   #blog/index.html 파일에 화면에 출력할 내용
        {
            'posts': posts,    #posts를 딕셔너리로 추가
        }
    )
def single_post_page(request, pk) :
    post = Post.objects.get(pk=pk)

    return render(
        request,
        'blog/single_post_page.html',
        {
            'post' :post,
        }
    )
    #render() : 요청이 들어오면 주소를 반환해준다