from django.db import models
from jalali_date import datetime2jalali, date2jalali
from django.core.validators import MaxLengthValidator
from accounts.models import User
from django.utils.text import slugify
from unidecode import unidecode
from django.shortcuts import reverse

# ----------------------- General Models  -----------------------
class General(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش')

    class Meta:
        abstract = True

    def get_created_at(self):
        return datetime2jalali(self.created_at).strftime('%H:%M - %Y/%m/%d')
    get_created_at.short_description = 'تاریخ ایجاد'

    def get_updated_at(self):
        return datetime2jalali(self.updated_at).strftime('%H:%M - %Y/%m/%d')
    get_updated_at.short_description = 'آخرین بروزرسانی'
# ----------------------- end General Models  -----------------------


class UserStatus(User):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='status', verbose_name='کاربر')
    online = models.BooleanField(default=False, verbose_name='وضعیت آنلاین بودن')

    def is_online(self):
        return self.online



class ChatRoom(General):
    name = models.CharField(max_length=100, verbose_name='نام گروه')
    slug = models.SlugField(max_length=225, unique=True, verbose_name='اسلاگ', blank=True, null=True)
    users = models.ManyToManyField(User, related_name='chat_rooms', verbose_name='کاربران')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            # Transliterate Persian characters to English
            slug_name = unidecode(self.name)
            self.slug = slugify(slug_name)
        return super(ChatRoom, self).save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse('chat:room', args=[str(self.slug)])


    class Meta:
        index_together = (('name', 'slug'), )
    

class Message(General):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, verbose_name='گروه')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='فرستنده پیام')
    message = models.TextField(verbose_name='متن پیام')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='زمان ارسال')
    seen_by = models.ManyToManyField(User, related_name='seen_messages', blank=True, verbose_name='بازدیدها')

    def __str__(self):
        return self.message
    