from django.shortcuts import render , redirect
from django.urls import reverse , reverse_lazy 
from . import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from  . import forms
import os
import time
from django.http import JsonResponse
from dotenv import load_dotenv
load_dotenv()
import cloudinary
from cloudinary import CloudinaryImage
import cloudinary.uploader
import cloudinary.api
config = cloudinary.config(secure=True)
#print("****1. Set up and configure the SDK:****\nCredentials: ", config.cloud_name, config.api_key, "\n")

@login_required(login_url='/login/')
def home(request):

    following_accounts_usernames = []
    home_page_posts_gcs = []
    home_page_posts = []
    suggest_usernames_from_model = []
    suggest_usernames_followed = []
    suggest_usernames_follow = []

    following_accounts_objects = models.following_tracker.objects.filter(who_requested = request.user.username).filter(still = True ).all()
    for account in following_accounts_objects:
        print(account.followed_who)
        following_accounts_usernames.append(account.followed_who)
    
    for username in following_accounts_usernames:
        for post in models.user_post.objects.order_by('-added_at').filter(who_pushed = username).all():
            home_page_posts_gcs.append(post.generated_code)
    
    for post_gc in home_page_posts_gcs:
        home_page_posts.append(models.image_and_specs.objects.get(generated_code = post_gc))
    
    
    sorted_home_page_posts = sorted(home_page_posts , key=lambda x: x.added_at , reverse=True)
    



    for item in models.suggests.objects.all():
        suggest_usernames_from_model.append(item.username)
    
    for suggest_username in User.objects.all():
        #print(suggest_username.username) 
        if suggest_username.username not in suggest_usernames_from_model:
                models.suggests.objects.create(username = suggest_username)

    for item in models.suggests.objects.all():
        
        if item.username in following_accounts_usernames:
            suggest_usernames_followed.append(item)
        else:
            suggest_usernames_follow.append(item)

    return render(request, 'app_blog/home.html' , context={ 'posts' : sorted_home_page_posts , 'suggests_follow' :  suggest_usernames_follow , 'suggests_unfollow' : suggest_usernames_followed })

@login_required(login_url='/login/')
def add(request):
    generated_post_code = models.generate_post_code()
    print(f'generated_code{generated_post_code}')
    if request.method == 'POST':
        print(request.POST['post_title'])
        print(request.POST['post_index'])

        post_title = request.POST['post_title']
        post_index = request.POST['post_index']
        

        form_image = forms.load_image_form(request.POST, request.FILES)
        forms.load_image_form()
        
        if form_image.is_valid():

            form_image.save()
            print('photo_valid!')
            models.user_post.objects.create(index = post_index , title = post_title , who_pushed = request.user.username , image_added = True , generated_code = generated_post_code - 1)        
            user_post_item = models.user_post.objects.get(generated_code = generated_post_code - 1)
            load_image_item = models.load_image.objects.get(generated_code = generated_post_code -1)
            print(user_post_item)
            print(load_image_item)
            models.image_and_specs.objects.create(specs = user_post_item , image = load_image_item , generated_code = generated_post_code  -1 )

            time.sleep(2)

            try:
                cloudinary.uploader.upload(f"media/images/{request.user.username}/{request.user.username}_{load_image_item.added_at.timestamp()}.{load_image_item.import_something.name.split('.')[-1]}", public_id=f"{generated_post_code - 1}", folder = f'images/{request.user.username}' ,  unique_filename = True, overwrite=False)
                public_srcURL = f'https://res.cloudinary.com/dahnnnwts/image/upload/images/{request.user.username}/{generated_post_code  -1 }.{load_image_item.import_something.name.split('.')[-1]}'  #CloudinaryImage(f'{generated_post_code - 1}')
                print(f'photo source : {public_srcURL}')
                load_image_item.uploaded_url = public_srcURL
                load_image_item.save()

            except FileNotFoundError:
                print('file not found error raised')

            return redirect(reverse('app_blog:home'))
        
        else:
            models.user_post.objects.create(index = post_index , title = post_title , who_pushed = request.user.username , image_added = False , generated_code = generated_post_code)
            user_post_item = models.user_post.objects.get(generated_code = generated_post_code)
            print(user_post_item)
            
            aio_model = models.image_and_specs.objects.create(specs = user_post_item , image = None , generated_code = generated_post_code)
            aio_model.save()
            return redirect(reverse('app_blog:home'))

    else:    
       
        form_image = forms.load_image_form()
        return render(request , 'app_blog/add.html', context= {'form_image' : form_image , 'code' : generated_post_code})
    
class user_signup(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = "registration/signup.html"
    
def redirect_to_home(request):
    return redirect(reverse('app_blog:home'))

def follow_unfollow(request , username):
    follow_tracker = models.following_tracker.objects.filter(who_requested = request.user.username).filter(followed_who = username).all()

    if follow_tracker:
        for item in follow_tracker:
            if item.still == False:
                item.still = True
                item.save()
            else:
                item.still = False
                item.save()
    
    else:
        models.following_tracker.objects.create(who_requested = request.user.username , followed_who = username)

    return redirect(reverse('app_blog:home'))

def delete_post(request, gen_code): 
    
    if request.user.username == models.user_post.objects.get(generated_code = gen_code).who_pushed:
        
        filename = f"{request.user.username}_{models.load_image.objects.get(generated_code = gen_code).added_at.timestamp()}"
        print(filename)

        models.load_image.objects.get(generated_code = gen_code).delete()
        models.user_post.objects.get(generated_code = gen_code).delete()
        
        for file in os.listdir(path= f'media/images/{request.user.username}'):
            if file.startswith(filename):
                os.remove(path=f'media/images/{request.user.username}/{file}')
                print(f"{file} has been deleted.")
            #auto folder deleting will be here

        cloudinary.uploader.destroy(public_id= f'images/{request.user.username}/{gen_code}')

        return redirect(reverse('app_blog:home'))
      
def posts_json(request):

    following_accounts_usernames = []
    home_page_posts_gcs = []
    home_page_posts = []

    following_accounts_objects = models.following_tracker.objects.filter(who_requested = request.user.username).filter(still = True ).all()
    for account in following_accounts_objects:
        print(account.followed_who)
        following_accounts_usernames.append(account.followed_who)
    
    for username in following_accounts_usernames:
        for post in models.user_post.objects.order_by('-added_at').filter(who_pushed = username).all():
            home_page_posts_gcs.append(post.generated_code)
    
    for post_gc in home_page_posts_gcs:
        home_page_posts.append(models.image_and_specs.objects.get(generated_code = post_gc))
    
    json_post_infos = {}

    sorted_home_page_posts = sorted(home_page_posts , key=lambda x: x.added_at , reverse=True)

    for json_post_item in sorted_home_page_posts:

        json_post_info = {
            'generated_code' : json_post_item.generated_code,
            'title' : json_post_item.specs.title,
            'index' : json_post_item.specs.index,
            'who_pushed' : json_post_item.specs.who_pushed, 
            'image_url' : json_post_item.image.uploaded_url,     
        }

    json_post_infos.update({f'{json_post_item.generated_code}' : json_post_info})
        
    return JsonResponse({'posts' : json_post_infos})