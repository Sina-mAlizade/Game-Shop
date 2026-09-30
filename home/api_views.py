from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q
from .models import Game, Cart, CartItem
from .serializers import CartSerializer, GameSerializer


def get_user_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_cart_detail(request):
    cart = get_user_cart(request.user)
    return Response(CartSerializer(cart).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_add_to_cart(request, game_id):
    game = Game.objects.get(id=game_id)
    cart = get_user_cart(request.user)

    item, created = CartItem.objects.get_or_create(cart=cart, game=game)
    if not created:
        item.quantity += 1
        item.save()

    return Response(CartSerializer(cart).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_increase_quantity(request, item_id):
    cart = get_user_cart(request.user)
    item = CartItem.objects.get(id=item_id, cart=cart)
    item.quantity += 1
    item.save()
    return Response(CartSerializer(cart).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_decrease_quantity(request, item_id):
    cart = get_user_cart(request.user)
    item = CartItem.objects.get(id=item_id, cart=cart)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return Response(CartSerializer(cart).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_remove_item(request, item_id):
    cart = get_user_cart(request.user)
    CartItem.objects.filter(id=item_id, cart=cart).delete()
    return Response(CartSerializer(cart).data)


@api_view(['GET'])
def api_search_games(request):
    query = request.GET.get('q', '')
    if len(query) < 2:
        return Response([])

    games = Game.objects.filter(
        Q(title__icontains=query) | Q(category__icontains=query)
    )[:6]

    return Response(GameSerializer(games, many=True).data)