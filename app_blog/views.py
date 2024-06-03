from django.shortcuts import render , redirect
from django.urls import reverse , reverse_lazy 
from . import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from  . import forms
import os
import time
from dotenv import load_dotenv
load_dotenv()
import cloudinary
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

    following_accounts_objects = models.following_tracker.objects.filter(request_owner = request.user.username).filter(still = True ).all()
    for account in following_accounts_objects:
        print(account.request_receiver)
        following_accounts_usernames.append(account.request_receiver)
    
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
    print(f'generated_code: {generated_post_code}')
    if request.method == 'POST':
        print(request.POST['post_title'])
        print(request.POST['post_index'])

        post_title = request.POST['post_title']
        post_index = request.POST['post_index']
        form_image = forms.load_image_form(request.POST, request.FILES)
        forms.load_image_form()
        print(f"full_form_image: {form_image.data}")
        print(f"form_image_info2: {form_image.data.get("local_url")}")
        ##weirdly if i choose image for uploading it sets local_url as None so i am using this for verification
        if form_image.is_valid() and form_image.data.get("local_url") == None :

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
                cloudinary.uploader.upload(f"media/images/{request.user.username}/{request.user.username}_{load_image_item.added_at.timestamp()}.{load_image_item.local_url.name.split('.')[-1]}", public_id=f"{generated_post_code - 1}", folder = f'images/{request.user.username}' ,  unique_filename = True, overwrite=False)
                public_srcURL = f'https://res.cloudinary.com/dahnnnwts/image/upload/images/{request.user.username}/{generated_post_code  -1 }.{load_image_item.local_url.name.split('.')[-1]}'  #CloudinaryImage(f'{generated_post_code - 1}')
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
    follow_tracker = models.following_tracker.objects.filter(request_owner = request.user.username).filter(request_receiver = username).all()

    if follow_tracker:
        for item in follow_tracker:
            if item.still == False:
                item.still = True
                item.save()
            else:
                item.still = False
                item.save()
    
    else:
        models.following_tracker.objects.create(request_owner = request.user.username , request_receiver = username)

    return redirect(reverse('app_blog:home'))

def delete_post(request, gen_code): 
    
    if request.user.username == models.user_post.objects.get(generated_code = gen_code).who_pushed:
        try :
            filename = f"{request.user.username}_{models.load_image.objects.get(generated_code = gen_code).added_at.timestamp()}"
            print(filename)
            models.load_image.objects.get(generated_code = gen_code).delete()
            for file in os.listdir(path= f'media/images/{request.user.username}'):
                if file.startswith(filename):
                    os.remove(path=f'media/images/{request.user.username}/{file}')
                    print(f"{file} has been deleted.")

        except ObjectDoesNotExist:
            print("no load_image object for this post")
        models.user_post.objects.get(generated_code = gen_code).delete()
        
        
            #auto folder deleting will be here

        cloudinary.uploader.destroy(public_id= f'images/{request.user.username}/{gen_code}')

        return redirect(reverse('app_blog:home'))
      