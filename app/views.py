from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from django.http import JsonResponse
import razorpay
# from . import Payment
from .models import Product,Customer,Cart,Payment,OrderPlaced,Wishlist
from django.db.models import Count
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.
@login_required
def home(request):
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(Wishlist.objects.filter(user=request.user))
    return render(request,'Home.html',locals())

@login_required
def about(request):
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(Wishlist.objects.filter(user=request.user))
    return render(request,'about.html',locals())

@login_required
def contact(request):
    totalitem=0
    wishitem=0
    
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(Wishlist.objects.filter(user=request.user))
        
    return render(request,'contact.html',locals())

@method_decorator(login_required,name='dispatch')
class CategoryView(View):
    def get(self,request,val):
        totalitem=0
        wishitem=0
        
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            wishitem=len(Wishlist.objects.filter(user=request.user))
            
        product=Product.objects.filter(category=val)
        title=Product.objects.filter(category=val).values('title')
        return render(request,'category.html',locals())
    
@method_decorator(login_required,name='dispatch')
class CategoryTitle(View):
    def get(self,request,val):
        product=Product.objects.filter(title=val)
        title=Product.objects.filter(category=product[0].category).values('title')
        totalitem=0
        wishitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            wishitem=len(Wishlist.objects.filter(user=request.user))
        return render(request,'category.html',locals())

@method_decorator(login_required,name='dispatch') 
class ProductDetail(View):
    def get(self,request,pk):
        product=Product.objects.get(pk=pk)
        wishlist = Wishlist.objects.filter(Q(product=product)&Q(user=request.user))
        totalitem=0
        wishitem=0
        # wishlist=False
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            wishitem=len(Wishlist.objects.filter(user=request.user))
            # wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()
        return render(request,'productdetail.html',locals())
    
# class CustomerRegistrationView(View):
#     def get(self,request):
#         form=CustomerRegistrationForm()
#         return render(request,'customerregistration.html',locals())
#     def post(self,request):
#         form=CustomerRegistrationForm(request.POST)
#         if form.is_valid():
#             print('cleaned Data;',form.cleaned_data)
#             form.save()
#             messages.success(request,'Congratulations! User Register Successfully ')
#         else:from django.views import View
# from django.shortcuts import render
# from django.contrib import messages
# from .forms import CustomerRegistrationForm

# @method_decorator(login_required,name='dispatch')
class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        totalitem=0
        wishitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            wishitem=len(Wishlist.objects.filter(user=request.user))
        return render(request, 'customerregistration.html', {'form': form})  # Avoid `locals()`

    def post(self, request):
        # print("POST Data:", request.POST)  # Debugging line to check email in request
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            # print("Cleaned Data:", form.cleaned_data)  # Debugging line to check email
            form.save()
            # print("Saved Email:", user.email)  # Confirm email is assigned
            messages.success(request, 'Congratulations! User Registered Successfully.')
        else:
            messages.warning(request, "Invalid Input Data")
        return render(request, 'customerregistration.html', {'form': form})  # Avoid `locals()`

@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self, request):
        form=CustomerProfileForm()
        totalitem=0
        wishitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            wishitem=len(Wishlist.objects.filter(user=request.user))
        return render(request,'profile.html',locals())
    def post(self, request):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            user=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            mobile=form.cleaned_data['mobile']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']
            
            reg=Customer(user=user,name=name,locality=locality,mobile=mobile,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,"Congratulations! Profile Save Successfully")
        else:
            messages.warning(request,'Invalid Input Data')
        return render(request,'profile.html',locals())
    
@login_required
def address(request):
    add=Customer.objects.filter(user=request.user)
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(Wishlist.objects.filter(user=request.user))
    return render(request,'address.html',locals())

