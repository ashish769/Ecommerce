from django.shortcuts import render,redirect,get_object_or_404
#for login
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import messages 
from .models import *
from .forms import ProfileUpdateForm,ReviewForm
from django.contrib.auth.decorators import login_required

#to show the selective item in a single page
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    product=Product.objects.all()
    cate=Category.objects.all()
    cateid=request.GET.get('category')

    if cateid:
        product=Product.objects.filter(subcategory=cateid)
    else:
        product=Product.objects.all()

    paginator=Paginator(product,2)#Paginator object that divides the product queryset into pages, with 2 products per page.
    num_page=request.GET.get('page')#retrieves the page number from the URL's query parameters and stores it in the variable num_page.
    data=paginator.get_page(num_page)# gets the products for the current page number and stores them in the variable data.
    total=data.paginator.num_pages#returns the total number of pages available in the paginator
    

    context={
        'product':product,
        'cate':cate,
        'data':data,
        'num':[i+1 for i in range(total)]
    }
    return render(request,'main/index.html',context)
def blog_single(request):
    return render(request,'main/blog-single.html')
def blog(request):
    return render(request,'main/blog.html')
def cart(request):
    return render(request,'main/cart.html')
def checkout(request):
    return render(request,'main/checkout.html')
def contact_us(request):
    return render(request,'main/contact-us.html')

def log_in(request):
    if request.method == 'POST':
        var=request.POST
        print(var)
        if 'login' in request.POST:
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)  
                messages.success(request,'login sucessfully!welcome to E-shop')
                return redirect('login')
            else:
                messages.error(request, 'Invalid credentials. Please try again with the correct information.')
                return redirect('login')
        elif 'signup' in request.POST:
            name = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            
            if User.objects.filter(username=email).exists():
                messages.error(request, 'Email already exists')
            elif len(password)<8:
                messages.error(request,'passsword should contain at least 8 character')
            else:
                User.objects.create_user(username=email, first_name=name, password=password)
                messages.success(request, 'Signup successfully! Please login now')
                return redirect('login')
            

    return render(request, 'main/login.html')

def product_details(request,id):
    product=get_object_or_404(Product,id=id)
    products=Product.objects.filter(category=product.category).exclude(id=id)
    cmt_all=request.GET.get('cmt_all')
    if cmt_all:
        reviews=product.reviews.all()
    else:
        reviews=product.reviews.all()[:3]
    form=ReviewForm()
    if request.method=='POST':
        form=ReviewForm(request.POST)
        if form.is_valid:
            review=form.save(commit=False)
            review.product=product
            review.user=request.user
            review.save()
            return redirect('product-details', id=id)
    

    context={
        'product':product,
        'products':products,
        'form':form,
        'reviews':reviews,
        'range':range(1,6)

    }
    return render(request,'main/product-details.html',context)
def shop(request):
    return render(request,'main/shop.html')

#profile creation
@login_required(login_url='login')
def customer_profile(request):
    profile=Profile.objects.get_or_create(user=request.user)
    profile_form=ProfileUpdateForm(instance=profile)

    if request.method=='POST':
        profile_form=ProfileUpdateForm(request.POST,request.FILES,instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('profile')
    
    context={
        'profile_form':profile_form,
        'user':request.user,
        'profile':request.user.profile

    }

    return render(request,'main/customer_profile.html',context)

