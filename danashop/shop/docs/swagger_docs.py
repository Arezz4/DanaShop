from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..serializers import ProductSerializer,ProductFilterSerializer

product_create = swagger_auto_schema(
    request_body=ProductSerializer,
    responses={201: ProductSerializer, 400: "Bad Request"}
)

product_update =swagger_auto_schema(
    request_body=ProductSerializer,
    responses={201: ProductSerializer, 400: "Bad Request"}
)
product_filter = swagger_auto_schema(
    operation_description="Filter products by category, price range, name, and stock availability.",
    manual_parameters=[
        openapi.Parameter(
            'category',
            openapi.IN_QUERY,
            description="Category ID to filter products (includes subcategories).",
            type=openapi.TYPE_INTEGER
        ),
        openapi.Parameter(
            'min_price',
            openapi.IN_QUERY,
            description="Minimum price to filter products.",
            type=openapi.TYPE_NUMBER,
            format=openapi.FORMAT_FLOAT
        ),
        openapi.Parameter(
            'max_price',
            openapi.IN_QUERY,
            description="Maximum price to filter products.",
            type=openapi.TYPE_NUMBER,
            format=openapi.FORMAT_FLOAT
        ),
        openapi.Parameter(
            'search',
            openapi.IN_QUERY,
            description="Regex search in product names (case-insensitive).",
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            'in_stock',
            openapi.IN_QUERY,
            description="Filter products by stock availability (true/false).",
            type=openapi.TYPE_BOOLEAN
        ),
    ],
    responses={
        200: openapi.Response(
            description="A list of filtered products.",
            examples={
                "application/json": [
                    {
                        "id": 1,
                        "name": "Smartphone",
                        "description": "A high-end smartphone",
                        "price": 299.99,
                        "category": 2,
                        "in_stock": True,
                        "created_at": "2023-05-01T12:00:00Z"
                    },
                    {
                        "id": 2,
                        "name": "Laptop",
                        "description": "A powerful laptop",
                        "price": 999.99,
                        "category": 3,
                        "in_stock": True,
                        "created_at": "2023-05-02T12:00:00Z"
                    }
                ]
            }
        ),
        400: openapi.Response(description="Bad Request"),
    }
)
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

product_review = swagger_auto_schema(
    operation_description="Create/edit reviews for a specific product.",
    manual_parameters=[
        openapi.Parameter(
            'product_id',
            openapi.IN_PATH,
            description="ID of the product for which reviews are being retrieved or created.",
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'rating': openapi.Schema(type=openapi.TYPE_INTEGER, description="Rating out of 5", example=5),
            'comment': openapi.Schema(type=openapi.TYPE_STRING, description="Review comment", example="Great product!"),
        },
        required=['rating', 'comment']
    ),
    responses={
        201: openapi.Response(
            description="Review created successfully.",
            examples={
                "application/json": {
                    "id": 3,
                    "user": "john_doe",
                    "rating": 5,
                    "comment": "Excellent product!",
                    "created_at": "2023-05-03T12:00:00Z"
                }
            }
        ),
        400: openapi.Response(description="Bad Request"),
        404: openapi.Response(description="Product not found"),
    }
)