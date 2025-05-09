from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..serializers import ProductSerializer

product_create = swagger_auto_schema(
    request_body=ProductSerializer,
    responses={201: ProductSerializer, 400: "Bad Request"}
)

product_update =swagger_auto_schema(
    request_body=ProductSerializer,
    responses={201: ProductSerializer, 400: "Bad Request"}
)