from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils.timezone import now

STATUS=(
    (0,'Draft'),
    (1,'Publish')
)
class Post(models.Model):
    title=models.CharField(max_length=200,unique=True)
    slug=models.SlugField(max_length=200,editable=False,default='123')
    author=models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    #updated_on= models.DateTimeField()
    content = models.TextField(default=None)
    created_on=models.DateTimeField(default=datetime.datetime.now())
    status=models.IntegerField(choices=STATUS,default=1)
    liked=models.ManyToManyField(User,default=None,blank=True,related_name='liked')


    class Meta:
        ordering=['-created_on']

    def __str__(self):
        return self.title
    @property
    def num_likes(self):
        return self.liked.all().count()
LIKE_CHOICES=(
    ('Like','Like'),
    ('Unlike','Unlike'),
)
class Like(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    value=models.CharField(choices=LIKE_CHOICES,default='Like',max_length=10)

    def __str__(self):
        return str(self.post)


class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80,default='')
    body=models.TextField()
    created_on=models.DateTimeField(default=datetime.datetime.now())
    active=models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body,self.name)


