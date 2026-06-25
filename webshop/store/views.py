from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, LoginSerializer, VariantListSerializer, VariantDetailSerializer
from .models import User, Variant, Category
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            } , status=status.HTTP_201_CREATED
        )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():        
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            } , status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class VariantListView(APIView):
    
    def get(self, request):
        queryset = Variant.objects.filter(active=True) # filter by active

        category = request.query_params.get('category')
        if category:
            cat = Category.objects.get(handle=category)
            category_ids = Category.objects.filter(parent=cat).values_list('id', flat=True)
            queryset = queryset.filter(product__category__in=[cat.id, *category_ids])

        brand = request.query_params.get('brand')
        if brand:
            queryset = queryset.filter(product__brand__brand_name=brand)

        serializer = VariantListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class VariantDetailView(APIView):
  
    def get(self, request, handle):
        try:
            serializer = VariantDetailSerializer(Variant.objects.get(active=True, handle=handle))
            return Response(serializer.data, status=status.HTTP_200_OK)         
        except Variant.DoesNotExist:
            return Response({"error": "variant not found"}, status=status.HTTP_404_NOT_FOUND)