from django.db import models
import uuid
# Create your models here.

#TODO: specification may need to use one to many relationship, to prevent accident revise
class specification(models.Model):
    name=models.CharField('name',max_length=30)
    def __str__(self):
        return self.name

class option(models.Model):
    name=models.CharField('name',max_length=30)
    belong=models.ForeignKey(specification,on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    
class catagory(models.Model):
    name=models.CharField('name',max_length=30)
    def __str__(self):
        return self.name

class store(models.Model):
    store_id=models.UUIDField('store_id',primary_key=True, default=uuid.uuid4, editable=False)
    name=models.CharField('name',max_length=50)
    description=models.TextField('description')
    def __str__(self):
        return self.name

class SPU(models.Model):
    SPU_id=models.UUIDField('SPU_id',primary_key=True, default=uuid.uuid4, editable=False)
    name=models.CharField('name',max_length=50)
    description=models.TextField('description')
    catagories=models.ManyToManyField(catagory)
    spec=models.ManyToManyField(specification)
    belong=models.ForeignKey(store,on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class SKU(models.Model):
    SKU_id=models.UUIDField('SKU_id',primary_key=True, default=uuid.uuid4, editable=False)
    price=models.IntegerField('price')
    amount=models.IntegerField('amount')
    options=models.ManyToManyField(option)
    belong=models.ForeignKey(SPU,on_delete=models.CASCADE)
    def __str__(self):
        s=str(self.belong.name)
        for opt in self.options.all():
            s+="#"+opt.name
        return str(s)

class img(models.Model):
    URL=models.CharField('URL',max_length=200)
    belong=models.ForeignKey(SKU,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.belong)+'['+self.URL+']'


class customer(models.Model):
    uuid=models.UUIDField('customer_id',primary_key=True, default=uuid.uuid4, editable=False)
    nickname=models.CharField('nickname',max_length=20)
    openid=models.CharField('openid',max_length=100)
    address=models.TextField('address')
    phone_number=models.CharField('phone_number',max_length=20)
    def __str__(self):
        return str(self.uuid)+'#'+self.nickname

class order(models.Model):
    order_id=models.UUIDField('order_id',primary_key=True, default=uuid.uuid4, editable=False)
    price=models.IntegerField('price')
    create_time=models.DateTimeField('create_time')
    payment_time=models.DateTimeField('payment_time',null=True)
    confirm_time=models.DateTimeField('confirm_time',null=True)
    status=models.IntegerField('status') #1:待付款 2:已付款 3:已发货 4:已收货
    snap_address=models.TextField('snap_address')
    belong=models.ForeignKey(customer,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.order_id)

class order_item(models.Model):
    toOrder=models.ForeignKey(order,related_name='items',on_delete=models.CASCADE)
    toSKU=models.ForeignKey(SKU,on_delete=models.DO_NOTHING)
    amount=models.IntegerField('amount')
    def __str__(self):
        return str(self.toSKU.belong.name)+'#'+str(self.amount)

class item(models.Model):
    toSKU=models.ForeignKey(SKU,on_delete=models.CASCADE)
    toCustomer=models.ForeignKey(customer,related_name='cart',on_delete=models.CASCADE)
    number=models.IntegerField('number')
    def __str__(self):
        return str(self.toSKU.belong.name)+'#'+str(self.number)
