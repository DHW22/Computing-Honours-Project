from django.shortcuts import render,redirect
from .models import User,log
from datetime import date
from django.shortcuts import redirect
import calendar
from django.http import HttpResponse, HttpResponseRedirect
import time
from datetime import datetime


# 首页
def index(request):
    if request.method == 'GET':
        return render(request,'index.html',locals())

from django.db.models import Avg
# 登录#get post
def login(request):
    if request.method =='GET':
        return render(request, 'login.html', locals())
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        # orm 技术
        exists = User.objects.filter(name = username ,password = password).exists()
        if not exists:
            return render(request, 'login.html', locals())
        else:
            times = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            log.objects.create(name = username,time=times)
            p = User.objects.filter(name=username, password=password).values('role')[0]['role']
            if username== 'admin':
                # 将用户名写入cookie和session中
                request.session["info"] = {'name': username}
                return redirect('/myapp/index')
            else :
                # 登陆时，check
                # 查询buyer_name为'123'的商品的seller_rating的非0值，并计算均值
                buyer_items = SecondHandItem.objects.filter(buyer_name=username).exclude(seller_rating=0)
                a = buyer_items.aggregate(Avg('seller_rating'))['seller_rating__avg']

                # 查询seller_name为'123'的商品的buyer_rating的非0值，并计算均值
                seller_items = SecondHandItem.objects.filter(seller_name=username).exclude(buyer_rating=0)
                b = seller_items.aggregate(Avg('buyer_rating'))['buyer_rating__avg']
                if a!=None and b!=None:
                    c = (a+b)/2
                    # 查找用户名为'123'的用户
                    user = User.objects.get(name=username)

                    # 更新personal_rating的值为456
                    user.personal_rating = c
                    print(c)
                    print('存储OK')
                    user.save()
                # 将用户名写入cookie和session中
                request.session["info"] = {'name': username}
                return redirect('/myapp/available_items')

# 退出登录
def log_out(request):
    if request.method =='GET':
        return redirect('/myapp/login')
# 中间件
# 注册
def regist(request):
    if request.method == 'GET':
        return render(request, 'regist.html', locals())
    else:
        a = request.POST['a']  # 用户名
        b = request.POST['b']  # 密码
        c = 'guest'  # 角色
        email = request.POST['email']  # 邮箱

        exists = User.objects.filter(name=a).exists()
        if exists:
            return HttpResponse('该用户名已被注册')

        # 创建新用户并保存邮箱
        User.objects.create(name=a, password=b, role=c, email=email)
        return render(request, 'login.html', locals())


# 登录日志
def login_log(request):
    if request.method =='GET':
        info = log.objects.all()
        return render(request,'login_log.html',locals())

# 用户管理
def user_info(request):
    if request.method=='GET':
        info = User.objects.all()
        return render(request, 'user_info.html', locals())

# 用户删除
def user_delete(request,username,password):
    if request.method=='GET':
        a = username
        b = password
        p = User.objects.filter(name=a,password=b)
        p.delete()
        # 使用redirect 可以保证url不会错误
        return redirect('/myapp/login')

# 用户修改
def user_alter(request,username,password):
    a = username
    b = password
    if request.method=='GET':
        info  = User.objects.filter(name=a,password=b)
        return render(request,'user_alter.html',locals())
    elif request.method=='POST':
        a = a
        b = b
        c = request.POST['aa']
        d = request.POST['bb']
        User.objects.filter(name=a, password=b).update(name=c, password=d)
        return redirect('/myapp/login')

# 员工创建信息 guest_profile_edit
def guest_profile_edit(request):
    if request.method=='GET':
        user_name = request.session["info"]['name']
        print('用户信息',user_name)
        user = User.objects.get(name=user_name)
        return render(request, 'guest_profile_edit.html', locals())

# 员工完善信息
def guest_profile_edit_upload(request):
    if request.method == 'POST':
        bio = request.POST['bio']
        signature = request.POST['signature']
        english_name = request.POST['english_name']
        email = request.POST['email']
        sex = request.POST['sex']
        status = request.POST['status']
        uid = request.POST['uid']

        phone = request.POST['phone']
        # avatar = request.FILES.get('avatar', None)
        # 图片路径的拼接
        # file_path = 'C:/Users/HUAWEI/school_pre/static/img/'+avatar.name
        # print(file_path)
        # # 图片下载到本地
        # f = open(file_path, mode='wb')
        # for chunk in avatar.chunks():
        #     f.write(chunk)
        # f.close()
        skills = request.POST['skills']
        user_name = request.session["info"]['name']
        print('用户信息',user_name)
        user_profile = User.objects.get(name=user_name)
        user_profile.bio = bio
        user_profile.signature = signature
        user_profile.english_name = english_name
        user_profile.email = email
        user_profile.sex = sex
        user_profile.status = status
        user_profile.uid = uid
        user_profile.phone = phone
        # if avatar:
        #     user_profile.avatar = file_path
        user_profile.skills = skills
        user_profile.save()
    return render(request, 'guest_index.html',locals())

