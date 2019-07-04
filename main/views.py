from django.shortcuts import render
from django.http import HttpResponse
import requests as rq
import json
import main.models as models
from django.db.models import ObjectDoesNotExist
# Create your views here.

def login(request):
    if (request.method=='POST'):
        d=json.loads(request.body)
        code=d.get('code',None)
        if (code!=None):
            response=rq.get("https://api.weixin.qq.com/sns/jscode2session",params={'appid':'wx3776f53af9d3fba1','secret':'4c5a7e33f599f841fd2e685d448e2e68','js_code':code,'grant_type':'authorization_code'})
            response.encoding='UTF-8'
            info=response.json()
            id=info.get('id',None)
            if (id!=None):
                (user,exist)=models.customer.objects.get_or_create(openid=id)
                return HttpResponse(json.dumps({'token':user.uuid,'openid':info.get('openid','null')}))
    return HttpResponse("Error")

def catagorieslist(request):
    l=[]
    for i in models.catagory.objects.all():
        l.append(i.name)
    return HttpResponse(json.dumps(l,ensure_ascii=False))

def getCatagory(request,cname):
    l=[]
    try:
        catagory=models.catagory.objects.get(name=cname)
        for i in catagory.spu_set.all():
            l.append({'name':i.name,'store':i.belong.name})
    except ObjectDoesNotExist:
        l['error']='Catagory does not exist'
    return HttpResponse(json.dumps(l,ensure_ascii=False))

def SPUlist(request):
    l=[]
    for i in models.SPU.objects.all():
        l.append({'uuid':str(i.SPU_id),'name':i.name})
    return HttpResponse(json.dumps(l,ensure_ascii=False))

def getSPU(request,uuid):
    l=dict()
    try:
        spu=models.SPU.objects.get(SPU_id=uuid)
        l['SPU_id']=str(spu.SPU_id)
        l['name']=spu.name
        l['description']=spu.description
        l['store']=spu.belong.name
        l['SKU']=[]
        for i in spu.sku_set.all():
            singleSKU={'SKU_id':str(i.SKU_id),'price':i.price,'amount':i.amount}
            optdict={}
            for j in i.options.all():
                optdict[j.belong.name]=j.name
            singleSKU['option']=optdict
            l['SKU'].append(singleSKU)
    except:
        l['error']='SPU does not exist'
    return HttpResponse(json.dumps(l,ensure_ascii=False))
    

def storeList(request):
    l=[]
    for i in models.store.objects.all():
        l.append({'store_id':str(i.store_id),'name':i.name})
    return HttpResponse(json.dumps(l,ensure_ascii=False))

def getStore(request,id):
    l=dict()
    try:
        store=models.store.objects.get(store_id=id)
        l['store_id']=str(store.store_id)
        l['name']=store.name
        l['description']=store.description
        for i in store.spu_set.all():
            singleSKU={'SPU_id':str(i.SPU_id),'name':i.name}
    except:
        l['error']='Store does not exist'
    return HttpResponse(json.dumps(l,ensure_ascii=False))