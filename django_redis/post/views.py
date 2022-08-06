from django.shortcuts import render, redirect, HttpResponse
from .models import Post
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .froms import RegisterForm, LoginForm, BasketForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
# Create your views here.
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
CACHE_TTL = getattr(settings,'CACHE_TTL',DEFAULT_TIMEOUT)

import redis
r = redis.Redis(host='localhost', port=6379, db=0,charset="utf-8", decode_responses=True)


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(username=cd['username'], email=cd['email'],password=cd['password'])
            return redirect('post:login')
    else:
        form = RegisterForm()

    return render(request, 'post/register.html', {'form':form})



def logining(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)

                member = request.user.username 
                score = 1
                key = 'user_score'
                users = r.zrange(key, 0, -1)
                if member not in users:
                    r.zadd(key, {member :score})
                messages.success(request, 'your loging', 'success')
            return redirect('post:index')

    else:
        form = LoginForm()
    messages.success(request, 'your welcome', 'success')
    return render(request, 'post/login.html', {'form':form})


@login_required
@cache_page(CACHE_TTL)
def index(request):
    posts = Post.objects.all()

    context ={
        'posts':posts,
        }
    messages.success(request,'welcome.', 'success')   
    return render(request, 'post/index.html', context )


@login_required
def detail(request, pk):
    post = Post.objects.get(pk=pk)

    #usernames = [user.username for user in User.objects.filter(id__in=[int(id) for id in r.smembers(f'visit-post:{post.id}')])] --->one
    usernames = r.lrange(f'visit-post:{post.id}', 0, -1)
    member = request.user.username

    if member not in usernames:
        r.zincrby('user_score', 2, member)
        user_id = request.user.id
        r.lpush(f'visit-post:{post.id}', member) #r.sadd(f'visit-post:{post.id}', user_id) --->one
        usernames.append(member)

    context ={
        'post':post,
        'total_views': r.llen(f'visit-post:{post.id}'),#r.scard(f'visit-post:{post.id}'), # total_views = r.incrby(f'post:{po.id}'),--->one
        'onlin': usernames,
        'form':BasketForm(initial={'post_id':post.id})
    }
    messages.success(request,'your welcome.', success)
    return render(request, 'post/detail.html', context)



def visit_post_information(request):
    keys = r.keys('visit-post:*') #[key for key in r.scan_iter('visit-post:*')]
    information = []
    for key in keys:
        post_id = key.split(':')[-1] #for get id post
        post = Post.objects.get(id=post_id)

        total_key = r.llen(key)#[int(id) for id in r.smembers(key)] --->one
        users = r.lrange(key, 0, -1)#User.objects.filter(id__in=total_key) --->one
        information.append([post, int(post_id), users, total_key])
    

    context = {
        'informations':information,
    }
    return render(request, 'post/information.html', context)

@login_required
def system_score_information(request):
    all_users_score = r.zrange('user_score' ,0 ,-1 ,desc=True, withscores=True )
    user = request.user.username
    me_score = r.zscore('user_score', user)
    
    context = {
        'all_users_score':all_users_score,
        'me_score':me_score
    }

    n = [i for i in r.scan_iter('visit-post:*')]
    print(n)
    return render(request, 'post/score.html', context)


@login_required
def order(request):
    user_id = request.user.id

    ordering =[[i] for i in r.scan_iter(f'order:{user_id}:*')]
    my_orders = []
    price_order = 0
    for order in ordering:
        post_id = order[0].split(':')[-1]
        price = r.hget(f'order:{user_id}:{post_id}',"total_price")
        price_order = price_order + int(price)
        my_orders.append(r.hgetall(order[0]))
    
    context = {
        'my_orders':my_orders,
        'price_order':price_order
    }

    if request.method == 'POST':
        form = BasketForm(request.POST or None)
        if form.is_valid():
            number = str(form.cleaned_data.get('number'))
            post_id = str(form.cleaned_data.get('post_id'))
            my_key = f'order:{user_id}:{post_id}'
            key = r.exists(my_key)
            if key == 0:
                post = Post.objects.get(id=post_id)
                total_price = int(number) * post.price
                order = {"name":post.name,"price":post.price,"number":number,"total_price":total_price,"pk":post.id}
                my_orders.append(r.hmset(my_key, order))
                price_order += total_price
                messages.success(request, 'products added to basket', 'success')
            
            context = {
                'my_orders':my_orders,
                'price_order':price_order
            }
            return redirect('post:index')
        
        else:
            messages.warning(request, 'this product was exists', 'warning')
            return redirect('post:detail', post_id)
    
    return render(request, 'post/orders.html', context)


@login_required
def order_delete(request, pk):
    user_id = request.user.id
    key = r.exists(f'order:{user_id}:{pk}')
    if key == 1:
       r.delete(f'order:{user_id}:{pk}')
    return redirect('post:order')

@login_required
def orders_delete(request):
    user_id = request.user.id
    for order in r.scan_iter(f'order:{user_id}:*'):
        r.delete(order)
    return redirect('post:index') 


@login_required
def order_update(request):
    if request.method == 'POST':
        user_id = request.user.id  
        post_id = request.POST.get('post_id')
        number = request.POST.get('number')
        post = Post.objects.get(id=post_id)
        key = r.hexists(f'order:{user_id}:{post_id}',"number")
        if key==1:
            total_price = post.price * int(number)
            r.hset(f'order:{user_id}:{post_id}',"number",number)
            r.hset(f'order:{user_id}:{post_id}',"total_price",total_price)
            return redirect('post:order')
        else:
            messages.warning(request, 'permission denide', 'warning')
    else:
        return redirect('post:order')

