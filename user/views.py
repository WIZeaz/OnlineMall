from django.shortcuts import render
from django.http import HttpResponse
import main.models as models
import requests as rq
import json
import main.config as Config
# Create your views here.

def login(request):
    if (request.method=='POST'):
        d=json.loads(request.body)
        code=d.get('code',None)
        if (code!=None):
            response=rq.get("https://api.weixin.qq.com/sns/jscode2session",params={'appid':Config.appId,'secret':Config.appSecret,'js_code':code,'grant_type':'authorization_code'})
            response.encoding='UTF-8'
            info=response.json()
            print(info)
            id=info.get('openid',None)
            if (id!=None):
                (user,exist)=models.customer.objects.get_or_create(openid=id)
                return HttpResponse(json.dumps({'token':str(user.uuid),'openid':info.get('openid','null')}))
    return HttpResponse("Error")

def verify(request):
    return HttpResponse(json.dumps({'isValid':True},ensure_ascii=False))

def getOrder(request):
    request.POST.get('token',None)
