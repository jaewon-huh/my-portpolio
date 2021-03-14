from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post, Category
from django.contrib.auth.models import User
class TestView(TestCase):        #TestCase 상속받은 클래스 정의
    def setUp(self):
        self.client =Client()
        self.user_trump = User.objects.create_user(username='trump',password='somepassword')
        self.user_obama = User.objects.create_user(username='obama', password='somepassword')

        self.category_programming = Category.objects.create(name='programming', slug='programming')
        self.category_music = Category.objects.create(name='music', slug='music')
        #test_post_list의 포스트요소들 setup으로 옮겨 공통적 적용
        self.post_001 = Post.objects.create(
            title='첫 번째 포스트입니다.',
            content='Hello World . We are the World.',
            category=self.category_programming,
            author=self.user_trump
             )
        self.post_002 = Post.objects.create(
            title='두 번째 포스트입니다.',
            content='1등이 전부는 아니잖아요.ㅎ',
            category=self.category_music,
            author=self.user_obama
            )
        self.post_003 = Post.objects.create(
            title='세 번째 포스트입니다.',
            content='카테고리가 없다',
            author=self.user_obama
            )
    def navbar_test(self, soup): #soup 매개변수 BS로 요소 가져와서 테스트
        navbar = soup.nav
        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', navbar.text)
        #제대로된 링크로 잘 연결되는지 확인하는 함수
        logo_btn = navbar.find('a', text='Do it Django')
        self.assertEqual(logo_btn.attrs['href'], '/')

        home_btn = navbar.find('a', text='Home')
        self.assertEqual(home_btn.attrs['href'], '/')

        blog_btn = navbar.find('a', text='Blog')
        self.assertEqual(blog_btn.attrs['href'], '/blog/')

        about_me_btn = navbar.find('a', text='About Me')
        self.assertEqual(about_me_btn.attrs['href'], '/about_me/')

    def category_card_test(self, soup):
        categories_card = soup.find('div', id='categories-card')    #id가 categories-card 인 div 찾기
        self.assertIn('Categories', categories_card.text)           # 그 div text 중 Categories 문구 찾기
        self.assertIn(f'{self.category_programming.name} ({self.category_programming.post_set.count()})', categories_card.text)  # 모든 카테고리가 제대로 출력?
        self.assertIn(f'{self.category_music.name} ({self.category_music.post_set.count()})', categories_card.text)
        self.assertIn(f'미분류 (1)', categories_card.text) # 카테고리가 없는 포스트 개수가 미분류 항목 옆 괄호에 써 있는지

    def test_post_list(self):
        # 포스트가 있는 경우
        self.assertEqual(Post.objects.count(),3)

        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.navbar_test(soup)
        self.category_card_test(soup)

        main_area = soup.find('div', id='main-area')
        self.assertNotIn('아직 게시물이 없습니다', main_area.text)

        post_001_card = main_area.find('div', id='post-1')
        self.assertIn(self.post_001.title, post_001_card.text)
        self.assertIn(self.post_001.category.name, post_001_card.text)

        post_002_card = main_area.find('div', id='post-2')
        self.assertIn(self.post_002.title, post_002_card.text)
        self.assertIn(self.post_002.category.name, post_002_card.text)

        post_003_card = main_area.find('div', id='post-3')
        self.assertIn('미분류', post_003_card.text)
        self.assertIn(self.post_003.title, post_003_card.text)

        self.assertIn(self.user_trump.username.upper(), main_area.text)
        self.assertIn(self.user_obama.username.upper(), main_area.text)

        #포스트가 없는 경우
        Post.objects.all().delete()
        self.assertEqual(Post.objects.count(), 0)
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')
        main_area = soup.find('div', id='main-area')  # id가 main-area인 div태그를 찾습니다.
        self.assertIn('아직 게시물이 없습니다', main_area.text)


def test_post_detail(self):
        # 1.   포스트가 하나 있다.
        post_001 = Post.objects.create(
            title='첫 번째 포스트입니다.',
            content='Hello World . We are the World.',
            author=self.user_trump
        )
        # 1.1  그 포스트의 url은 'blog/1/' 이다.
        self.assertEqual(post_001.get_absolute_url(), '/blog/1/')

        # 2.   첫 번째 post의 detail 페이지 테스트
        # 2.1  첫 번째 post url로 접근하면 정상적으로 작동한다. (status code: 200)
        response = self.client.get(post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        # 2.2  post_list 페이지와 똑같은 네비게이션 바가 있다.
        #navbar = soup.nav  # beautifulsoup를 이용하면 간단히 페이지의 태그 요소에 접근이 가능합니다.
        #self.assertIn('Blog', navbar.text)
        #self.assertIn('About Me', navbar.text)
        self.navbar_test(soup)
        # 2.3  첫 번째 post의 title이 웹 브라우저 탭 타이틀에 들어있다.
        self.assertIn(post_001.title, soup.title.text)

        # 2.4  첫 번째 post의 title이 post-area에 있다.
        main_area = soup.find('div', id='main-area')
        post_area = main_area.find('div', id='post-area')
        self.assertIn(post_001.title, post_area.text)

        # 2.5  첫 번째 post의 작성자(author)가 post-area에 있다.
        self.assertIn(self.user_trump.username.upper(), post_area.text)

        # 2.6  첫 번째 post의 content가 post-area에 있다.
        self.assertIn(post_001.content, post_area.text)

# Create your tests here.
