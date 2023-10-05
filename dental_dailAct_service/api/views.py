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
from doctors.models import Question, Answer
from datetime import date


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
        existing_answers = Answer.objects.filter(user_id=query_params['user_id'], pub_date=date.today()).exists()
        if (existing_answers):
            return Response({'messsage':'You have already answered to daily questions'}, status=status.HTTP_404_NOT_FOUND)
        # Do something with the data        
        return super().get(request, *args, **kwargs)


@api_view(['POST'])
def save_answers(request):
    for element in request.data:
        serializer = AnswerSerializer(data=element)  # Set many=True to indicate bulk data
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
    

# def question_list(request):
#     if request.method == 'GET':
#         # Retrieve all questions
#         question_list = Question.objects.all()
#         # question_list = list(question_list.values())
#         # print(question_list)
#         # Create a dictionary of questions by kind
#         questions_by_kind = {}
#         for question in question_list:
#             if question.kind not in questions_by_kind:
#                 questions_by_kind[question.kind] = []
#             questions_by_kind[question.kind].append(question)

#         json_data = json.dumps({k: [q.text for q in v] for k, v in questions_by_kind.items()})        
#         print(json_data)
#         existing_answers = Answer.objects.filter(user_id=request.user.id, pub_date=date.today()).exists()
#         message = ''
#         if existing_answers:
#             message = 'You have already answered the questions for today.'

#         context = {
#             'questions_by_kind': json_data,
#             'existing_answers': existing_answers,
#             'message': message
#         }
#         # print(questions_by_kind)
#         return Response(context)

    # elif request.method == 'POST':
    #     form = QuestionForm(request.POST)
    #     if form.is_valid():
    #         for question_id, answer_value in form.cleaned_data.items():
    #             answer = Answer(user_id=request.user.id if request.user.is_authenticated else None, question_id=question_id, value=answer_value, pub_date=date.today())
    #             answer.save()
    #             message = "Successfully Answered"
    #             context = {
    #                 'message': message
    #             }
    #             return Response(context)
    #         # Redirect or perform further actions
    #     else:
    #         message = "Invalid post data"
    #         context = {
    #             'message': message
    #         }
    #         return Response(context)
