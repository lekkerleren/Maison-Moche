from django.db import models

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
    
class Product(models.Model):
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL, related_name='products') # points to Category model
    name = models.CharField(max_length=100)
    handle = models.SlugField(max_length=100, unique=True)
    product_title = models.CharField(max_length=140)
    description = models.TextField()
    supplier = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    style = models.CharField(max_length=100, null=True, blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class Variant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants') # points to Product model
    name = models.CharField(max_length=100)
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
    total_weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    number_of_packages = models.IntegerField()
    stock_quantity = models.IntegerField()
    stock_location = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)

    def __str__(self):
        return self.name    

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
    
class Collection(models.Model):
    name = models.CharField(max_length=100)
    handle = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    products = models.ManyToManyField(Product, related_name='collections', blank=True) # many-to-many relationship with Product model

    def __str__(self):
        return self.name
    
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

