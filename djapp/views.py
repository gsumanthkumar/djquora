from ast import Delete
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout
from .models import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import F
# Create your views here.
@csrf_exempt
def signup(request):
    if not request.method == "POST":
        return JsonResponse({"status" : 400, "error": "Send a post request with valid parameters only."})
        
    username = request.POST["username"]
    password = request.POST["password"]

    usernames = list(User.objects.values_list('username', flat=True))
    if username in usernames:
        return JsonResponse({"status" : 400, "error": "Username is already taken by others!"})
    if len(password)>4:
        if len(username)>4:
            userdata = User(username=username)
            userdata.set_password(password)
            userdata.save()
            return JsonResponse({"status" : 200, "data": "Account Created Succesfully!"})
        else:
            return JsonResponse({"status" : 400, "error": "Username can't be less than 4 characters"})
    else:
        return JsonResponse({"status" : 400, "error": "Password length must be more than 4 characters"})

def get_user_token(user):
    token_instance,  created = Token.objects.get_or_create(user=user)
    return token_instance.key


@csrf_exempt
def signin(request):
    if not request.method == "POST":
        return JsonResponse({"status" : 400, "error": "Send a post request with valid parameters only."})
        
    username = request.POST["username"]
    password = request.POST["password"]
    try:
        user = User.objects.get(username=username)
        if user is None:
            return JsonResponse({ "status" : 400, "error": "There is no account with this email!"})
        if( user.check_password(password)):
            usr_dict = User.objects.filter(username=username).values().first()
            usr_dict.pop("password")
            if user != request.user:
                login(request, user)
                token = get_user_token(user)
                return JsonResponse({"status" : 200,"token": token,"status":"Logged in"})
            else:
                return JsonResponse({"status":200,"message":"User already logged in!"})
        else:
            return JsonResponse({"status":400,"status":"Invalid Login!"})
    except Exception as e:
        return JsonResponse({"400":"Invalid Login!"})

@csrf_exempt   
def signout(request):
    try:
        request.user.auth_token.delete()
        logout(request)
        return JsonResponse({ "status" : 200, "success" : "logout successful"})
    except Exception as e:
        return JsonResponse({ "status" : 400, "error": "Something Went wrong! Please try again later."})


class QuestionView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request):
        user = request.user
        description = request.POST["question"]
        try:
            question = Question(description=description,asked_by=user)
            question.save()
            return JsonResponse({"status":200,"Message":"Question posted!","qid": question.id})
        except Exception as e:
            return JsonResponse({"status":500,"Message":"Something Went wrong Please try again!"})

    def get(self,request):
        try:
            questions = Question.objects.filter(asked_by=request.user).values('id','description')
            return Response({"data":questions})
        except Exception as e:
            return JsonResponse({"status":500,"Message":"Something Went wrong Please try again!"})

    def delete(self,request,qid):
        try:
            Question.objects.filter(id=qid).delete()
            return Response({"Message":"Question Deleted!"})
        except Exception as e:
            return JsonResponse({"status":500,"Message":"Something Went wrong Please try again!"})
    
    def put(self,request,qid):
        try:
            description = request.POST["question"]
            Question.objects.filter(id=qid).update(description=description)
            return Response({"Message":"Question Edited!"})
        except Exception as e:
            return JsonResponse({"status":500,"Message":"Something Went wrong Please try again!"})

class AnswerView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request):
        user = request.user
        qid = request.POST["qid"]
        description = request.POST["answer"]
        question=Question.objects.get(id=qid)
        try:
            answer = Answer(question=question,description=description,answered_by=user)
            answer.save()
            return JsonResponse({"status":200,"Message":"Answer posted!","aid": answer.id,"qid": qid})
        except Exception as e:
            return JsonResponse({"status":500,"Message":"Something Went wrong Please try again!"})

    def get(self,request,aid):
        try:
            answers = Answer.objects.filter(id=aid).annotate(user=F('answered_by__username')).values('id','description','user')
            return Response({"data":answers})
        except Exception as e:
            return JsonResponse({"status":500,"Message":"Something Went wrong Please try again!"})

    def put(self,request,aid):
        description = request.POST["answer"]
        try:
            Answer.objects.filter(id=aid).update(description=description)
            return Response({"Message":"Answer Edited!"})
        except Exception as e:
            return JsonResponse({"status":500,"Message":"Something Went wrong Please try again!"})

    def delete(self,request,aid):
        try:
            Answer.objects.filter(id=aid).delete()
            return Response({"Message":"Answer Deleted!"})
        except Exception as e:
            return JsonResponse({"status":500,"Message":"Something Went wrong Please try again!"})

class QuestionAnswerView(APIView):
    permission_classes = [IsAuthenticated]
    

    def get(self,request,qid):
        try:
            answers = Answer.objects.filter(question__id=qid).annotate(user=F('answered_by__username')).values('id','description','user')
            return Response({"data":answers})
        except Exception as e:
            return JsonResponse({"status":500,"Message":"Something Went wrong Please try again!"})


class AnswerVoteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        user = request.user
        aid = request.POST["aid"]
        vote = request.POST["vote"]
        answer = Answer.objects.get(id=aid)
        try:
            votedata = Answervote(answer=answer,vote=vote,voted_by=user)
            votedata.save()
            return JsonResponse({"status":200,"Message":"Successfully Voted!"})
        except Exception as e:
            return JsonResponse({"status":500,"Message":"Something Went wrong Please try again!"})
    
    def get(self,request,aid):
        try:
            upvote = Answervote.objects.filter(answer__id=aid,vote=1).count()
            downvote = Answervote.objects.filter(answer__id=aid,vote=0).count()
            return JsonResponse({"status":200,"data":{"upvote":upvote,"downvote":downvote}})
        except Exception as e:
            return JsonResponse({"status":500,"Message":"Something Went wrong Please try again!"})
    
    def put(self,request,aid):
        user = request.user
        vote = request.POST["vote"]
        answer = Answer.objects.get(id=aid)
        try:
            Answervote.objects.filter(answer=answer,voted_by=user).update(vote=vote)
            return Response({"Message":"Vote Updated!"})
        except Exception as e:
            return JsonResponse({"status":500,"Message":"Something Went wrong Please try again!"})
    
    def delete(self,request,aid):
        user = request.user
        try:
            Answervote.objects.filter(answer__id=aid,voted_by=user).delete()
            return Response({"Message":"Vote Deleted!"})
        except Exception as e:
            return JsonResponse({"status":500,"Message":"Something Went wrong Please try again!"})

