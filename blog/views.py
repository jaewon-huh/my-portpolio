from django.shortcuts import render ,redirect
from django.views.generic import ListView, DetailView, CreateView , UpdateView#ListView 클래스로 포스트 목록페이지 만들기 +DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin  #로그인 했을때만 페이지가 보이게
from .models import Post, Category , Tag #models.py에 정의된 Post모델을 임포트
from .forms import CommentForm
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify
from django.shortcuts import get_object_or_404

class PostList(ListView):
    model = Post
    ordering = '-pk'

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context

class PostDetail(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        context['comment_form'] = CommentForm
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
class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    fields = ['title','hook_text','content','head_image','file_upload','category',]

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user
            response = super(PostCreate, self).form_valid(form)

            tags_str = self.request.POST.get('tags_str')
            if tags_str:
                tags_str = tags_str.strip()

                tags_str = tags_str.replace(',', ';')
                tags_list = tags_str.split(';')

                for t in tags_list:
                    t = t.strip()
                    tag, is_tag_created = Tag.objects.get_or_create(name=t)
                    if is_tag_created:
                        tag.slug = slugify(t, allow_unicode=True)
                        tag.save()
                    self.object.tags.add(tag)

            return response

        else:
                return redirect('/blog/')

class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title','hook_text','content','head_image','file_upload','category', 'tags']

    template_name = 'blog/post_update_form.html' # 원하는 html 파일을 템플릿 파일로 설정

    def get_context_data(self, **kwargs):   #템플릿으로 추가 인자를 넘기기 get_context_data
        context = super(PostUpdate, self).get_context_data()
        if self.object.tags.exists():       #태그가 있다면
            tags_str_list = list()          #리스트 생성
            for t in self.object.tags.all():        #태그들에 대해서
                tags_str_list.append(t.name)        #태그 이름들을 리스트에 넣음
            context['tags_str_default'] = ';'.join(tags_str_list)                #인자 정의 = 태그리스트를 ;로 구분하고 하나로 결합

        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate,self).dispatch(request,*args,**kwargs)  #방문자가 로그인, 작성자인 경우만 dispatch() 확인
        else:
            raise PermissionDenied

    def form_valid(self, form):
        response = super(PostUpdate, self).form_valid(form)
        self.object.tags.clear()

        tags_str = self.request.POST.get('tags_str')
        if tags_str:
            tags_str = tags_str.strip()
            tags_str = tags_str.replace(',', ';')
            tags_list = tags_str.split(';')

            for t in tags_list:
                t = t.strip()
                tag, is_tag_created = Tag.objects.get_or_create(name=t)
                if is_tag_created:
                    tag.slug = slugify(t, allow_unicode=True)
                    tag.save()
                self.object.tags.add(tag)

        return response


def new_comment(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)

        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
        else:
            return redirect(post.get_absolute_url())
    else:
        raise PermissionDenied


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

    #render() : 요청이 들어오면 주소를 반환해준다