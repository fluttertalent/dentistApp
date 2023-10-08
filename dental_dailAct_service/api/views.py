from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework import generics
from doctors.models import Question
from .serializers import QuestionSerializer, AnswerSerializer
import json
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.decorators import api_view, authentication_classes, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.authtoken.models import Token
from doctors.models import Question, Answer, Score, Tip
from datetime import date
import random


@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # token, _ = Token.objects.get_or_create(user=user)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def signup_view(request):
    print(request.data)
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Create your views here.
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
class QuestionList(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get(self, request, *args, **kwargs):
        # Access request data
        query_params = request.query_params
        print(query_params)
        existing_answers = Answer.objects.filter(user_id=query_params['user_id'], pub_date=query_params['pub_date']).exists()
        if (existing_answers):
            return Response({'messsage':'You have already answered to daily questions'}, status=status.HTTP_404_NOT_FOUND)
        # Do something with the data        
        return super().get(request, *args, **kwargs)


@api_view(['POST'])
def save_answers(request):
    score = 0
    for element in request.data:
        serializer = AnswerSerializer(data=element)  # Set many=True to indicate bulk data
        if serializer.is_valid():
            serializer.save()
            score = score + int(element['value'])
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    scoreData = Score(user_id=element['user'], value=score, pub_date=date.today())
    scoreData.save()

    tips = Tip.objects.all()
    random_index = random.randint(0, len(tips) - 1)
    random_tip = tips[random_index]
    
    str = ""
    if(score <= 14):
        str = "Status is Low Risk."
    elif(score >=15 and score <= 28):
        str = "Status is Moderate Risk."
    else:
        str = "Status is High Risk."

    return Response({"title":"Successfully Answered!","content": "Your score is {score}.".format(score=score)+" "+str, "tip":random_tip.text}, status=status.HTTP_201_CREATED)
    


