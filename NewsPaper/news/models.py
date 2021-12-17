from django.db import models
from django.contrib.auth.models import User

from django.db.models import Sum
from datetime import datetime


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.SmallIntegerField(default=0)

    def __str__(self):
        return f'{self.user.username}'

    def update_rating(self):
        self.rating = 0
        author_comments = self.user.comment_set.all()
        for c in author_comments:
            self.rating += c.rating
        author_posts = self.post_set.all()
        for p in author_posts:
            if p.post_type == ARTICLE:
                self.rating += p.rating * 3
                p_comments = p.comment_set.all()
                for c in p_comments:
                    self.rating += c.rating
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return f'{self.name}'


NEWS = 'NW'
ARTICLE = 'AR'

POST_DICT = {NEWS: 'Новость', ARTICLE: 'Статья'}

POST_TYPES = tuple(POST_DICT.items())


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2, choices=POST_TYPES, default=NEWS)
    time_stamp = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def __str__(self):
        return f'{POST_DICT[self.post_type]} "{self.title}"'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:124] + '...'

    def post_info(self, header):
        print(header)
        print(f'Название 	: {self.title}')
        print(f'Рейтинг 	: {self.rating}')
        print(f'Coздано 	: {self.time_stamp}')
        print(f'Автор   	: {self.author.user.username}')
        print(f'Рейтинг	    : {self.author.rating}')
        print(f'Превью  	: {self.preview()}')

    def comment_list(self):
        c_list = self.comment_set.all()
        print(f'Комментарии к статье "{self.title}"')
        for c in c_list: print(c.text)


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    time_stamp = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def __str__(self):
        return f'Комментарий на "{self.post.title}"'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()