# 员工首页
def guest_index(request):
    if request.method == 'GET':
        return render(request,'guest_index.html',locals())

# 员工信息展示
def guest_profile_display(request):
    if request.method == 'GET':
        user_name = request.session["info"]['name']
        user = User.objects.get(name=user_name)
        return render(request,'guest_profile_display.html',locals())

# 测试页面
def test(request):
    if request.method == 'GET':
        return render(request,'test.html',locals())


from django.shortcuts import render, redirect
from .models import Email
from django.utils import timezone

def email_editor(request):
    if request.method == 'POST':
        recipient = request.POST['recipient']
        subject = request.POST['subject']
        body = request.POST['body']
        sent_time = timezone.now()
        user_name = request.session["info"]['name']
        email = Email(recipient=recipient, subject=subject, body=body, sent_time=sent_time,sender = user_name)
        email.save()

        return HttpResponse('发送成功')
    users = User.objects.all()
    return render(request, 'email_editor.html',locals())

# 邮件删除
def email_manage(request,id):
    if request.method == 'GET':
        p = Email.objects.filter(id = id).first()
        p.delete()
        return HttpResponse('删除成功')

# 邮件展示
def email_presentation(request):
    if request.method == 'GET':
        info = Email.objects.all()

        return render(request, 'email_presentation.html',locals())

def email_single_presentation(request):
    emails = Email.objects.all()
    subjects = Email.objects.values_list('subject', flat=True).distinct()
    context = {'info': emails, 'subjects': subjects}
    return render(request, 'email_single_presentation.html', context)

