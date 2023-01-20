from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import View, TemplateView
from IMDAPP.models import *
from django.contrib.auth import authenticate, login as loginuser,logout

#DashBord View

@method_decorator(login_required, name='dispatch')

class HomeView(View):
    template_name = "home.html"
    def get(self, request):        
        labels = []
        data = []        
        stockqueryset = Stock.objects.filter(is_deleted=False).order_by('-quantity')

        incount=Stock.objects.aggregate(s=Sum('quantity'))['s']

        incount1=Stock.objects.all().count()
        outcount1=SaleItem.objects.all().count()

        incount2=NonStock.objects.all().count()
        outcount2=NonSaleItem.objects.all().count()

        nonincount=NonStock.objects.aggregate(ns=Sum('quantity'))['ns']
        outcount=SaleItem.objects.aggregate(sb=Sum('quantity'))['sb']
        nonoutcount=NonSaleItem.objects.aggregate(sn=Sum('quantity'))['sn']

        print(outcount)
        for item in stockqueryset:
            labels.append(item.quantity)
            data.append(item.quantity)
        sales = SaleBill.objects.order_by('-time')[:3]
        inward = Stock.objects.order_by('-time')[:3]
        noninward = NonStock.objects.order_by('-time')[:3]
        nonsales = NonSaleBill.objects.order_by('-time')[:3]
        purchases = PurchaseBill.objects.order_by('-time')[:3]
        nonpurchases = NonPurchaseBill.objects.order_by('-time')[:3]
        context = {
            'labels'    : labels,
            'data'      : data,
            'sales'     : sales,
            'nonsales'     : nonsales,
            'inward'     : inward,
            'noninward'     : noninward,
            'purchases' : purchases,
            'nonpurchases' : nonpurchases,
            'incount' : incount,
            'incount1' : incount1,
            'outcount1' : outcount1,
            'incount2' : incount2,
            'outcount2' : outcount2,
            'outcount':outcount,
            'nonoutcount':nonoutcount,
            'nonincount':nonincount,
        }
        return render(request, self.template_name, context)


#Login

def login(request):

   if request.method =='GET':
       form = AuthenticationForm()
       context = {
           "form": form
       }
       return render(request, 'login.html', context=context)
   else:
       form = AuthenticationForm(data=request.POST)
       print(form.is_valid())
       if form.is_valid():
           username = form.cleaned_data.get('username')
           password = form.cleaned_data.get('password')
           user= authenticate(username=username, password=password)
           if user is not None:
               loginuser(request,user)
               return redirect('home')
           return render(request,'login.html')

       else:
           context = {
               "form": form
           }
           return render(request, 'login.html', context=context)

#Signout

def signout(request):
    logout(request)
    return redirect('login')

#AboutUs

class AboutView(TemplateView):
    template_name = "about.html"



