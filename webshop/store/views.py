from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from .serializers import AdminVariantSerializer, RegisterSerializer, LoginSerializer, VariantListSerializer, VariantDetailSerializer
from .models import User, Variant, Category
from rest_framework_simplejwt.tokens import RefreshToken
from .pagination import StandardPagination

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
            queryset = queryset.filter(product__brand__handle=brand)

        sort = request.query_params.get('sort')
        if sort == 'price_asc':
            queryset = queryset.order_by('price')
        elif sort == 'price_desc':
            queryset = queryset.order_by('-price')
        elif sort == 'newest':
            queryset = queryset.order_by('-product__created_at')

        paginator = StandardPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = VariantListSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)
    
class VariantDetailView(APIView):
  
    def get(self, request, handle):
        try:
            serializer = VariantDetailSerializer(Variant.objects.get(active=True, handle=handle))
            return Response(serializer.data, status=status.HTTP_200_OK)         
        except Variant.DoesNotExist:
            return Response({"error": "variant not found"}, status=status.HTTP_404_NOT_FOUND)
        

class AdminVariantViewset(ModelViewSet):

    def get_queryset(self):
        queryset = Variant.objects.all()
        active = self.request.query_params.get('active')
        if active:
            queryset = queryset.filter(active=True)
        return queryset

    serializer_class = AdminVariantSerializer
    permission_classes = [IsAdminUser]  # Only admin users can access this viewset
    