# 找回密码
def reset_password(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']

        user = User.objects.filter(name=username, email=email).first()
        if user:
            # 如果用户名和邮箱匹配，重定向到密码重置页面
            print(user.id)
            url = '/myapp/change_password'+'/'+str(user.id)
            return redirect(url)
        else:
            # 如果不匹配，返回错误消息
            error_message = "用户名或邮箱不正确"
            return render(request, 'reset_password.html', {'error_message': error_message})
    return render(request, 'reset_password.html')

# 创建密码重置
def change_password(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        new_password = request.POST['new_password']
        user.password = new_password
        user.save()
        return redirect('/myapp/login')  # 重定向到登录页面
    return render(request, 'change_password.html', {'user': user})

# 下载经纬度
# import requests, re, pandas as pd, matplotlib.pyplot as mp
# url = 'https://blog.csdn.net/Yellow_python/article/details/88823956'
# header = {'User-Agent': 'Opera/8.0 (Windows NT 5.1; U; en)'}
# r = requests.get(url, headers=header)
# contain = re.findall('<pre><code>([\s\S]+?)</code></pre>', r.text)[0].strip()
# df = pd.DataFrame([i.split(',') for i in contain.split('\n')],
#                   columns=['province', 'city', 'longitude', 'latitude'])
# df['longitude'] = pd.to_numeric(df['longitude'])
# df['latitude'] = pd.to_numeric(df['latitude'])
# mp.scatter(df['longitude'], df['latitude'], alpha=0.2)
# mp.show()
# df.to_csv('中国省市经纬度.csv', index=None)

from django.shortcuts import render, redirect
import csv

# 部署时 需要运行下面两行代码
# import_city_coordinates()
# print('ok')

# 用户报名
from django.shortcuts import render, redirect, get_object_or_404


# 商品类别管理啊
from django.shortcuts import render, redirect
from .models import Category
from .forms import CategoryForm

def manage_categories(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/myapp/manage_categories')
    else:
        form = CategoryForm()
    return render(request, 'manage_categories.html', {'form': form, 'categories': categories})
#管理员删除类别
def delete_category(request, category_id):
    category = Category.objects.get(pk=category_id)
    category.delete()
    return redirect('/myapp/manage_categories')

# 普通用户二手商品上传
from django.shortcuts import render, redirect
from .models import SecondHandItem, Category
from .forms import SecondHandItemForm,ShippingAddressForm
def upload_item(request):
    if request.method == 'POST':
        # 在提交的数据中为on_sale_status设置一个默认值
        post_data = request.POST.copy()
        post_data['on_sale_status'] = '待售'

        form = SecondHandItemForm(post_data, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            user_name = request.session["info"]['name']
            item.seller_name = user_name
            item.on_sale_status = '待售'  # 明确设置为 '待售'
            item.save()
            print('上传成功')
            return redirect('/myapp/item_list')
        else:
            print('表单验证失败')
            print(form.errors)  # 打印表单验证的错误信息
    else:
        form = SecondHandItemForm()

    return render(request, 'upload_item.html', {'form': form})

# 展示二手商品
def item_list(request):
    show_alert = False  # 设置为True以显示警告
    user_name = request.session["info"]['name']
    items = SecondHandItem.objects.filter(seller_name=user_name)
    categories = Category.objects.all()  # 获取所有的类别
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        item = SecondHandItem.objects.get(id=item_id)
        form = SecondHandItemForm(request.POST, instance=item)  # 使用 SecondHandItemForm 来处理修改
        if form.is_valid():
            print('数据有效')
            form.save()
            return render(request, 'item_list.html', {'items': items, 'categories': categories})
        print('数据无效')
        print(form.errors)  # 打印表单验证的错误信息
        show_alert = True  # 设置为True以显示警告

    return render(request, 'item_list.html', {'items': items, 'categories': categories, 'show_alert': show_alert})

# 删除该商品
def delete_item(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        item = SecondHandItem.objects.get(id=item_id)
        if item.on_sale_status == "待售":
            item.delete()
    return redirect('/myapp/item_list')


# 管理员管理商品的状态
def admin_review(request):
    items = SecondHandItem.objects.filter(audit_status='等待')
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        action = request.POST.get('action')
        item = SecondHandItem.objects.get(id=item_id)
        if action == 'approve':
            item.audit_status = '批准'
        elif action == 'reject':
            item.audit_status = '拒绝'
        item.save()
        return redirect('/myapp/admin_review')
    return render(request, 'admin_review.html', {'items': items})

# 删除所有的二手商品
def delete_second_items_all(request):
    if request.method == 'GET':
        SecondHandItem.objects.all().delete()
        UserFavorites.objects.all().delete()
        BrowsingHistory.objects.all().delete()
        return HttpResponse('二手商品全部删除')

# 展示待售商品
from django.core.paginator import Paginator
from .models import SecondHandItem, Category
from django.db.models import Avg
def available_items(request):
    user_name = request.session["info"]['name']
    # 获取所有的种类
    categories = Category.objects.all()

    # 获取用户选择的种类
    selected_category = request.GET.get('category')
    if selected_category:
        # items = SecondHandItem.objects.filter(category__id=selected_category, on_sale_status='待售', audit_status='批准').exclude(seller_name=user_name)
        items = SecondHandItem.objects.filter(category__id=selected_category, on_sale_status='待售', audit_status='批准')
    else:
        # items = SecondHandItem.objects.filter(on_sale_status='待售', audit_status='批准').exclude(seller_name=user_name)
        items = SecondHandItem.objects.filter(on_sale_status='待售', audit_status='批准')

    # 根据价格排序
    order = request.GET.get('order')
    if order == 'asc':
        items = items.order_by('current_price')
    elif order == 'desc':
        items = items.order_by('-current_price')

    # 获取用户信息和提交的数据
    if request.method == 'POST':
        user_name = request.session["info"]['name']
        item_id = request.POST.get('item_id')
        item = SecondHandItem.objects.get(id=item_id)
        item.receiving_address = request.POST.get('receiving_address')
        item.buyer_name = user_name
        item.on_sale_status = '售出'
        item.save()

    # 实现分页
    paginator = Paginator(items, 10)
    page = request.GET.get('page')
    items_on_page = paginator.get_page(page)
    # 为每个商品计算其卖家的平均评分
    for item in items:
        item.seller_avg_rating = SecondHandItem.objects.filter(seller_name=item.seller_name).exclude(seller_rating__isnull=True).aggregate(Avg('seller_rating'))['seller_rating__avg']

    return render(request, 'available_items.html', {
        'items': items_on_page,
        'categories': categories,
        'selected_category': selected_category,
        'order': order
    })


# 待发货
def filtered_items(request):
    user_name = request.session["info"]['name']
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        rating = request.POST.get('seller_rating')
        item = SecondHandItem.objects.get(id=item_id)
        item.seller_rating = rating
        item.deal_status = '已成交'
        item.save()

    items = SecondHandItem.objects.filter(
        on_sale_status='售出',
        seller_name = user_name,
        deal_status='已成交',
        audit_status='批准',
    )
    return render(request, 'filtered_items.html', {'items': items})

# 展示我的订单
def buyer_view(request):
    user_name = request.session["info"]['name']
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        rating = request.POST.get('seller_rating')
        item = SecondHandItem.objects.get(id=item_id)
        item.buyer_rating = rating
        item.save()
        print('保存成功')
    items = SecondHandItem.objects.filter(
        buyer_name = user_name,
        deal_status='已成交',

    )
    return render(request, 'buyer_view.html', {'items': items})

# 展示商品详情
def item_detail(request, item_id):
    item = SecondHandItem.objects.get(id=item_id)
    user_name = request.session["info"]['name']

    # Save to browsing history
    history = BrowsingHistory(user_name=user_name, item=item)
    history.save()
    return render(request, 'item_detail.html', {'item': item})

# 商品收藏
from .models import UserFavorites,BrowsingHistory

def add_to_favorites(request):
    if request.method == 'POST':
        user_name = request.session["info"]['name']
        item_id = request.POST.get('item_id')
        item = SecondHandItem.objects.get(id=item_id)

        # 检查是否已经收藏
        existing_favorite = UserFavorites.objects.filter(user_name=user_name, item=item)
        if not existing_favorite:
            favorite = UserFavorites(user_name=user_name, item=item)
            favorite.save()

    return redirect('/myapp/available_items')  # 重定向回商品列表页面

# 展示我的收藏
def my_favorites(request):
    user_name = request.session["info"]['name']
    favorites = UserFavorites.objects.filter(user_name=user_name)
    return render(request, 'my_favorites.html', {'favorites': favorites})

# 展示我的历史记录
def browsing_history(request):
    user_name = request.session["info"]['name']
    history_items = BrowsingHistory.objects.filter(user_name=user_name).order_by('-viewed_at')
    return render(request, 'browsing_history.html', {'history_items': history_items})

# 推荐商品
from django.db.models import Count
from django.db import models

# def recommend_items_collaborative_filtering(request):
#     user_name = request.session["info"]['name']
#     items = SecondHandItem.objects.filter(on_sale_status='待售').exclude(seller_name=user_name)
#
#     scores = {}
#
#     # 获取用户浏览过的商品
#     browsed_items = BrowsingHistory.objects.filter(user_name=user_name).values_list('item', flat=True)
#
#     # 如果用户没有浏览历史，返回评分最高的商品
#     if not browsed_items:
#         recommended_items = items.order_by('-seller_rating')[:3]
#         return render(request, 'recommend_items_collaborative_filtering.html', {'items': recommended_items})
#
#     # 基于用户的协同过滤
#     similar_users = find_similar_users(user_name)
#     for user in similar_users:
#         for item in SecondHandItem.objects.filter(buyer_name=user):
#             scores[item.id] = scores.get(item.id, 0) + 1
#
#     # 基于物品的协同过滤
#     for browsed_item in browsed_items:
#         similar_items = find_similar_items(browsed_item)
#         for item in similar_items:
#             scores[item.id] = scores.get(item.id, 0) + 1
#
#     # 根据分数排序商品
#     recommended_items = sorted(items, key=lambda x: scores.get(x.id, 0), reverse=True)[:3]  # 推荐前3个商品
#
#     return render(request, 'recommend_items_collaborative_filtering.html', {'items': recommended_items})

from django.db.models import Q

def recommend_items_collaborative_filtering(request):
    user_name = request.session["info"]['name']
    recommended_items = []

    # 获取满足条件的商品
    items = SecondHandItem.objects.filter(
        ~Q(seller_rating__in=[str(i) for i in range(1, 11)]),  # seller_rating 不是数字
        ~Q(buyer_rating__in=[str(i) for i in range(1, 11)]),  # buyer_rating 不是数字
        audit_status='批准',
    ).exclude(seller_name=user_name)

    # 获取用户的personal_rating
    user = User.objects.get(name=user_name)
    personal_rating = user.personal_rating

    # 如果用户的personal_rating很高，我们可以考虑推荐更多的商品
    if float(personal_rating) > 8:

        recommended_items = items[:10]  # 推荐前10个商品
    elif float(personal_rating) > 6:
        recommended_items = items[:5]  # 推荐前5个商品

    # 考虑用户的浏览历史和收藏数据
    browsed_items = BrowsingHistory.objects.filter(user_name=user_name).values_list('item', flat=True)
    favorited_items = UserFavorites.objects.filter(user_name=user_name).values_list('item', flat=True)

    # 如果用户没有浏览和收藏数据，就什么都不推荐
    if not browsed_items and not favorited_items:
        return []

    # 否则，可以考虑将用户浏览过和收藏过的商品加入推荐列表
    for item in browsed_items:
        if item not in recommended_items:
            recommended_items = list(recommended_items)
            recommended_items.append(item)

    for item in favorited_items:
        if item not in recommended_items:
            recommended_items = list(recommended_items)
            recommended_items.append(item)

    return render(request, 'recommend_items_collaborative_filtering.html', {'items': recommended_items})

def find_similar_users(target_user):
    target_user_browsed_items = set(BrowsingHistory.objects.filter(user_name=target_user).values_list('item', flat=True))
    users = BrowsingHistory.objects.values('user_name').annotate(shared_items=Count('item', filter=models.Q(item__in=target_user_browsed_items))).order_by('-shared_items')
    similar_users = [user['user_name'] for user in users if user['shared_items'] > 0]
    return similar_users

def find_similar_items(target_item_id):
    target_item = SecondHandItem.objects.get(id=target_item_id)
    similar_items = SecondHandItem.objects.filter(category=target_item.category).exclude(id=target_item_id)
    return similar_items

# 普通游客界面
from django.core.paginator import Paginator
from .models import SecondHandItem, Category

def visitor_index(request):
    # 获取所有的种类
    categories = Category.objects.all()

    # 获取用户选择的种类
    selected_category = request.GET.get('category')
    if selected_category:
        items = SecondHandItem.objects.filter(category__id=selected_category, on_sale_status='待售', audit_status='批准')
    else:
        items = SecondHandItem.objects.filter(on_sale_status='待售', audit_status='批准')

    # 根据价格排序
    order = request.GET.get('order')
    if order == 'asc':
        items = items.order_by('current_price')
    elif order == 'desc':
        items = items.order_by('-current_price')

    # 实现分页
    paginator = Paginator(items, 10)
    page = request.GET.get('page')
    items_on_page = paginator.get_page(page)

    return render(request, 'visitor_index.html', {
        'items': items_on_page,
        'categories': categories,
        'selected_category': selected_category,
        'order': order
    })

# 购物车
def my_cart(request):
    # 获取当前用户的名字
    user_name = request.session["info"]['name']
    current_user_name = user_name

    # 查询购物车中的物品
    cart_items = SecondHandItem.objects.filter(
        on_sale_status='售出',
        deal_status='未成交',
        shipping_status='未发货',
        audit_status='批准',
        guest_deal_status = '未成交',
        buyer_name=current_user_name
    )

    context = {
        'cart_items': cart_items
    }

    return render(request, 'my_cart.html', context)

from django.shortcuts import render, redirect
from .models import SecondHandItem

def remove_from_cart(request, item_id):
    item = SecondHandItem.objects.get(id=item_id)
    item.on_sale_status = '待售'
    item.buyer_name = None
    item.receiving_address = None
    item.save()
    return redirect('/myapp/my_cart')

def checkout_item(request, item_id):
    item = SecondHandItem.objects.get(id=item_id)
    item.deal_status = '已成交'
    item.save()
    return redirect('/myapp/my_cart')


from django.shortcuts import render
from .models import SecondHandItem
def earned_money_view(request):
    # 获取满足条件的SecondHandItem对象
    user_name = request.session["info"]['name']
    score = User.objects.filter(
        name = user_name).first()

    items = SecondHandItem.objects.filter(
        seller_name = user_name,
        deal_status='已成交',
        # guest_deal_status='未成交',
        buyer_rating__isnull=False,
        seller_rating__isnull=False
    )
    print(items)
    # 计算总金额
    total_earned = sum(item.current_price for item in items)

    context = {
        'items': items,
        'total_earned': total_earned,
        'score': score,
    }

    return render(request, 'earned_money_view.html', context)


from django.shortcuts import render, redirect, get_object_or_404
from .models import User

def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.name = request.POST.get('name')
        user.email = request.POST.get('email')
        user.role = request.POST.get('role')
        user.bio = request.POST.get('bio')
        user.signature = request.POST.get('signature')
        user.english_name = request.POST.get('english_name')
        user.phone = request.POST.get('phone')
        user.avatar = request.POST.get('avatar')
        user.skills = request.POST.get('skills')
        user.uid = request.POST.get('uid')
        user.status = request.POST.get('status')
        user.sex = request.POST.get('sex')
        user.save()
        return redirect('/myapp/user_list')  # 一个名为'user_list'的URL，用于显示用户列表
    return render(request, 'edit_user.html', {'user': user})


def user_list(request):
    # 获取除了名为'123'的所有用户
    users = User.objects.exclude(name='admin')
    return render(request, 'user_list.html', {'users': users})

def delete_user(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        user.delete()
        return redirect('/myapp/user_list')
    except User.DoesNotExist:
        return HttpResponse('用户不存在', status=404)
