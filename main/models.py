from django.db import models
import uuid
# Create your models here.

class option(models.Model):
    name=models.CharField('name',max_length=30)
    def __str__(self):
        return self.name
    

class speification(models.Model):
    name=models.CharField('name',max_length=30)
    def __str__(self):
        return self.name

class catagory(models.Model):
    name=models.CharField('name',max_length=30)
    def __str__(self):
        return self.name

class img(models.Model):
    URL=models.URLField('URL')

class SKU(models.Model):
    SKU_id=models.UUIDField('SKU_id',primary_key=True, default=uuid.uuid4, editable=False)
    price=models.IntegerField('price')
    amount=models.IntegerField('amount')
    spec=models.ManyToManyField(option)
    def __str__(self):
        return str(self.spec.all()[0].name)

class SPU(models.Model):
    SPU_id=models.UUIDField('SPU_id',primary_key=True, default=uuid.uuid4, editable=False)
    name=models.CharField('name',max_length=50)
    description=models.TextField('description')
    SKUs=models.ManyToManyField(SKU)
    imgs=models.ManyToManyField(img)
    catagorys=models.ManyToManyField(catagory)
    def __str__(self):
        return self.name

class store(models.Model):
    store_id=models.UUIDField('store_id',primary_key=True, default=uuid.uuid4, editable=False)
    name=models.CharField('name',max_length=50)
    description=models.TextField('description')
    SPUs=models.ManyToManyField(SPU)
    def __str__(self):
        return self.name

class order(models.Model):
    order_id=models.UUIDField('order_id',primary_key=True, default=uuid.uuid4, editable=False)
    create_time=models.TimeField('create_time')
    payment_time=models.TimeField('payment_time')
    confirm_time=models.TimeField('confirm_time')
    def __str__(self):
        return self.order_id

class customer(models.Model):
    uuid=models.UUIDField('customer_id',primary_key=True, default=uuid.uuid4, editable=False)
    password=models.CharField('password',max_length=50)
    nickname=models.CharField('nickname',max_length=50)
    address=models.CharField('address',max_length=100)
    phone_number=models.CharField('phone_number',max_length=20)
    def __str__(self):
        return str(self.uuid)+'#'+self.nickname