from django.shortcuts import render, redirect
from .models import Profile, Group, Post, Comment
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# Create your views here.


def home(request):
    return render(request, 'socialmedia/home.html', {})


@login_required(login_url='login')
def tutorial(request):
    return render(request, 'socialmedia/tutorial.html', {})


@login_required(login_url='login')
def comingsoon(request):
    return render(request, 'socialmedia/comingsoon.html', {})


@login_required(login_url='login')
def feed(request):
    try:
        posts = Post.objects.all().order_by('-created')

    except Exception as err:
        print(err)
        getpage = 1
        posts = []

    getpage = request.GET.get('p')
    if getpage == None:
        getpage = 1

    p = Paginator(posts, 5)
    page = p.page(getpage)

    return render(request, 'socialmedia/feed.html', {"posts": posts, "posts": page.object_list, "p": p})


@login_required(login_url='login')
def friends_feed(request):
    posts = Post.objects.all().order_by('-created')
    profile = Profile.objects.get(user=request.user)
    friends = profile.friends.all()

    friendsposts = []
    for post in posts:
        if post.user == profile:
            friendsposts.append(post)
        else:
            for friend in friends:
                if post.user.user == friend:
                    friendsposts.append(post)

    getpage = request.GET.get('p')
    if getpage == None:
        getpage = 1
    p = Paginator(friendsposts, 5)
    page = p.page(getpage)
    return render(request, 'socialmedia/friendsposts.html', {"friendsposts": friendsposts, "friendsposts": page.object_list, "p": p})


@login_required(login_url='login')
def post_spesific(request, id):
    postSpesific = Post.objects.get(id=id)
    isLike = False
    for like in postSpesific.likes.all():
        if request.user == like.user:
            isLike = True
    return render(request, 'socialmedia/post.html', {"postSpesific": postSpesific, "isLike": isLike})


@login_required(login_url='login')
def new_post(request, username):
    profileUsername = User.objects.get(username=username)
    profile = Profile.objects.get(user=profileUsername)
    if profile.user == request.user:
        if request.method == 'POST':
            Post.objects.create(
                user=profile,
                body=request.POST['body'],
                imageUrl=request.POST['imageUrl']
            )
            return redirect('friendsposts')
    return render(request, 'socialmedia/newpost.html', {"profile": profile})


@login_required(login_url='login')
def addComment(request, id):
    postSpesific = Post.objects.get(id=id)
    if request.method == 'POST':
        Comment.objects.create(
            user=request.user,
            post=postSpesific,
            body=request.POST['body']
        )
        return redirect('post_spesific', postSpesific.id)
    return render(request, 'socialmedia/addcomment.html', {"postspesific": postSpesific})


@login_required(login_url='login')
def addRemoveLike(request, id):
    try:
        postSpesific = Post.objects.get(id=id)
        profile = Profile.objects.get(user=request.user)
        isExist = postSpesific.likes.filter(id=profile.id)
        print((isExist))
        if isExist.exists():
            postSpesific.likes.remove(profile)
        else:
            postSpesific.likes.add(profile)
        postSpesific.save()
    except Exception as e:
        print(e)
    return redirect('friendsposts')


@login_required(login_url='login')
def edit_post(request, id):
    post = Post.objects.get(id=id)
    if request.method == 'POST':
        post.body = request.POST['body']
        post.imageUrl = request.POST['imageUrl']
        post.save()
        return redirect('friendsposts')
    return render(request, 'socialmedia/editpost.html', {"post": post})


@login_required(login_url='login')
def edit_comment(request, id):
    comment = Comment.objects.get(id=id)
    if request.method == 'POST':
        comment.body = request.POST['body']
        comment.save()
        return redirect('friendsposts')
    return render(request, 'socialmedia/editcomment.html', {"comment": comment})


@login_required(login_url='login')
def remove_post(request, id):
    post = Post.objects.get(id=id)
    if request.method == 'POST':
        post.delete()
        return redirect('friendsposts')
    return render(request, 'socialmedia/removepost.html', {"post": post})


@login_required(login_url='login')
def remove_Comment(request, id):
    comment = Comment.objects.get(id=id)
    if request.method == 'POST':
        comment.delete()
        return redirect('friendsposts')
    return render(request, 'socialmedia/removecomment.html', {"comment": comment})


# צריך לסדר את ההצגה של כפתור ההוספת חבר הורדת חבר
@login_required(login_url='login')
def profile_username(request, username):
    profileUsername = User.objects.get(username=username)
    profile = Profile.objects.get(user=profileUsername)
    posts = Post.objects.filter(user=profile).order_by('-created')

    getpage = request.GET.get('p')
    if getpage == None:
        getpage = 1

    isFriend = False
    for friend in profile.friends.all():
        if friend == request.user:
            isFriend = True

    p = Paginator(posts, 4)
    page = p.page(getpage)
    return render(request, 'socialmedia/profile.html', {"profile": profile, "posts": posts, "posts": page.object_list, "p": p, "isFriend": isFriend})


