from django.db import models
from django.utils.safestring import mark_safe
from django.contrib.auth.models import AbstractUser
from django.db.models import Q
from jalali_date import datetime2jalali, date2jalali
from datetime import datetime
from .managers import UserManager
from .utils import generate_new_verification_code
from django.core.validators import MaxLengthValidator
import string
import random

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


class User(AbstractUser):
    GENDER_CHOICES = [
        (1, 'آقا'),
        (2, 'خانم'),
    ]
    
    first_name = models.CharField(verbose_name="نام", max_length=30, null=True, blank=False)
    last_name = models.CharField(verbose_name="نام خانوادگی", max_length=50, null=True, blank=False)
    date_joined = models.DateTimeField(verbose_name="تاریخ عضویت", null=True, blank=True, default=datetime.now)
    last_update = models.DateTimeField(verbose_name="آخرین بروزرسانی", auto_now=True, null=True)
    last_login = models.DateTimeField(verbose_name="آخرین ورود", null=True, blank=True)
    gender = models.PositiveSmallIntegerField(verbose_name="جنسیت", choices=GENDER_CHOICES, default=1)
    phone = models.CharField(verbose_name="تلفن همراه", null=True, max_length=11, unique=True)
    email = models.EmailField(verbose_name="ایمیل", null=True, blank=True)
    valid_phone = models.BooleanField(default=False, verbose_name="تایید تلفن همراه")    
    valid_email = models.BooleanField(default=False, verbose_name="تایید ایمیل")
    date_of_birth = models.DateField(verbose_name="تاریخ تولد", null=True, blank=True)

    
    USERNAME_FIELD = 'phone'
    objects = UserManager()

    class Meta:
        verbose_name_plural = '   کاربران'
        verbose_name = 'کاربر'

    def get_date_joined(self):
        if self.date_joined:
            return datetime2jalali(self.date_joined).strftime("%H:%M - %Y/%m/%d")
        return 'بدون تاریخ'
    get_date_joined.short_description = 'تاریخ و زمان عضویت'

    def get_date_joined__date(self):
        if self.date_joined:
            return datetime2jalali(self.date_joined).strftime("%Y/%m/%d")
        return 'بدون تاریخ'  
    get_date_joined__date.short_description = 'تاریخ عضویت'

    def get_last_update(self):
        if self.last_update:
            return datetime2jalali(self.last_update).strftime("%H:%M - %Y/%m/%d")
        return 'بدون تاریخ'
    get_last_update.short_description = 'آخرین بروزرسانی'

    def get_last_login(self):
        if self.last_login:
            return datetime2jalali(self.last_login).strftime("%H:%M - %Y/%m/%d")
        return "تاکنون وارد سایت نشده است."
    get_last_login.short_description = 'آخرین ورود'

    def get_gender(self):
        if self.gender == 1:
            return 'آقای'
        elif self.gender == 2:
            return 'خانم'
        else:
            return 'نامعتبر'

    def __str__(self):
        if self.get_full_name():
            return self.get_full_name()
        return self.username

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.__previous_phone = self.phone
            self.__previous_email = self.email

    def generate_random_code(self, length=6):
        """
        Generate a random code with a given length.
        """
        characters = string.ascii_letters + string.digits
        return ''.join(random.choices(characters, k=length))

    def save(self, *args, **kwargs):
        if not self.username:
            # Generate a unique username based on random code
            username = self.generate_random_code()
            self.username = username.lower()
        
        super().save(*args, **kwargs)


class VerificationCode(General):
    SUBJECT_CHOICES = [
        ("phone", "تلفن همراه"),
        ("email", "ایمیل"),
    ]
    STATUS_CHOICES =[
        (0, "نامعتبر"),
        (1, "معتبر"),
        (2, "اعمال شده"),
    ]
    subject = models.CharField(max_length=20, choices=SUBJECT_CHOICES, verbose_name="نوع کد تایید")
    code = models.CharField(max_length=10, blank=True, editable=False, unique=True,
           default=generate_new_verification_code, verbose_name="کد تایید")
    status = models.PositiveSmallIntegerField(default=1, choices=STATUS_CHOICES, verbose_name="وضعیت کد")
    attempts =  models.PositiveSmallIntegerField(default=0, verbose_name="تعداد تلاش")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")

    class Meta:
        verbose_name = 'کد تایید'
        verbose_name_plural = 'کدهای تایید'

    def __str__(self):
        return f"{self.subject} - {self.code}"
    
    @property
    def get_status(self):
        return dict(self.STATUS_CHOICES)[self.status]

    @property
    def get_subject(self):
        return dict(self.SUBJECT_CHOICES)[self.subject]