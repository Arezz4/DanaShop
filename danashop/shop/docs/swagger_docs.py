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

shipping_address_get = swagger_auto_schema(
    operation_description="Retrieve all shipping addresses for the authenticated user.",
    responses={
        200: openapi.Response(
            description="List of shipping addresses.",
            examples={
                "application/json": [
                    {
                        "id": 1,
                        "user": 1,
                        "full_name": "John Doe",
                        "phone_number": "1234567890",
                        "address_line_1": "123 Main Street",
                        "address_line_2": "Apt 4B",
                        "city": "New York",
                        "state": "NY",
                        "postal_code": "10001",
                        "country": "USA",
                        "is_default": True
                    }
                ]
            }
        ),
        401: openapi.Response(description="Authentication required."),
    }
)

shipping_address_post = swagger_auto_schema(
    operation_description="Create a new shipping address for the authenticated user.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'full_name': openapi.Schema(type=openapi.TYPE_STRING, description="Full name of the recipient."),
            'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description="Phone number of the recipient."),
            'address_line_1': openapi.Schema(type=openapi.TYPE_STRING, description="Primary address line."),
            'address_line_2': openapi.Schema(type=openapi.TYPE_STRING, description="Secondary address line (optional)."),
            'city': openapi.Schema(type=openapi.TYPE_STRING, description="City."),
            'state': openapi.Schema(type=openapi.TYPE_STRING, description="State."),
            'postal_code': openapi.Schema(type=openapi.TYPE_STRING, description="Postal code."),
            'country': openapi.Schema(type=openapi.TYPE_STRING, description="Country."),
            'is_default': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Mark this address as default."),
        },
        required=['full_name', 'phone_number', 'address_line_1', 'city', 'state', 'postal_code', 'country']
    ),
    responses={
        201: openapi.Response(
            description="Shipping address created successfully.",
            examples={
                "application/json": {
                    "message": "Shipping address added successfully."
                }
            }
        ),
        400: openapi.Response(description="Invalid input."),
        401: openapi.Response(description="Authentication required."),
    }
)

shipping_address_put = swagger_auto_schema(
    operation_description="Update an existing shipping address for the authenticated user.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'full_name': openapi.Schema(type=openapi.TYPE_STRING, description="Full name of the recipient."),
            'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description="Phone number of the recipient."),
            'address_line_1': openapi.Schema(type=openapi.TYPE_STRING, description="Primary address line."),
            'address_line_2': openapi.Schema(type=openapi.TYPE_STRING, description="Secondary address line (optional)."),
            'city': openapi.Schema(type=openapi.TYPE_STRING, description="City."),
            'state': openapi.Schema(type=openapi.TYPE_STRING, description="State."),
            'postal_code': openapi.Schema(type=openapi.TYPE_STRING, description="Postal code."),
            'country': openapi.Schema(type=openapi.TYPE_STRING, description="Country."),
            'is_default': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Mark this address as default."),
        }
    ),
    responses={
        200: openapi.Response(
            description="Shipping address updated successfully.",
            examples={
                "application/json": {
                    "message": "Shipping address updated successfully."
                }
            }
        ),
        400: openapi.Response(description="Invalid input."),
        404: openapi.Response(description="Shipping address not found."),
        401: openapi.Response(description="Authentication required."),
    }
)

shipping_address_delete = swagger_auto_schema(
    operation_description="Delete an existing shipping address for the authenticated user.",
    responses={
        200: openapi.Response(
            description="Shipping address deleted successfully.",
            examples={
                "application/json": {
                    "message": "Shipping address deleted successfully."
                }
            }
        ),
        404: openapi.Response(description="Shipping address not found."),
        401: openapi.Response(description="Authentication required."),
    }
)
discount_code_create = swagger_auto_schema(
    operation_description="Create a new discount code (Admin only).",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'code': openapi.Schema(type=openapi.TYPE_STRING, description="Unique discount code."),
            'discount_percentage': openapi.Schema(type=openapi.TYPE_NUMBER, description="Discount percentage (e.g., 10.00 for 10%)."),
            'valid_from': openapi.Schema(type=openapi.FORMAT_DATETIME, description="Start date for the discount code."),
            'valid_until': openapi.Schema(type=openapi.FORMAT_DATETIME, description="End date for the discount code."),
            'is_active': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Whether the discount code is active."),
        },
        required=['code', 'discount_percentage', 'valid_from', 'valid_until', 'is_active']
    ),
    responses={
        201: openapi.Response(
            description="Discount code created successfully.",
            examples={
                "application/json": {
                    "message": "Discount code created successfully."
                }
            }
        ),
        400: openapi.Response(description="Invalid input."),
        403: openapi.Response(description="Permission denied."),
    }
)

discount_code_delete = swagger_auto_schema(
    operation_description="Delete an existing discount code (Admin only).",
    responses={
        200: openapi.Response(
            description="Discount code deleted successfully.",
            examples={
                "application/json": {
                    "message": "Discount code deleted successfully."
                }
            }
        ),
        404: openapi.Response(description="Discount code not found."),
        403: openapi.Response(description="Permission denied."),
    }
)
discount_code_post = swagger_auto_schema(
    operation_description="Validate a discount code.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'code': openapi.Schema(type=openapi.TYPE_STRING, description="Discount code to validate."),
        },
        required=['code']
    ),
    responses={
        200: openapi.Response(description="Discount code is valid."),
        400: openapi.Response(description="Discount code is expired or inactive."),
        404: openapi.Response(description="Invalid discount code."),
    }
)
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

cart_delete = swagger_auto_schema(
    operation_description="Remove a product from the cart.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'product_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the product to remove."),
        },
        required=['product_id']
    ),
    responses={
        200: openapi.Response(
            description="Product removed from cart successfully.",
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