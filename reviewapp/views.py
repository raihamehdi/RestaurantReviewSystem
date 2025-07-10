# use this command on CMD to run docker: docker run -p 6379:6379 redis

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Restaurant, Review
from .serializers import RestaurantSerializer
from .sentiments import analyze_sentiment
from .redis_utils import update_leaderboard, get_leaderboard
import redis
from django.http import JsonResponse
from rest_framework import status
from .sentiment import analyze_sentiment
from .leaderboard import update_leaderboard
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return render(request, 'index.html')

def review(request):
    return render(request, 'review.html')

# def leaderboard_page(request):
#     return render(request, 'leaderboard.html')

@csrf_exempt
@api_view(['POST'])
def add_restaurant(request):
    serializer = RestaurantSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

@api_view(['POST'])
def add_review(request):
    name = request.data.get("name")
    text = request.data.get("text")

    if not name or not text:
        return Response({"error": "Name and text are required."}, status=400)

    try:
        restaurant = Restaurant.objects.get(name__iexact=name)
    except Restaurant.DoesNotExist:
        return Response({"error": "Restaurant not found."}, status=404)

    sentiment_score = analyze_sentiment(text)
    Review.objects.create(restaurant=restaurant, text=text, sentiment_score=sentiment_score)

    update_leaderboard(restaurant.id, sentiment_score)

    return Response({"sentiment_score": sentiment_score}, status=201)


def get_leaderboard(request):  
    r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
    leaderboard = r.zrevrange('restaurant_leaderboard', 0, 9, withscores=True)

    data = []
    for restaurant_id, score in leaderboard:
        try:
            restaurant = Restaurant.objects.get(id=restaurant_id)
            data.append({
                'restaurant_name': restaurant.name,
                'score': score
            })
        except Restaurant.DoesNotExist:
            continue

    return render(request, 'leaderboard.html', {'leaderboard': data})


