from rest_framework import serializers
from .models import Supplier, Brand, User, Product, Variant, VariantImage, VariantShipping, Collection, TableAttribute, LightingAttribute, SeatingAttribute, DecorativeAttribute

#registration and login

class RegisterSerializer(serializers.Serializer): #validates registration data and creates user
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)

    def create(self, validated_data): 
        try:
            user = User.objects.create_user(
                email=validated_data["email"], 
                password=validated_data["password"], 
                first_name=validated_data["first_name"], 
                last_name=validated_data["last_name"]
                )
        except Exception as e:
            raise serializers.ValidationError(str(e))
        return user
    
class LoginSerializer(serializers.Serializer): #validates login data and returns user
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist: raise serializers.ValidationError("invalid credentials")

        if user.check_password(password):
            return user
        else:
            raise serializers.ValidationError("invalid credentials")
        
# nestable serializers
        
class VariantImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariantImage
        fields = ('image_url', 'display_order')


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('brand_name', 'brand_description')

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('product_title', 'description', 'category', 'handle', 'brand', 'style', 'active', 'created_at', 'updated_at')
    
class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ('name', 'handle', 'description')
    
class TableAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableAttribute
        fields = ('tabletop_material', 'tabletop_color', 'tabletop_height')
    
class LightingAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LightingAttribute
        fields = ('lighting_material', 'lighting_color', 'lighting_height')
    
class SeatingAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeatingAttribute
        fields = ('seating_material', 'seating_color', 'seating_height', 'seating_depth', 'seating_width', 'armchair_height', 'corner_side')
    


# pdp and plp

class VariantListSerializer(serializers.ModelSerializer): #serializer for plp use
    variant_image = VariantImageSerializer(source='variant_images', many=True)
    
    class Meta:
        model = Variant
        fields = ('variant_title', 'price', 'handle', 'variant_image')

class VariantDetailSerializer(serializers.ModelSerializer): #serializer for pdp use
    product = ProductSerializer()
    variant_image = VariantImageSerializer(source='variant_images', many=True)
    collection = CollectionSerializer(source='collections', many=True)
    table_attribute = TableAttributeSerializer(source='table_attributes', many=True)
    lighting_attribute = LightingAttributeSerializer(source='lighting_attributes', many=True)
    seating_attribute = SeatingAttributeSerializer(source='seating_attributes', many=True)

    class Meta:
        model = Variant
        fields = ('variant_title', 'price', 'handle', 'product', 'variant_image', 'collection', 'table_attribute', 'lighting_attribute', 'seating_attribute')


