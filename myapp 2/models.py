from django.db import models
from django.utils import timezone

class User(models.Model):
    # 创建用户模型 int text date
    name = models.CharField("用户名", max_length=50, default='', null=False)
    password = models.CharField("密码", max_length=50, default='', null=False)
    role = models.CharField("角色", max_length=50, default='', null=False)
    bio = models.CharField("个人介绍", max_length=500, default='', null=True)
    signature = models.CharField("个性签名", max_length=50, default='', null=True)
    english_name = models.CharField("英文名", max_length=50, default='', null=True)
    phone = models.CharField("手机号码", max_length=50, default='', null=True)
    avatar = models.CharField("头像url", max_length=200, default='', null=True)
    skills = models.CharField("兴趣专业", max_length=50, default='', null=True)
    uid = models.CharField("编号", max_length=50, default='', null=True)
    status = models.CharField("状态", max_length=50, default='', null=True)
    email = models.EmailField("邮箱", max_length=100, unique=True, null=False)
    sex = models.CharField("性别", max_length=50, default='', null=True)
    personal_rating = models.CharField("信任分", max_length=50, default='', null=True)

# 用户日志类
class log(models.Model):
    name = models.CharField("用户名", max_length=50, default='', null=False)
    time = models.CharField("登陆时间", max_length=50, default='', null=False)


class Email(models.Model):
    recipient = models.CharField(max_length=200, verbose_name="收件人")
    subject = models.CharField(max_length=200, verbose_name="主题")
    body = models.TextField(verbose_name="正文")
    sent_time = models.DateTimeField(auto_now_add=True, verbose_name="发送时间")
    sender = models.CharField(max_length=200, verbose_name="发件人")

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = "邮件"
        verbose_name_plural = "邮件"



# 商品类别
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

# 二手商品创建
class SecondHandItem(models.Model):
    STATUS_CHOICES = (
        ('待售', '待售'),
        ('售出', '售出'),
    )
    AUDIT_CHOICES = (
        ('Pending', '等待'),
        ('Approved', '批准'),
        ('Rejected', '拒绝'),
    )
    DEAL_STATUS_CHOICES = (
        ('Not Dealt', '未成交'),
        ('Dealt', '已成交'),
    )
    GUEST_DEAL_STATUS_CHOICES = (
        ('Not Dealt', '未成交'),
        ('Dealt', '已成交'),
    )
    SHIPPING_STATUS_CHOICES = (
        ('Not Shipped', '未发货'),
        ('Shipped', '已发货'),
    )
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    on_sale_status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='待售')
    audit_status = models.CharField(max_length=255, choices=AUDIT_CHOICES, default='等待')
    seller_name = models.CharField(max_length=255, default='123')
    buyer_name = models.CharField(max_length=255, blank=True, null=True)
    # 商家是否认定成交
    deal_status = models.CharField(max_length=255, choices=DEAL_STATUS_CHOICES, default='未成交')
    # 买家是否认定成交
    guest_deal_status = models.CharField(max_length=255, choices=GUEST_DEAL_STATUS_CHOICES, default='未成交')
    shipping_address = models.TextField(blank=True, null=True)
    receiving_address = models.TextField(blank=True, null=True)
    buyer_rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 11)], null=True, blank=True)
    # 这是卖家给买家打分
    seller_rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 11)], null=True, blank=True)
    image = models.ImageField(upload_to='static/', blank=True, null=True)
    shipping_status = models.CharField(max_length=255, choices=SHIPPING_STATUS_CHOICES, default='未发货')

    def __str__(self):
        return self.name

# 收藏表
class UserFavorites(models.Model):
    user_name = models.CharField(max_length=255)  # 收藏者的用户名
    item = models.ForeignKey(SecondHandItem, on_delete=models.CASCADE)  # 关联的商品

    class Meta:
        unique_together = ('user_name', 'item')  # 确保每个用户只能收藏每个商品一次

    def __str__(self):
        return f"{self.user_name} - {self.item.name}"

# 我的浏览历史
from django.db import models
from datetime import datetime

class BrowsingHistory(models.Model):
    user_name = models.CharField(max_length=255)
    item = models.ForeignKey(SecondHandItem, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.user_name} viewed {self.item.name}"

