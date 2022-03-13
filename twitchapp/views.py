from email import message
from rest_framework.response import Response
from django import views
from django.shortcuts import render
from .serializers import TwitchSerializer
from .be_project import preprocess
import pandas as pd
from rest_framework import views

# def twitch(request):
#     l1=['what the hell was that','do it you wont','Fuck your couch!','No Spoils!','u look like u suck dick for money']
#     df=pd.DataFrame(l1,columns=['message'])
#     y_pred = preprocess(df)
#     print(y_pred)

class Twitch(views.APIView):
    def get(self, request):
        #print(request.data)
        message = request.data["message"]
        df=pd.DataFrame(message,columns=['message'])
        y_pred = preprocess(df)
        #results = TwitchSerializer(y_pred).data
        response_twitch = {"response":request.data}
        return Response(response_twitch)