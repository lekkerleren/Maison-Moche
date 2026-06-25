from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    objects = UserManager()
    username =  None 
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Category(models.Model): # top level category model
    name = models.CharField(max_length=100)
    handle = models.SlugField(max_length=100, unique=True)
    parent = models.ForeignKey('self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='children'
    )
        
    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
    
class Supplier(models.Model):
    supplier_name = models.CharField(max_length=100)
    supplier_email = models.EmailField(max_length=100)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    
    def __str__(self):
        return self.supplier_name
    
class Brand(models.Model):
    brand_name = models.CharField(max_length=100)
    brand_description = models.TextField()
    
    def __str__(self):
        return self.brand_name
    
    
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products') # points to Category model
    handle = models.SlugField(max_length=100, unique=True)
    product_title = models.CharField(max_length=140)
    description = models.TextField()
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='products') # points to Supplier model
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products') # points to Brand model
    style = models.CharField(max_length=100, null=True, blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_title
    
class Collection(models.Model):
    name = models.CharField(max_length=100)
    handle = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    products = models.ManyToManyField(Product, related_name='collections', blank=True) # many-to-many relationship with Product model

    def __str__(self):
        return self.name

class Variant(models.Model):
    active = models.BooleanField(default=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants') # points to Product model
    handle = models.SlugField(max_length=100, unique=True)
    variant_title = models.CharField(max_length=140)
    primary_material = models.CharField(max_length=100)
    secondary_material = models.CharField(max_length=100, null=True, blank=True)
    primary_color = models.CharField(max_length=100)
    secondary_color = models.CharField(max_length=100, null=True, blank=True)
    length = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    width = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    depth = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    diameter = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    total_weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    number_of_packages = models.IntegerField()
    stock_quantity = models.IntegerField()
    stock_location = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    collections = models.ManyToManyField(Collection, related_name='variants', blank=True) # many-to-many relationship with Collection model

    def __str__(self):
        return self.variant_title    

class VariantImage(models.Model):
    variant = models.ForeignKey(Variant, null=True, blank=True, on_delete=models.SET_NULL, related_name='variant_images') # points to Variant model
    image_url = models.URLField(max_length=200)
    display_order = models.IntegerField()

    def __str__(self):
        return self.image_url
    
    
class VariantShipping(models.Model):
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, related_name='variant_shipping') # points to Variant model
    loading_type = models.CharField(max_length=100)
    shipping_weight = models.DecimalField(max_digits=5, decimal_places=2)
    package_length = models.DecimalField(max_digits=5, decimal_places=2)
    package_width = models.DecimalField(max_digits=5, decimal_places=2)
    package_height = models.DecimalField(max_digits=5, decimal_places=2)
    
    def __str__(self):
        return f"Shipping for variant {self.variant_id}"
    
    
class TableAttribute(models.Model):
    variant = models.OneToOneField(Variant, on_delete=models.CASCADE, related_name='table_attributes') # points to Product model
    tabletop_material = models.CharField(max_length=100)
    tabletop_color = models.CharField(max_length=100)
    tabletop_height = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"Table attributes for variant {self.variant_id}"

class LightingAttribute(models.Model):
    variant = models.OneToOneField(Variant, on_delete=models.CASCADE, related_name='lighting_attributes') # points to Product model
    lighting_material = models.CharField(max_length=100)
    lighting_color = models.CharField(max_length=100)
    lighting_height = models.DecimalField(max_digits=5, decimal_places=2)
    
    def __str__(self):
        return f"Lighting attributes for variant {self.variant_id}"
    
class SeatingAttribute(models.Model):
    variant = models.OneToOneField(Variant, on_delete=models.CASCADE, related_name='seating_attributes') # points to Product model
    seating_material = models.CharField(max_length=100)
    seating_color = models.CharField(max_length=100)
    seating_height = models.DecimalField(max_digits=5, decimal_places=2)
    seating_depth = models.DecimalField(max_digits=5, decimal_places=2)
    seating_width = models.DecimalField(max_digits=5, decimal_places=2)
    armchair_height = models.DecimalField(max_digits=5, decimal_places=2)
    corner_side = models.CharField(max_length=10)
    
    def __str__(self):
        return f"Seating attributes for variant {self.variant_id}"
    
class DecorativeAttribute(models.Model):
    variant = models.OneToOneField(Variant, on_delete=models.CASCADE, related_name='decorative_attributes')
    # TODO: expand decorative attributes

    def __str__(self):
        return f"Decorative attributes for variant {self.variant_id}"
    

# TODO: add model for undercarriage data
# TODO: write serializers