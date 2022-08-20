from django.http.response import HttpResponse
from django.shortcuts import render
from .models import bill1, products,sales,bill
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import allowed_users,allowed_users1
from datetime import date,datetime,time
from machine.models import data
from django.db.models import Sum
import calendar
# Create your views here.
m=date.today()
n=date.today()
n = n.replace(day = calendar.monthrange(n.year, n.month)[1])
print(n)
s=time(22,00)
now = datetime.now()
now1=now.strftime("%H:%M:%S")
current_time = time(int(now1[0:2]),int(now1[3:5]),int(now1[7:]))

@login_required(login_url='login')
@allowed_users1
def bill_items(request):
    if request.method=='POST':
        if 'product' in request.POST:
            x=request.POST['product']
            y=request.POST['qty']
            try:
                z=products.objects.get(product=x)
                if(z.qty<int(y)):
                    messages.error(request,"Enough Quantity is not present in the store")
                else:
                    a=bill1(product=x,qty=int(y),price=int(y)*z.sell_price)
                    a.save()
                    z.qty-=int(y)
                    z.save()
            except:
                messages.error(request,"Product not available")
        if 'submit' in request.POST:
            bill50=bill1.objects.all()
            for x in bill50:
                c=products.objects.get(product=x.product)
                try:
                    y=sales.objects.get(product=x.product)
                    try:
                        a=bill.objects.get(date1=str(date.today()),product=c.unique)
                        print(a)
                        a.sales1+=x.qty
                        a.save()
                    except:
                        b=bill(date1=str(date.today()),product=c,sales1=x.qty)
                        print(b)
                        b.save()
                    y.qty+=x.qty   
                    y.save() 
                except:
                    z=sales(product=x.product,qty=x.qty,buy_price=c.buy_price*x.qty,sell_price=x.price)
                    try:
                        a=bill.objects.get(date1=str(date.today()))
                        print(a)
                        a.sales1+=x.qty
                        a.save()
                    except:
                        b=bill(date1=str(date.today()),product=c,sales1=x.qty)
                        print(b)
                        b.save()
                    z.save()
                x.delete()
            if m==n and current_time>=s:
                saved=bill.objects.all()
                for i in saved:
                    h=i.date1
                    newh=h[8:]+"-"+h[5:7]+"-"+h[:4]
                    c=data(date=newh,product=i.product.unique,sales=i.sales1)
                    c.save()
                    i.delete()
    bill2=bill1.objects.all()
    total=bill1.objects.aggregate(Sum('price'))  
    total1=total['price__sum']        
    context={
        'date':now,
        'bill':bill2,
        'total':total1
    }
    return render(request,'bill1.html',context)



@login_required(login_url='login')
@allowed_users
def update_products(request):
    if request.method=='POST':
        x=request.POST['product']
        try:
            pro_update=products.objects.get(product=x);
            pro_update.qty+=int(request.POST['qty'])
            pro_update.save()
            messages.success(request,"product updated successfully")
        except:
            messages.error(request,"Product not available")
    return render(request,'update_product.html')



@login_required(login_url='login')
@allowed_users
def add_products(request):
    if request.method=='POST':
        a=request.POST['product']
        b=request.POST['qty']
        c=request.POST['bprice']
        d=request.POST['sprice']
        e=request.POST['unique']
        try:
            products.objects.get(unique=int(e))
            messages.error(request,"Product is already available")
        except:
            try:
                print(1)
                products.objects.get(product=a)
                messages.error(request,"Product is already available")
            except:
                print(2)
                z=products(product=a,qty=int(b),buy_price=int(c),sell_price=int(d),unique=int(e))
                z.save()
                messages.success(request,"product added successfully")
    return render(request,'add_product.html')

@login_required(login_url='login')
@allowed_users
def delete_products(request):
    if request.method=='POST':
        x=request.POST['product']
        try:
            z=products.objects.get(product=x)
            z.delete()
            messages.success(request,"product deleted successfully")
        except:
            messages.error(request,"Product not available")
    return render(request,'delete_product.html')

@login_required(login_url='login')
@allowed_users
def Total_products(request):
    total=products.objects.all().order_by('unique')
    context={
        'products':total
    }
    return render(request,'total_products.html',context)


@login_required(login_url='login')
@allowed_users
def Total_sales(request):
    total=sales.objects.all()
    try:
        buytotal=sales.objects.aggregate(Sum('buy_price'))  
        selltotal=sales.objects.aggregate(Sum('sell_price'))  
        profit=selltotal['sell_price__sum']-buytotal['buy_price__sum']
    except:
        profit=0
    context={
        'products':total,
        'profit':profit
    }
    return render(request,'total_sales.html',context)

@login_required(login_url='login')
@allowed_users
def dashboard(request):
    return render(request,'dashboard.html')



