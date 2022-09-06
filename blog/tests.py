import tempfile
import shutil

from django.conf import settings
from django.core.cache import cache
from django.db.models import QuerySet
from django.test import TestCase, Client,override_settings
from .models import Post, Comment,Tag
from .forms import CommentForm,AddPostForm,CustomCreationForm
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile




class BlogTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username="Roman", email="roman@gmail.com", password="gr1985r69")
        cls.post = Post.objects.create(title="Hello My Beautiful World", content="Hello", excerpt="hello")
        cls.tag = Tag.objects.create(caption="Cool!")
        settings.MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)

    def setUp(self):
        cache.clear()
        print("Cache is cleared!")
        self.authorized_user = Client()
        self.authorized_user.force_login(self.user)


    def tearDown(self):
        super().tearDown()
        shutil.rmtree(settings.MEDIA_ROOT,ignore_errors=True)
        print("tearDown!")

class ViewTest(BlogTest):
# ----------------------------- test view ---------------------------
    def test_templates(self):
        templates = {
            "blog/start_page.html": reverse("start-page"),
            "blog/post_detail.html": reverse("post-details", kwargs={"slug": self.post.slug}),
            "blog/add_post.html": reverse("add-post"),
        }
        for template, reverse_name in templates.items():
            with self.subTest(template):
                response = self.authorized_user.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_start_page_context(self):
        response = self.authorized_user.get(reverse("start-page"))
        self.assertIsInstance(response.context["posts"], QuerySet)

    def test_all_posts_context(self):
        response = self.authorized_user.get(reverse("all-posts"))
        self.assertIsInstance(response.context["posts"], QuerySet)

    def test_post_detail_GET(self):
        response = self.authorized_user.get(reverse("post-details", args=[self.post.slug]))
        self.assertIsInstance(response.context["post"], Post)
        self.assertIsInstance(response.context["tags"], QuerySet)
        self.assertIsInstance(response.context["comment_form"], CommentForm)
        self.assertIsInstance(response.context["comment_list"], QuerySet)
        self.assertIsInstance(response.context["is_set_to_read"], bool)

    def test_post_detail_POST(self):
        response = self.authorized_user.post(reverse("post-details", args=[self.post.slug]),{
            "user_name":"Ivan",
            "email":"ivan@gmail.com",
            "text": "Great!Great!Great!"
        })

        self.assertEqual(self.post.comments.get(user_name="Ivan").text,"Great!Great!Great!")

        self.assertTrue(self.post.comments.get(user_name="Ivan"))

    def test_unread_post_GET(self):

        response = self.authorized_user.get(reverse("to-read"))
        # print(response.context)
        print(response.cookies)
        # print(response.content.decode())
        self.assertIsInstance(response.context["post_to_read"],list)
        self.assertIsInstance(response.context["is_empty"],bool)

    def test_unread_post_POST(self):
        response = self.authorized_user.post(reverse("to-read"),{
            "post_id": 1,
        })
        # print(response.context)
        self.assertEqual(self.authorized_user.session["to_read"],[1])
        self.assertRedirects(response,reverse("post-details",args=[self.post.slug]))

# ------------------------ model test ----------------------------

class ModelTest(BlogTest):

    def test_post_save(self):
        self.assertEqual(self.post.slug,"hello-my-beautiful-world")

    def test_post_validator_check(self):
        print(self.post.content)
        print(self.post._meta.get_field("content").validators[0].limit_value)
        print(self.post._meta.get_field("content").validators[0].message)

        content_invalid = Post(content="roma")
        with self.assertRaises(ValidationError):
            content_invalid.full_clean()
            content_invalid.save()
# ------------------------ form test -----------------------------


class FormTest(BlogTest):



    def test_add_post_form(self):
        with open("uploads/images/BCLI9784.JPG","rb") as pic:
            pic_str = pic.read()


        image = SimpleUploadedFile(name="image.jpg",content=pic_str,content_type="image/jpeg")
        # tag as m2m field should be tested as per its' value in DB ,
        # in our test case we have created one only tag == "Cool!"
        # so value == [1] --> nice visible in API --> "tag": [1,3]
        form_data = {
           "title":"Grom85",
            "content": "Hello grom85!",
            "excerpt": "BLABALBLA",
            "image": image,
            "tag": [1],
        }

        response = self.authorized_user.post(reverse("add-post"),data=form_data,)
        # print(response.context["errors"])
        self.assertTrue(Post.objects.get(title="Grom85"))
        self.assertEqual(Post.objects.count(),2)



