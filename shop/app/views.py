from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from .models import Product, Cart, Order
from .permissions import isClient
from .serializers import ProductSerializer, OrderSerializer


@api_view(["GET"])
def get_products(request):
    print(request)
    products = Product.objects.all()
    return Response(data= ProductSerializer(products, many=True).data,
                    status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAdminUser])
def post_products(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"data": {"id": serializer.data["id"], "message": "Product added"}},
                        status=status.HTTP_201_CREATED)
    return Response({"error": {"code": 422, "message": "Validation error", "errors": serializer.errors}},
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY)


@api_view(["GET", "PATCH", "DELETE"])
@permission_classes([IsAdminUser])
def update_product(request, **kwargs):
    try:
        product = Product.objects.get(pk=kwargs.get("pk", None))
    except:
        return Response({"error": {"code": 404, "message": "Not found"}}, status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        return Response({"data": ProductSerializer(product).data},
                        status=status.HTTP_200_OK)
    elif request.method == "PATCH":
        serializer = ProductSerializer(data=request.data, instance=product, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": {"id": serializer.data, "message": "Product updated"}},
                            status=status.HTTP_201_CREATED)
        return Response({"error": {"code": 422, "message": "Validation error", "errors": serializer.errors}},
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    if request.method == "DELETE":
        product.delete()
        return Response({'data': {"message": "Product removed"}}, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([isClient])
def get_cart(request):
    try:
        cart = Cart.objects.get(user=request.user)
        data = []
        count = 0
        for product in cart.products.all():
            count += 1
            data.append({
                "product_id": product.id,
                "name": product.name,
                "description": product.description,
                "price": product.price,
            })
        return Response({"data": {"products": data, "quantity": cart.quantity}}, status=status.HTTP_200_OK)
    except:
        return Response({"error": {"code": 404, "message": "Not found"}}, status=status.HTTP_404_NOT_FOUND)


@api_view(["POST", "DELETE"])
@permission_classes([isClient])
def update_cart(request, **kwargs):
    try:
        product = Product.objects.get(pk=kwargs["pk"])
    except:
        return Response({"error": {"code": 404, "message": "Not found"}}, status=status.HTTP_404_NOT_FOUND)
    cart, c = Cart.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        cart.products.add(product)
        cart.quantity += 1
        cart.save()
        return Response({"data": {"message": "Product add to cart"}}, status=status.HTTP_200_OK)
    if request.method == "DELETE":
        cart.products.remove(product)
        return Response({"data": {"message": "Item removed from cart"}}, status=status.HTTP_200_OK)


@api_view(["GET", "POST"])
@permission_classes([isClient])
def order(request):
    print(request.user)
    print(1)
    print(1)
    print(1)
    print(1)
    print(1)
    if request.method == "GET":
        order = Order.objects.filter(user=request.user)
        return Response({"data": OrderSerializer(order, many=True).data}, status=status.HTTP_200_OK)
    if request.method == 'POST':
        try:
            cart = Cart.objects.get(user=request.user)
        except:
            return Response(
                {"error": {
                    "code": 422,
                    "message": "Cart is empty"
                }},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        order = Order(user=request.user)
        order.save()
        full = 0
        for product in cart.products.all():
            order.products.add(product)
            full += product.price
        order.full_price = full
        order.quantity = cart.quantity
        order.save()
        cart.delete()
        return Response({"data": {"order_id": order.id, "message": "Order is processed"}},
                        status=status.HTTP_201_CREATED)
