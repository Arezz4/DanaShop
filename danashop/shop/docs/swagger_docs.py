from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..serializers import *

order_post = swagger_auto_schema(
    operation_description="Convert the cart to order.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'first_name': openapi.Schema(type=openapi.TYPE_STRING, description="First name of the user.", example="Ali"),
            'last_name': openapi.Schema(type=openapi.TYPE_STRING, description="Last name of the user.", example="Rezaei"),
            'shipping_address': openapi.Schema(type=openapi.TYPE_STRING, description="Shipping address.", example="Tehran, Khiyaban 123"),
            'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description="Phone number.", example="+989123456789"),
            'cart_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the cart to convert to order.", example=1),
            
        },
        required=['product_id']
    ),
    responses={
        201: openapi.Response(
            description="Order was placed successfully.",
            examples={
                "application/json": {
                    "message": "Order was placed successfully."
                }
            }
        ),
        400: openapi.Response(description="Invalid input."),
        401: openapi.Response(description="Authentication required."),
    }
)

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

cart_get = swagger_auto_schema(
    operation_description="Retrieve the cart for the authenticated user.",
    responses={
        200: openapi.Response(
            description="Cart retrieved successfully.",
            examples={
                "application/json": {
                    "id": 1,
                    "user": 1,
                    "items": [
                        {
                            "id": 1,
                            "product": 1,
                            "product_name": "Smartphone",
                            "product_price": 299.99,
                            "quantity": 2
                        }
                    ],
                    "created_at": "2023-05-01T12:00:00Z"
                }
            }
        ),
        401: openapi.Response(description="Authentication required."),
    }
)

cart_post = swagger_auto_schema(
    operation_description="Add or update a product in the cart.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'product_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the product to add or update."),
            'quantity': openapi.Schema(type=openapi.TYPE_INTEGER, description="Quantity of the product.", default=1),
        },
        required=['product_id']
    ),
    responses={
        201: openapi.Response(
            description="Product added to cart successfully.",
            examples={
                "application/json": {
                    "message": "Product added to cart successfully."
                }
            }
        ),
        400: openapi.Response(description="Invalid input."),
        404: openapi.Response(description="Product not found."),
        401: openapi.Response(description="Authentication required."),
    }
)

cart_update = swagger_auto_schema(
    operation_description="Update a product's quantity.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'new_quantity': openapi.Schema(type=openapi.TYPE_INTEGER, description="New quantity."),
        },
        required=['new_quantity']
    ),
    responses={
        200: openapi.Response(
            description="Cart was updated successfully.",
            examples={
                "application/json": {
                    "message": "Product removed from cart successfully."
                }
            }
        ),
        404: openapi.Response(description="Product not found in cart or cart not found."),
        401: openapi.Response(description="Authentication required."),
    }
)