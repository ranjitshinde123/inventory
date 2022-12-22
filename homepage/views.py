from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from IMDAPP.models import *
from django.contrib.auth import authenticate, login as loginuser,logout



class HomeView(View):
    template_name = "home.html"
    def get(self, request):        
        labels = []
        data = []        
        stockqueryset = Stock.objects.filter(is_deleted=False).order_by('-quantity')
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
            'nonpurchases' : nonpurchases
        }
        return render(request, self.template_name, context)


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
           return render(request,'index.html')

       else:
           context = {
               "form": form
           }
           return render(request, 'login.html', context=context)

def signout(request):
    logout(request)
    return redirect('login')


class AboutView(TemplateView):
    template_name = "about.html"





