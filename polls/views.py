from operator import length_hint
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render,get_object_or_404
from django.urls import reverse
from django.db import connection
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from .models import Question, Choice

def index(request):
    if request.user.is_authenticated:
        latest_question_list = Question.objects.order_by('-id')[:5]
        context = {'latest_question_list': latest_question_list}
        return render(request, 'polls/index.html', context)
    return render(request, 'polls/notloggedin.html', {'message': 'You are not logged in.'})

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

# Voting is allowed only for logged in users
def vote(request, question_id):
    if request.user.is_authenticated:
        question = get_object_or_404(Question, pk=question_id)
        try:
            selected_choice = question.choice_set.get(pk=request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            # Redisplay the question voting form.
            return render(request, 'polls/detail.html', {
                'question': question,
                'error_message': "You didn't select a choice.",
            })
        else:
            selected_choice.votes += 1
            selected_choice.save()
            return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    return render(request, 'polls/notloggedin.html', {'message': 'You are not logged in.'})

# !!!!! RISK 4: INJECTION !!!!!
def create(request):
    if request.user.is_authenticated:

        if request.method=='GET': 
            return render(request, 'polls/create.html')
        elif request.method=='POST':
            # Secure way:
            # question_text = request.POST['question_text']
            # question = Question(question_text=question_text)
            # question.save()
            with connection.cursor() as cursor:
                q_text = request.POST['question_text']
                sql = "INSERT INTO polls_question (question_text) VALUES ('%s')" % q_text
                cursor.execute(sql)
                question = Question.objects.get(pk=cursor.lastrowid)
                connection.close()
        
            return HttpResponseRedirect(reverse('polls:addchoices', args=(question.id,)))
    return render(request, 'polls/notloggedin.html', {'message': 'You are not logged in.'})

def addchoices(request, question_id):
    if request.user.is_authenticated:
        if request.method=='GET':
            question = get_object_or_404(Question, pk=question_id)
            return render(request, 'polls/addchoices.html', {'question': question})
        elif request.method=='POST':
            c_text1 = request.POST['choice_text1']
            c_text2 = request.POST['choice_text2']
            c_text3 = request.POST['choice_text3']
            q = Question.objects.get(pk=question_id)
            q.choice_set.create(choice_text=c_text1, votes=0)
            q.choice_set.create(choice_text=c_text2, votes=0)
            q.choice_set.create(choice_text=c_text3, votes=0)
            return HttpResponseRedirect(reverse('polls:index'))
    return render(request, 'polls/notloggedin.html', {'message': 'You are not logged in.'})

def home(request):
    return render(request, 'polls/home.html')

# Self-made signup method. All kinds of passwords are accepted
# !!!!! RISK NO 1: IDENTIFICATION AND AUTHETICATION FAILUERS !!!!!
def signup(request):
    if request.method=='GET':
        return render(request, 'polls/signup.html')
    elif request.method=='POST':
        username = request.POST['username']
        if User.objects.filter(username=username).exists() == False:
            psw = request.POST['password']
            psw_conf = request.POST['password-repeat']
            if psw == psw_conf:
                user = User.objects.create_user(username, 'email', psw)
                user.save()
                login(request, user)
                return HttpResponseRedirect(reverse('polls:home'))
            return HttpResponse('Not a match')
        return HttpResponse('Username is taken')

# !!!!! RISK NO 3: BROKEN ACCESS CONTROL !!!!! 
def pollusers(request):
    #if request.user.is_superuser:
        return render(request, 'polls/pollusers.html', {'pollusers':User.objects.all()})
    #return HttpResponse("You are not a superuser.")

def lastloggedin(request, polluser_id):
    if request.user.is_authenticated:
        polluser = request.user
        #polluser = User.objects.get(pk=polluser_id)
        return render(request, 'polls/lastloggedin.html', {'polluser':polluser})
    return render(request, 'polls/notloggedin.html', {'message': 'You are not logged in.'})
