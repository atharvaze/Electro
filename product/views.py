from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist,MultipleObjectsReturned
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,get_object_or_404,redirect,reverse
from django.views.generic import ListView,DetailView,View
from product.models import Category,Product,Order,OrderItem,CheckOut
from .forms import CheckoutForm
from django.utils import timezone
from django.db.models import Count, Q
from django.core.mail import send_mail



def search(request):
	queryset=Product.objects.all()
	query=request.GET.get('q')
	if query:
		queryset=queryset.filter(
			Q(title__icontains=query) |
			Q(overview__icontains=query)
		).distinct()
	context={
		'queryset':queryset
	}
	return render(request,'search_results.html',context)





class HomeView(ListView):
    model=Product
    template_name="index.html"


class OrderSummaryView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):

        try:
            order=Order.objects.get(user=self.request.user, ordered=False)
            context={
                'object':order
            }
            return render(self.request,'order_summary.html',context)
        except ObjectDoesNotExist:
            messages.error(self.request,"You dont have an active order!")
            return redirect("/")


        



class ProductDetailView(DetailView):
    model=Product
    template_name="product.html"




def store(request):
    return render(request,'store.html',{})


@login_required
def check(request):
    
    order=Order.objects.get(user=request.user, ordered=False)
    context={
        'order':order
    }
    return render(request,'checkout.html',context)

@login_required
def finalorder(request):
    
    order=Order.objects.get(user=request.user, ordered=False)
    context={
        'order':order
    }
    return render(request,'almostcheck.html',context)
    

@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Product,slug=slug)
    order_item, created=OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs=Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order=order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity+=1
            order_item.save()
            messages.info(request,"This item quantity was updated!")
            return redirect("p-detail",slug=slug)
        else:

            order.items.add(order_item)
            messages.info(request,"This item was added!")
            return redirect("p-detail",slug=slug)
    else:
        ordered_date=timezone.now()
        order=Order.objects.create(user=request.user,ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request,"This item was added!")
        return redirect("p-detail",slug=slug)

@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Product,slug=slug)
    order_qs=Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order=order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item=OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            messages.info(request,"This item was removed!")
            return redirect("p-detail",slug=slug) 
        else:
            messages.info(request,"Your order does not have this item!")
            return redirect("p-detail",slug=slug)

        
            
    else:
        messages.info(request,"You dont have any orders!")
        return redirect("p-detail",slug=slug)

@login_required
def remove_single_from_cart(request, slug):
    item = get_object_or_404(Product,slug=slug)
    order_qs=Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order=order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item=OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity>1:
                order_item.quantity-=1
                order_item.save()
            else:
                order.items.remove(order_item)

            messages.info(request,"Your order quantity was updated!")
            return redirect("order-summary") 
        else:
            messages.info(request,"Your order does not have this item")
            return redirect("p-detail",slug=slug)

        
            
    else:
        messages.info(request,"You dont have any orders!")
        return redirect("p-detail",slug=slug)


@login_required
def add_single_from_cart(request, slug):
    item = get_object_or_404(Product,slug=slug)
    order_qs=Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order=order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item=OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order_item.quantity+=1
            order_item.save()
            messages.info(request,"Your order quantity was updated!")
            return redirect("order-summary") 
        else:
            messages.info(request,"Your order does not have this item")
            return redirect("p-detail",slug=slug)

        
            
    else:
        messages.info(request,"You dont have any orders!")
        return redirect("p-detail",slug=slug)


def checkout(request):
    orderr=Order.objects.get(user=request.user, ordered=False)
    form=CheckoutForm(request.POST or None)
    if form.is_valid():
        
        email = form.cleaned_data['email']
        name = form.cleaned_data['name']
        form.save()
        subject=f" Dear {name} , your order confirmation"
        send_mail(
            subject,
            'This is an automated email. Thankyou for ordering from Electro.Your order will be delivered soon. The payment method being COD.',
            'waze.atharva@yahoo.com',
            [email]
        
            )       
        form.save()
        try:
            Ord=Order.objects.get(user=request.user)
            Ord.ordered=True
            Ord.save()
            messages.info(request,"Your order has been placed successfully!")
        except(MultipleObjectsReturned):
            Ord=Order.objects.filter(user=request.user).order_by('id').last()
            Ord.ordered=True
            Ord.save()
            messages.info(request,"Your order has been placed successfully!")
        

        return redirect(reverse('home'))
        




    return render(request,'almostcheck.html',{
        'form':form,
        'order':orderr
    })


# def mail(request):
#     form=CheckoutForm(request.POST or None)
#     if form.is_valid():
#         email = form.cleaned_data['email']
#         name = form.cleaned_data['name']
#         subject='f" Dear {name} , your order confirmation"'
#         send_mail(
#             subject,
#             'This is an automated email. Thankyou for ordering from Electro.Your order will be delivered soon. The payment method being COD.',
#             'waze.atharva@yahoo.com',
#             [email]
#             )
#         return redirect(reverse('home'))


    