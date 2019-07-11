from django.shortcuts import render
from django.http import HttpResponse
import requests as rq
import json
import main.models as models
from django.db.models import ObjectDoesNotExist
import config as Config
# Create your views here.

def catagorieslist(request):
    l=[]
    for i in models.catagory.objects.all():
        l.append({'id':i.id,'name':i.name,'description':'','img':{'url':''}})
    return HttpResponse(json.dumps(l,ensure_ascii=False))

def getCatagory(request):
    l=[]
    cname=request.GET.get('id',None)
    if cname==None:
        return HttpResponse("error")
    try:
        catagory=models.catagory.objects.get(id=cname)
        for i in catagory.spu_set.all():
            tmp={'name':i.name,'store':i.belong.name,'id':str(i.SPU_id)}
            for j in i.sku_set.all():
                if j.img_set.count()>0:
                    tmp['main_img_url']=Config.dname+j.img_set.all()[0].URL
            l.append(tmp)
    except ObjectDoesNotExist:
        l['error']='Catagory does not exist'
    return HttpResponse(json.dumps(l,ensure_ascii=False))

def SPUlist(request):
    l=[]
    for i in models.SPU.objects.all():
        minprice=999999999
        URL=''
        try:
            for j in i.sku_set.all():
                if j.img_set.count()>0:
                    URL=j.img_set.all()[0].URL
                    break
            URL=Config.dname+ URL
        except:
            pass
        for j in i.sku_set.all():
            minprice=min(minprice,j.price)
        l.append({'id':str(i.SPU_id),'name':i.name,'price':minprice,'stock':'','main_img_url':URL})
    return HttpResponse(json.dumps(l,ensure_ascii=False))

def getSPU(request,uuid):
    l=dict()
    try:
            
        spu=models.SPU.objects.get(SPU_id=uuid)
        l['id']=str(spu.SPU_id)
        l['name']=spu.name
        l['properties']=spu.description
        l['summary']=spu.description
        l['store']=spu.belong.name

        URL=''
        try:
            for j in spu.sku_set.all():
                if j.img_set.count()>0:
                    URL=j.img_set.all()[0].URL
                    break
            URL=Config.dname+URL
        except:
            pass
        l['main_img_url'] = URL
        l['SKU']=[]
        l['specification']={}
        minprice=999999999999
        for i in spu.sku_set.all():
            singleSKU={'SKU_id':str(i.SKU_id),'price':i.price,'stock':i.amount}
            minprice=min(minprice,i.price)

            optdict={}
            for j in i.options.all():
                optdict[j.belong.name]=j.name
                
                if (l['specification'].get(j.belong.name,None)==None):
                    l['specification'][j.belong.name]=[]
                # 根据SPU拥有的SKU来返回这个SPU可能有的option
                if j.name not in l['specification'][j.belong.name]:
                    l['specification'][j.belong.name].append(j.name)
            singleSKU['option']=optdict

            SKUimg=[]
            for j in i.img_set.all():
                SKUimg.append(Config.dname+j.URL)
            singleSKU['img_url']=SKUimg

            l['SKU'].append(singleSKU)
        l['price']=minprice
        
    except ObjectDoesNotExist:
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

def getBanner(request,id):
    l={'description':'首页轮播图','id':id}
    l['items']=[]
    l['items'].append({'key_word':'22203ac2-9257-4725-9980-9c7179dcd426','type':1,'img':{'url':Config.dname+'/static/banner/huaweiP30.png'}})
    return HttpResponse(json.dumps(l,ensure_ascii=False))

def getTheme(request):
    return HttpResponse("{}")
