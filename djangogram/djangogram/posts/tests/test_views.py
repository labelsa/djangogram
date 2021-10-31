from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class TestPosts(TestCase):
    # 테스트시 setUp 함수가 제일 먼처 실행된다
    # 인증 테스트를 위해 사용자 추가 하는 코드 작성
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username='jungo', email='jungo@gamil.com', password='top_secret'
        )
    
    # get 테스트 - post 입력 화면 열림 확인 테스트
    def test_get_posts_page(self):
        url = reverse('posts:post_create')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/post_create.html')
    
    # post 테스트 - 로그인 성공시 테스트
    def test_post_creating_posts(self):
        login = self.client.login(username="jungo", password="top_secret")
        self.assertTrue(login)

        url = reverse('posts:post_create')
        image = SimpleUploadedFile("test.jpg", b"whatevercontents") # (사진이미지이름, 사진바이너리 데이터)
        response = self.client.post(
            url,
            {"image": image, "caption": 'test'}
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "posts/base.html")
    
    # post 테스트 - 로그인 없이 테스트 
    def test_post_posts_create_not_login(self):
        url = reverse('posts:post_create')
        image = SimpleUploadedFile("test.jpg", b"whatevercontents") # (사진이미지이름, 사진바이너리 데이터)
        response = self.client.post(
            url,
            {"image": image, "caption": 'test test'}
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/main.html")