from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Restaurant, Review
from .serializers import ReviewSerializer
from .sentiments import analyze_sentiment
from .redis_utils import update_leaderboard, get_leaderboard

@api_view(['POST'])
def add_review(request):
    restaurant_id = request.data.get("restaurant_id")
    text = request.data.get("text")

    sentiment_score = analyze_sentiment(text)
    restaurant = Restaurant.objects.get(id=restaurant_id)
    review = Review.objects.create(restaurant=restaurant, text=text, sentiment_score=sentiment_score)

    update_leaderboard(restaurant_id, sentiment_score)

    return Response({"sentiment_score": sentiment_score})

@api_view(['GET'])
def leaderboard(request):
    data = get_leaderboard()
    return Response({restaurant_id.decode(): score for restaurant_id, score in data})