@method_decorator(login_required,name='dispatch')
class updateAddress(View):
    def get(self,request,pk):
        add=Customer.objects.get(pk=pk)
        form=CustomerProfileForm(instance=add)
        totalitem=0
        wishitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            wishitem=len(Wishlist.objects.filter(user=request.user))
            
        return render(request,'updateAddress.html',locals())
    def post(self,request,pk):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            add=Customer.objects.get(pk=pk)
            add.name=form.cleaned_data['name']
            add.locality=form.cleaned_data['locality']
            add.city=form.cleaned_data['city']
            add.mobile=form.cleaned_data['mobile']
            add.state=form.cleaned_data['state']
            add.zipcode=form.cleaned_data['zipcode']
            add.save()
            messages.success(request,"Congratulation! Profile Update Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return redirect('address')
    
@login_required
def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')

@login_required
def show_cart(request):
    user=request.user
    cart=Cart.objects.filter(user=user)
    amount=0
    for p in cart:
        value=p.quantity * p.product.discounted_price
        amount=amount + value
    totalamount=amount+40
    totalitem=0
    wishitem=0
    
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(Wishlist.objects.filter(user=request.user))
    return render(request,'addtocart.html',locals())


@method_decorator(login_required,name='dispatch')
class checkout(View):
    def get(self, request):
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        
        famount = sum([p.quantity * p.product.discounted_price for p in cart_items])
        totalamount = famount + 40
        razoramount = int(totalamount * 100)

        # Razorpay client initialization
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        data = {"amount": razoramount, "currency": 'INR', "receipt": 'order_reptid_12'}
        payment_response = client.order.create(data=data)

        order_id = payment_response['id']
        order_status = payment_response['status']

        if order_status == 'created':
            payment = Payment(
                user=user,
                amount=totalamount,
                razorpay_order_id=order_id,
                razorpay_payment_status=order_status
            )
            payment.save()

        context = {
            'add': add,
            'cart_items': cart_items,
            'totalamount': totalamount,
            'razorpay_order_id': order_id,
            'razorpay_merchant_key': settings.RAZOR_KEY_ID,
            'razoramount': razoramount
        }
        return render(request, 'checkout.html', context)

@login_required
def payment_done(request):
    if request.method == "POST":
        order_id = request.POST.get('order_id')
        payment_id = request.POST.get('payment_id')
        cust_id = request.POST.get('cust_id')

        user = request.user
        customer = Customer.objects.get(id=cust_id)
        payment = Payment.objects.get(razorpay_order_id=order_id)

        payment.paid = True
        payment.razorpay_payment_id = payment_id
        payment.razorpay_payment_status = 'Success'
        payment.save()

        cart = Cart.objects.filter(user=user)
        for c in cart:
            OrderPlaced.objects.create(
                user=user,
                customer=customer,
                product=c.product,
                quantity=c.quantity,
                payment=payment
            )
            c.delete()

        return render(request, 'paymentdone.html')


@login_required
def orders(request):
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(Wishlist.objects.filter(user=request.user))
        
    order_placed=OrderPlaced.objects.filter(user=request.user)
    return render(request, 'orders.html',locals())

@login_required
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        
        
        c = Cart.objects.filter(Q(product__id=prod_id) & Q(user=request.user)).first()

        if c:  
            c.quantity += 1
            c.save()
        
        
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = sum(p.quantity * p.product.discounted_price for p in cart)
        totalamount = amount + 40

        data = {
            'quantity': c.quantity if c else 0,  
            'amount': amount,
            'totalamount': totalamount,
        }
        return JsonResponse(data)

    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')

        # Use .filter().first() to avoid MultipleObjectsReturned error
        c = Cart.objects.filter(Q(product=prod_id) & Q(user=request.user)).first()
        
        if c:
            c.quantity += 1
            c.save()

            # Calculate updated totals
            cart_items = Cart.objects.filter(user=request.user)
            amount = sum(item.quantity * item.product.discounted_price for item in cart_items)
            totalamount = amount + 40  # Assuming 40 is delivery charge

            data = {
                'quantity': c.quantity,
                'amount': amount,
                'totalamount': totalamount,
            }
            return JsonResponse(data)
        else:
            return JsonResponse({"error": "Cart item not found"}, status=400)

@login_required
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        
        # ✅ Fix: Use .filter().first() to avoid errors
        c = Cart.objects.filter(Q(product__id=prod_id) & Q(user=request.user)).first()

        if c:  # ✅ Only update if cart item exists
            c.quantity -= 1
            c.save()
        
        # ✅ Recalculate amounts
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = sum(p.quantity * p.product.discounted_price for p in cart)
        totalamount = amount + 40

        data = {
            'quantity': c.quantity if c else 0,  # ✅ Ensure response doesn't break
            'amount': amount,
            'totalamount': totalamount,
        }
        return JsonResponse(data)

    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')

        # Use .filter().first() to avoid MultipleObjectsReturned error
        c = Cart.objects.filter(Q(product=prod_id) & Q(user=request.user)).first()
        
        if c:
            c.quantity += 1
            c.save()

            # Calculate updated totals
            cart_items = Cart.objects.filter(user=request.user)
            amount = sum(item.quantity * item.product.discounted_price for item in cart_items)
            totalamount = amount + 40  # Assuming 40 is delivery charge

            data = {
                'quantity': c.quantity,
                'amount': amount,
                'totalamount': totalamount,
            }
            return JsonResponse(data)
        else:
            return JsonResponse({"error": "Cart item not found"}, status=400)
        
@login_required   
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        
        # ✅ Fix: Use .filter().first() to avoid errors
        c = Cart.objects.filter(Q(product__id=prod_id) & Q(user=request.user)).first()

        c.delete()
        
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = sum(p.quantity * p.product.discounted_price for p in cart)
        totalamount = amount + 40

        data = {
            'amount': amount,
            'totalamount': totalamount,
        }
        return JsonResponse(data)

    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')

        # Use .filter().first() to avoid MultipleObjectsReturned error
        c = Cart.objects.filter(Q(product=prod_id) & Q(user=request.user)).first()
        
        if c:
            c.quantity += 1
            c.save()

            # Calculate updated totals
            cart_items = Cart.objects.filter(user=request.user)
            amount = sum(item.quantity * item.product.discounted_price for item in cart_items)
            totalamount = amount + 40  # Assuming 40 is delivery charge

            data = {
                'quantity': c.quantity,
                'amount': amount,
                'totalamount': totalamount,
            }
            return JsonResponse(data)
        else:
            return JsonResponse({"error": "Cart item not found"}, status=400)
        
@login_required
def plus_wishlist(request):
    if request.method == 'GET':
        prod_id=request.GET.get('prod_id')
        product = get_object_or_404(Product, id=prod_id)
        Wishlist.objects.get_or_create(user=request.user, product=product)
        data={
            'message':'Wishlist Added Successfully',
        }
        return JsonResponse(data)

@login_required
def minus_wishlist(request):
    if request.method == 'GET':
        prod_id=request.GET.get('prod_id')
        product = get_object_or_404(Product, id=prod_id)
        Wishlist.objects.filter(user=request.user,product=product).delete()
        data={
            'message':'Wishlist Removed Successfully',
        }
        return JsonResponse(data)

@login_required  
def search(request):
    query=request.GET['search']
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(Wishlist.objects.filter(user=request.user))
    product=Product.objects.filter (Q(title__icontains=query))
    return render(request,'search.html',locals())