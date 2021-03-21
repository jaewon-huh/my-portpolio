from django.shortcuts import render ,redirect
from django.views.generic import ListView, DetailView, CreateView #ListView 클래스로 포스트 목록페이지 만들기 +DetailView
from django.contrib.auth.mixins import LoginRequiredMixin #로그인 했을때만 페이지가 보이게
from .models import Post, Category , Tag #models.py에 정의된 Post모델을 임포트

class PostList(ListView):
    model = Post
    ordering = '-pk'

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context

def category_page(request, slug):
    if slug == 'no_category':
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)

    return render(
        request,
        'blog/post_list.html',
        {
            'post_list': post_list,
            'categories': Category.objects.all(),
            'no_category_post_count': Post.objects.filter(category=None).count(),
            'category': category,
        }
    )
def tag_page(request, slug):
        tag = Tag.objects.get(slug=slug)
        post_list = tag.post_set.all()

        return render(
        request,
        'blog/post_list.html',
        {
            'post_list': post_list,
            'categories': Category.objects.all(),
            'no_category_post_count': Post.objects.filter(category=None).count(),
            'tag': tag,
        }
    )
class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title','hook_text','content','head_image','file_upload','category']

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.author = current_user
            return super(PostCreate, self).form_valid(form)
        else:
            return redirect('/blog/')


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

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context

    #render() : 요청이 들어오면 주소를 반환해준다