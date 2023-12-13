from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid
from decimal import Decimal




class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, max_length=50)
    image = models.ImageField(upload_to='category_images', null=True, blank=True)

    def __str__(self):
        return self.name
    @property
    def imageURL(self):
        try:
            url=self.image.url
        except:
            url=''
        return url


class Product(models.Model):
    tags = models.ManyToManyField(Tag, related_name='products')
    image = models.ImageField(upload_to='product_images/')
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    specifications = models.TextField(max_length=1000, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    availability=models.CharField(max_length=20, choices=[('In Stock', 'In Stock'), ('Out of Stock', 'Out of Stock')])
    stock = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    reviews = models.ManyToManyField('Customer', related_name="reviewedproducts", through="Review")
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.CharField(max_length=50, unique=True, blank=True, primary_key=True, default=uuid.uuid4)

    def __str__(self):
        return self.name
    class Meta:
        ordering = ['-created_at']


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    middlename = models.CharField(max_length=255, null=True, blank=True)
    lastname = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='profilepics', default='user.png', null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    alternate_email = models.EmailField(max_length=255, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    @property
    def imageURL(self):
        try:
            url=self.image.url
        except:
            url=''
        return url


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    ordered_date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, default=0, decimal_places=2)
    complete = models.BooleanField(default=False, null=True, blank=True)
    payment_method = models.CharField(max_length=20, choices=[('Credit Card', 'Credit Card'), ('M-PESA', 'M-PESA'), ('Cash on Delivery', 'Cash on Delivery')])
    shipping_method = models.CharField(max_length=20, choices=[('Standard', 'Standard'), ('Express', 'Express'), ('Pickup', 'Pickup')])
    order_id = models.CharField(unique=True, editable=False, default=uuid.uuid4, max_length=10)
    def __str__(self):
        return f"Order #{self.order_id} by {self.customer}"
    class Meta:
        ordering = ['-ordered_date']
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total() for item in orderitems])
        return total
    

    @property
    def vat(self):
        sub_total = self.get_cart_total
        total_vat = sub_total * Decimal('0.16')
        return total_vat

    @property
    def get_order_total(self):
        sub_total = self.get_cart_total
        vat = self.vat
        total = sub_total + vat
        return total


    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

   
        

    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order #{self.order.id}"
   
    def get_total(self):
        total =  self.product.price * self.quantity
        return total
    

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL,null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL,null=True, blank=True)
    address = models.CharField(max_length=100, null=False)
    city = models.CharField(max_length=100, null=False)
    county = models.CharField(max_length=100, null=False)
    postal_code = models.CharField(max_length=100, null=False)
    date_added = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return self.address

class Review(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.customer} - {self.product.name} - {self.rating}'