@login_required(login_url='login')
def edit_profile(request, username):
    profileUsername = User.objects.get(username=username)
    editProfile = Profile.objects.get(user=profileUsername)
    if editProfile.user == request.user:
        if request.method == 'POST':
            editProfile.first_name = request.POST['first_name']
            editProfile.last_name = request.POST['last_name']
            editProfile.city = request.POST['city']
            editProfile.imageUrl = request.POST['imageUrl']
            editProfile.coverUrl = request.POST['coverUrl']
            editProfile.relationship = request.POST['relationship']
            editProfile.save()
            return redirect('profile_username', username)
        return render(request, 'socialmedia/editprofile.html', {"editProfile": editProfile})
    else:
        return redirect('home')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            return render(request, 'socialmedia/login.html', {"error": "Username Not Found"})

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('feed')
        else:
            return render(request, 'socialmedia/login.html', {"error": "Username or Password incorrect"})

    return render(request, 'socialmedia/login.html', {})


def signup_user(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if request.POST['first_name'] != '' and request.POST['last_name'] != '':
            if form.is_valid():
                form.save()
                username = request.POST['username']
                password = request.POST['password1']
                user = authenticate(username=username, password=password)
                Profile.objects.create(
                    user=user,
                    first_name=request.POST['first_name'],
                    last_name=request.POST['last_name'],
                    city=request.POST['city'],
                    dob=request.POST['dob'],
                    imageUrl=request.POST['imageUrl'],
                    coverUrl=request.POST['coverUrl'],
                    relationship=request.POST['relationship']
                )
                login(request, user)
                return redirect('feed')
            else:
                return render(request, 'socialmedia/signup.html', {"error": "Error creating the user , All fields required"})
    return render(request, 'socialmedia/signup.html', {"form": form})


@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('home')


@login_required(login_url='login')
def nav_following(request):
    profile = Profile.objects.get(user=request.user)
    users = profile.friends.all()

    getpage = request.GET.get('p')
    if getpage == None:
        getpage = 1

    profiles = []

    for user in users:
        x = Profile.objects.get(user=user)
        print(len(x.post_set.all()))
        profiles.append(x)

    p = Paginator(profiles, 3)
    page = p.page(getpage)

    return render(request, 'socialmedia/following.html', {"friends": profiles, "friends": page.object_list, "p": p})


# צריך להגיע לשליפה של כל היוזרים שיש בדאטהבייס שהם לא חברים של היוזר המחובר ולהציג אותם
@login_required(login_url='login')
def new_followers(request):
    profile = Profile.objects.get(user=request.user)
    friends = profile.friends.all()
    users = User.objects.all()
    profiles = []

    getpage = request.GET.get('p')
    if getpage == None:
        getpage = 1

    for user in users:
        if user not in friends:
            if user != profile.user:
                profile1 = Profile.objects.get(user=user)
                profiles.append(profile1)

    p = Paginator(profiles, 2)
    page = p.page(getpage)

    return render(request, 'socialmedia/newfollowers.html', {"friends": profiles, "friends": page.object_list, "p": p})


@login_required(login_url='login')
def addFriend(request, username):
    friend = User.objects.get(username=username)
    profile = Profile.objects.get(user=friend)
    currentUserProfile = Profile.objects.get(user=request.user)
    if request.user in profile.friends.all():
        profile.friends.remove(request.user)
        currentUserProfile.friends.remove(friend)
    else:
        profile.friends.add(request.user)
        currentUserProfile.friends.add(friend)
    return redirect('profile_username', username)


@login_required(login_url='login')
def remove_profile(request, username):
    profile1 = User.objects.get(username=username)
    profile = Profile.objects.get(user=profile1)
    if profile.user == request.user:
        if request.method == 'POST':
            profile.user.delete()
            profile.delete()
            logout(request)
            return redirect('login')
        return render(request, 'socialmedia/removeprofile.html', {"profile": profile})
    else:
        return redirect('feed')


@login_required(login_url='login')
def search(request):

    q = request.GET.get('q') if request.GET.get('q') != None else ''

    profiles = Profile.objects.filter(
        Q(first_name__icontains=q) |
        Q(last_name__icontains=q)
    )

    posts = Post.objects.filter(
        Q(body__icontains=q)
    )

    comments = Comment.objects.filter(
        Q(body__icontains=q)
    )

    return render(request, 'socialmedia/search.html', {"profiles": profiles, "posts": posts, "comments": comments})
