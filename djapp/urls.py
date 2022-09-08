from django.urls import path
from . import views

urlpatterns = [
    path('home',views.home,name='home'),
    #Register
    path('signup/',views.signup,name='signup'),
    #Login
    path('signin/',views.signin,name='signin'),
    #Logout
    path('signout/',views.signout,name='signout'),
    #Post or Get Questions
    path('question/',views.QuestionView.as_view(),name='QuestionView'),
    #Put or Delete Questions
    path('question/<int:qid>/',views.QuestionView.as_view(),name='QuestionView'),
    #Post Answer
    path('answer/',views.AnswerView.as_view(),name='AnswerView'),
    #Put Answer or Delete Answer or Get Answer
    path('answer/<int:aid>/',views.AnswerView.as_view(),name='AnswerView'),
    #Get answers for particular question
    path('questionanswer/<int:qid>/',views.QuestionAnswerView.as_view(),name='QuestionAnswerview'),
    #Post Vote
    path('answervote/',views.AnswerVoteView.as_view(),name='AnswerVoteView'),
    #Get votes for answer or edit vote for answer
    path('answervote/<int:aid>/',views.AnswerVoteView.as_view(),name='AnswerVoteView'),
]