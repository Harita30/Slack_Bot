from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from slack_sdk import WebClient

SLACK_VERIFICATION_TOKEN = getattr(settings,'SLACK_VERIFICATION_TOKEN', None)
SLACK_BOT_USER_TOKEN = getattr(settings,'SLACK_BOT_USER_TOKEN',None)
Client = WebClient(token=SLACK_BOT_USER_TOKEN)
SLACK_BOT_USER_ID = getattr(settings,'SLACK_BOT_USER_ID',None)

class Events(APIView):
    def post(self,request,*args,**kwargs):
        
        slack_message = request.data
        
        if slack_message.get('token') != SLACK_VERIFICATION_TOKEN:
            return Response(status=status.HTTP_403_FORBIDDEN)
    
        if slack_message.get('type') == 'url_verification':
            return Response(data=slack_message,status=status.HTTP_200_OK)
        
        if 'event' in slack_message:
            
            event_msg = slack_message.get('event')
            
            if event_msg.get('subtype') == 'bot_message' or event_msg.get('user') == SLACK_BOT_USER_ID:
                return Response(status=status.HTTP_200_OK)
            
            user = event_msg.get('user')
            text = event_msg.get('text')
            channel = event_msg.get('channel')
            bot_text = 'Hi <@{}> :wave:'.format(user)
            
            if '<@{}>'.format(SLACK_BOT_USER_ID) in text:
                return Response(status=status.HTTP_200_OK)
            
            if 'hi' in text.lower():
                Client.chat_postMessage(channel=channel,text=bot_text)
                return Response(status=status.HTTP_200_OK)
        
        return Response(status=status.HTTP_200_OK)
        
# Create your views here.
