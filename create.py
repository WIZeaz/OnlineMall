import OnlineMall.main.models

t=SKU()
t.price=111
t.amount=111
t.options.add(*option.objects.all()[0])
t.save()
