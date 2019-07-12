from django.shortcuts import render
from django.http import HttpResponse
import main.models as models
import requests as rq
import json
import config as Config
import time
from django.db.models import ObjectDoesNotExist
import util
# Create your views here.

def login(request):
    if (request.method=='POST'):
        d=json.loads(request.body.decode('utf-8'))
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
    try:
        token=request.META.get("HTTP_TOKEN",None)
        user=models.customer.objects.get(uuid=token)
        return HttpResponse(json.dumps({'isValid':True},ensure_ascii=False))
    except:
        return HttpResponse(json.dumps({'isValid':False},ensure_ascii=False))
    

def orderList(request):
    try: 
        token=request.META.get("HTTP_TOKEN",None)

        page=int(request.GET.get('page',1))
        page-=1
        if (token==None):
            return HttpResponse("{'error':'Can not find token'}")
        user=models.customer.objects.get(uuid=token)

        print(page*Config.orderPerPage,(page+1)*Config.orderPerPage)
        l=dict(data=[])
        for i in user.order_set.all()[page*Config.orderPerPage:(page+1)*Config.orderPerPage]:
            tmp={'order_no':str(i.order_id),'id':str(i.order_id),'status':(i.status),'create_time':str(i.create_time),'payment_time':str(i.payment_time),'confirm_time':str(i.confirm_time),'total_price':i.price}
            try:
                tmp['snap_img']=Config.dname+i.items.all()[0].toSKU.img_set.all()[0].URL
            except:
                tmp['snap_img']=''
            tmp['snap_name']=str(i.items.all()[0].toSKU)
            tmp['total_count']=i.items.all()[0].amount
            l['data'].append(tmp)
        return HttpResponse(json.dumps(l,ensure_ascii=False))
    except:
        return HttpResponse("{'error':'something wrong happened'}")

def getOrder(request,order_id):
    try:
        order=models.order.objects.get(order_id=order_id)
        l=dict(status=order.status,total_price=order.price,create_time=str(order.create_time),order_no=order_id,snap_address=json.loads(order.snap_address),snap_items=[])
        for i in order.items.all():
            try:
                url=Config.dname+i.toSKU.img_set.all()[0].URL
            except:
                url=''
            l['snap_items'].append(dict(main_img_url=url,name=str(i.toSKU),price=i.toSKU.price,count=i.amount))
        return HttpResponse(json.dumps(l,ensure_ascii=False))
    except ObjectDoesNotExist:
        return HttpResponse('{"error":"Order does not exist"}')
    return HttpResponse('{"error":"unknown error"}')

def address(request):
    if(request.method == "GET"):
        try:
            uuid = request.META.get("HTTP_TOKEN")
            address=models.customer.objects.get(uuid=uuid).address
        except:
            address={'msg':'Address does not exist'}
        return HttpResponse(str(address))

    elif(request.method == "POST"):
        try:
            concat = request.POST
            postBody = str(request.body.decode('utf-8'), encoding = "utf-8") 
            uuid = request.META.get("HTTP_TOKEN")
            models.customer.objects.filter(uuid=uuid).update(address=postBody)
            return HttpResponse('success submit')   
            print(postBody)
            msg='success'
        except:
            msg='failed'
        return HttpResponse(msg)
    
def order(request):
    if (request.method=='POST'):
        info=json.loads(request.body.decode('utf-8'),encoding='utf-8')
        uuid = request.META.get("HTTP_TOKEN",None)
        try:
            user=models.customer.objects.get(uuid=uuid)
        except:
            return HttpResponse('{"error":"user does not exist"}')
        newOrder=models.order()
        newOrder.create_time=util.formatTime(time.localtime(time.time()))
        newOrder.status=2
        newOrder.belong=user
        newOrder.snap_address=user.address
        newOrder.price=0
        newOrder.save()
        totprice=0
        for i in info['products']:
            sku=models.SKU.objects.get(SKU_id=i['product_id'])
            models.order_item.objects.create(toOrder=newOrder,toSKU=sku,amount=i['count'])
            sku.amount-=i['count']
            sku.save()
            totprice+=sku.price
        newOrder.price=totprice
        newOrder.save()
        return HttpResponse(json.dumps({'order_id':str(newOrder.order_id),'pass':True},ensure_ascii=False))