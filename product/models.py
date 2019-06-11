from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.conf import settings



LABEL_CHOICES=(
	('P','primary'),
	('S','secondary'),
	('D','danger'),
)

class Category(models.Model):
	title=models.CharField(max_length=20)

	def __str__(self):
		return self.title


class Product(models.Model):
	title=models.CharField(max_length=100)
	overview=models.TextField()
	timestamp=models.DateTimeField(auto_now_add=True)
	thumbnail=models.ImageField()
	categories=models.ManyToManyField(Category)
	label=models.CharField(choices=LABEL_CHOICES,max_length=1)
	price=models.IntegerField()
	slug=models.SlugField()

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('p-detail',kwargs={
			'slug':self.slug
		})

	def get_add_to_cart_url(self):
		return reverse('add_to_cart',kwargs={
			'slug':self.slug
		})	

	def get_remove_from_cart_url(self):
		return reverse('remove_from_cart',kwargs={
			'slug':self.slug
		})	

class OrderItem(models.Model):
	user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	item=models.ForeignKey(Product,on_delete=models.CASCADE)
	quantity=models.IntegerField(default=1)
	ordered=models.BooleanField(default=False)
	def __str__(self):
		return f"{self.quantity} of {self.item.title}"

	def get_total_price(self):
		return self.quantity*self.item.price

	def get_final_price(self):
		return self.get_total_price()




class Order(models.Model):
	user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	items=models.ManyToManyField(OrderItem)
	start_date=models.DateTimeField(auto_now_add=True)
	ordered_date=models.DateTimeField()
	ordered=models.BooleanField(default=False)
	
	def __str__(self):
		return self.user.username

	def get_total(self):
		total=0
		for order_item in self.items.all():
			total+= order_item.get_final_price()
		return total

class CheckOut(models.Model):
	name=models.CharField(max_length=40)
	email=models.EmailField()
	address=models.TextField()
	country=models.CharField(max_length=20)
	zipcode=models.IntegerField()
	contactno=models.IntegerField()

	def __str__(self):
		return self.name





