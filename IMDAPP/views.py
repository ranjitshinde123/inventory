import json
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponse, JsonResponse, request, Http404, HttpResponseRedirect, response
import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django_filters.views import FilterView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime
#Generic
from django.views.generic import (
    View,
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)
from .filters import StockFilter, NonStockFilter
from .models import (
    PurchaseBill,
    PurchaseItem,
    PurchaseBillDetails,
    SaleBill,
    SaleItem,
    SaleBillDetails, Stock, NonStock, Subcategory, Description, NonSubcategory, NonDescription, NonPurchaseBill,
    NonPurchaseBillDetails, NonPurchaseItem, Supplier, NonSaleBill, NonSaleItem, NonSaleBillDetails,
    trs, Category, NonCategory, InwardBillDetails, NonInwardBillDetails, Unit, Consumer, History, HNonStock
)
#form
from .forms import (
    StockForm,
    PurchaseItemFormset,
    PurchaseDetailsForm,
    SaleForm,
    SaleItemFormset,
     SubcategoryForm, CategoryForm, DescriptionForm, NonDescriptionForm, NonCategoryForm,
    NonSubcategoryForm, NonStockForm, NonPurchaseItemFormset, SelectSupplierForm,
    SupplierForm,
    NonPurchaseDetailsForm, NonSaleForm, NonSaleItemFormset, InwardDetailsForm,
    NonInwardDetailsForm, UnitForm, ConsumerForm, SelectConsumerForm,

)

# Create your views here
#Consumer

@method_decorator(login_required, name='dispatch')

class ConsumerListView(ListView):
    model = Consumer
    template_name = "suppliers/consumer_list.html"
    queryset = Consumer.objects.filter(is_deleted=False)
    paginate_by = 10


# used to add a new supplier

@method_decorator(login_required, name='dispatch')

class ConsumerCreateView(SuccessMessageMixin, CreateView):
    model = Consumer
    form_class = ConsumerForm

    success_url = '/inventory/consumers'
    success_message = "Supplier added successfully"
    template_name = "suppliers/edit_consumer.html"

    def post(self, request, *args, **kwargs):
        # response = super().post(request, *args, **kwargs)
        # print(response)
        body = request.POST.get('gstin')
        print('GST NUmber:',body)
        print(type(body))
        url = ("http://sheet.gstincheck.co.in/check/e33d005358c1ecc5bc0229186afa1adc/" + body)
        r = requests.get(url)
        a = r.json()
        e = a['flag']
        print(e)
        if e == True:
            b = a['data']['lgnm']
            c = a['data']['pradr']['adr']
            print('Name:', b)
            print("address:", c)
            if request.method == "POST":
                name = request.POST['name']
                phone = request.POST['phone']
                gstin = request.POST['gstin']
                email = request.POST['email']
                address = request.POST['address']
                print(name, phone, gstin, email, address)

                if name=="" and phone=="" and gstin=="" and email=="" and address=="":
                   breakpoint()
                else:
                    Consumer(name=name, phone=phone, address=address, email=email, gstin=gstin).save()
                # return HttpResponse(f"Name:{b} and Address:{c}")
            return render(request, 'suppliers/demo.html', {'b': b, 'c': c, 'd': body})
        else:
            print("GST Number is invalid Please Fill  valid GST Number")
            return HttpResponse("invalid GST Number")

        if not self.object:
            messages.info(request, 'Supplier already exist!!')
            return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'New Supplier'
        context['verify']='Verify'
        context["savebtn"] = 'Add Supplier'
        return context
    # used to update a supplier's info



@method_decorator(login_required, name='dispatch')

#update Supplier details

class ConsumerUpdateView(SuccessMessageMixin, UpdateView):
    model = Consumer
    form_class = ConsumerForm
    success_url = '/inventory/consumers'
    success_message = "Supplier details updated successfully."
    template_name = "suppliers/edit_consumer.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edit Supplier'
        context["savebtn"] = 'Save Changes'
        context["delbtn"] = 'Delete Supplier'
        return context


# used to delete a supplier
@method_decorator(login_required, name='dispatch')

class ConsumerDeleteView(View):
    template_name = "suppliers/delete_consumer.html"
    success_message = "Supplier deleted successfully."

    def get(self, request, pk):
        consumer = get_object_or_404(Consumer, pk=pk)
        return render(request, self.template_name, {'object': consumer})

    def post(self, request, pk):
        consumer = get_object_or_404(Consumer, pk=pk)
        consumer.is_deleted = True
        consumer.save()
        messages.success(request, self.success_message)
        return redirect('consumer-list')


# used to view a supplier's profile
@method_decorator(login_required, name='dispatch')
#show supplier details
class ConsumerView(View):
    def get(self, request,name):
        consumerobj = get_object_or_404(Consumer, name=name)
        bill_list = PurchaseBill.objects.filter(supplier=consumerobj)
        page = request.GET.get('page', 1)
        paginator = Paginator(bill_list, 10)
        try:
            bills = paginator.page(page)
        except PageNotAnInteger:
            bills = paginator.page(1)
        except EmptyPage:
            bills = paginator.page(paginator.num_pages)
        context = {
            'supplier': consumerobj,
            'bills': bills
        }
        return render(request, 'suppliers/edit_consumer.html', context)







#supplier List
@method_decorator(login_required, name='dispatch')

class SupplierListView(ListView):
    model = Supplier
    template_name = "suppliers/suppliers_list.html"
    queryset = Supplier.objects.filter(is_deleted=False)
    paginate_by = 10


# used to add a new supplier

class SupplierCreateView(SuccessMessageMixin, CreateView):
    model = Supplier
    form_class = SupplierForm
    success_url = '/inventory/suppliers'
    success_message = "Supplier added successfully."
    template_name = "suppliers/edit_supplier.html"

    def post(self, request, *args, **kwargs):
        # super().post() maybe raise a ValidationError if it is failure to save
        response = super().post(request, *args, **kwargs)
        # the below code is optional. django has responsed another erorr message
        if not self.object:
            messages.info(request, 'Supplier already exist!!')
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'New Supplier'
        context["savebtn"] = 'Add Supplier'
        return context




    # used to update a supplier's info

@method_decorator(login_required, name='dispatch')


class SupplierUpdateView(SuccessMessageMixin, UpdateView):
    model = Supplier
    form_class = SupplierForm
    success_url = '/inventory/suppliers'
    success_message = "Supplier details updated successfully."
    template_name = "suppliers/edit_supplier.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edit Supplier'
        context["savebtn"] = 'Save Changes'
        context["delbtn"] = 'Delete Supplier'
        return context


# used to delete a supplier

@method_decorator(login_required, name='dispatch')

class SupplierDeleteView(View):
    template_name = "suppliers/delete_supplier.html"
    success_message = "Supplier deleted successfully."

    def get(self, request, pk):
        supplier = get_object_or_404(Supplier, pk=pk)
        return render(request, self.template_name, {'object': supplier})

    def post(self, request, pk):
        supplier = get_object_or_404(Supplier, pk=pk)
        supplier.is_deleted = True
        supplier.save()
        messages.success(request, self.success_message)
        return redirect('suppliers-list')


# used to view a supplier's profile

@method_decorator(login_required, name='dispatch')

class SupplierView(View):
    def get(self, request,name):
        supplierobj = get_object_or_404(Supplier, name=name)
        bill_list = NonPurchaseBill.objects.filter(supplier=supplierobj)
        page = request.GET.get('page', 1)
        paginator = Paginator(bill_list, 10)
        try:
            bills = paginator.page(page)
        except PageNotAnInteger:
            bills = paginator.page(1)
        except EmptyPage:
            bills = paginator.page(paginator.num_pages)
        context = {
            'supplier': supplierobj,
            'bills': bills
        }
        return render(request, 'suppliers/supplier.html', context)


# shows the list of bills of all purchases
@method_decorator(login_required, name='dispatch')

class PurchaseView(ListView):
    model = PurchaseBill
    template_name = "purchases/purchases_list.html"
    context_object_name = 'bills'
    ordering = ['time']
    paginate_by = 10




# used to select the supplier

@method_decorator(login_required, name='dispatch')

class SelectConsumerView(View):
    form_class = SelectConsumerForm
    template_name = 'purchases/select_consumer.html'

    def get(self, request, *args, **kwargs):  # loads the form page
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):  # gets selected supplier and redirects to 'InwardCreateView' class
        form = self.form_class(request.POST)
        if form.is_valid():
            consumerid = request.POST.get("consumer")
            consumer = get_object_or_404(Consumer, id=consumerid)
            return redirect('new-purchase', consumer.pk)
        return render(request, self.template_name, {'form': form})
#




# used to delete a bill object

@method_decorator(login_required, name='dispatch')

class PurchaseCreateView(View):
    template_name = 'purchases/new_purchase.html'

    def get(self, request, pk):
        formset = PurchaseItemFormset(request.GET or None)  # renders an empty formset
        consumerobj = get_object_or_404(Consumer, pk=pk)  # gets the supplier object
        context = {
            'formset': formset,
            'consumer': consumerobj,
        }  # sends the supplier and formset as context
        return render(request, self.template_name, context)

    def post(self, request, pk):
        formset = PurchaseItemFormset(request.POST or None)  # recieves a post method for the formset
        consumerobj = get_object_or_404(Consumer, pk=pk)  # gets the supplier object
        if formset.is_valid():
            # saves bill
            billobj = PurchaseBill(
                consumer=consumerobj)  # a new object of class 'PurchaseBill' is created with supplier field set to 'supplierobj'
            billobj.save()  # saves object into the db
            # create bill details object
            billdetailsobj = PurchaseBillDetails(billno=billobj)
            billdetailsobj.save()
            for form in formset:  # for loop to save each individual form as its own object
                # false saves the item and links bill to the item
                billitem = form.save(commit=False)
                billitem.billno = billobj  # links the bill object to the items
                # gets the stock item
                stock = get_object_or_404(Stock, pk=billitem.stock.pk)

                # gets the item
                # calculates the total price
                billitem.totalprice = billitem.perprice * billitem.quantity
                # updates quantity in stock db
                stock.quantity += billitem.quantity  # updates quantity
                # saves bill item and stock
                stock.save()
                billitem.save()
            messages.success(request, "Item added successfully")
            return redirect('purchase-bill', billno=billobj.billno)
        formset = PurchaseItemFormset(request.GET or None)
        context = {
            'formset': formset,
            'consumer': consumerobj
        }
        return render(request, self.template_name, context)

@method_decorator(login_required, name='dispatch')

#deleted add item

class PurchaseDeleteView(SuccessMessageMixin, DeleteView):
    model = PurchaseBill
    template_name = "purchases/delete_purchase.html"
    success_url = '/inventory/purchases'

    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        items = PurchaseItem.objects.filter(billno=self.object.billno)
        for item in items:
            stock = get_object_or_404(Stock, name=item.stock.name)
            if stock.is_deleted == False:
                stock.quantity -= item.quantity
                stock.save()
        messages.success(self.request, " Bill deleted successfully")
        return super(PurchaseDeleteView, self).delete(*args, **kwargs)

@method_decorator(login_required, name='dispatch')

#List Non-consumable item

class NonPurchaseView(ListView):
    model = NonPurchaseBill
    template_name = "purchases/nonpurchases_list.html"
    context_object_name = 'bills'
    ordering = ['time']
    paginate_by = 10

@method_decorator(login_required, name='dispatch')

#select supplier

class SelectSupplierView(View):
    form_class = SelectSupplierForm
    template_name = 'purchases/select_supplier.html'

    def get(self, request, *args, **kwargs):  # loads the form page
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):  # gets selected supplier and redirects to 'PurchaseCreateView' class
        form = self.form_class(request.POST)
        if form.is_valid():
            supplierid = request.POST.get("supplier")
            supplier = get_object_or_404(Supplier, id=supplierid)
            return redirect('non-purchase', supplier.pk)
        return render(request, self.template_name, {'form': form})



@method_decorator(login_required, name='dispatch')

#create new non-consumable item

class NonPurchaseCreateView(View):
    template_name = 'purchases/non_purchase.html'

    def get(self, request, pk):
        formset = NonPurchaseItemFormset(request.GET or None)  # renders an empty formset
        supplierobj = get_object_or_404(Supplier, pk=pk)  # gets the supplier object
        context = {
            'formset': formset,
            'supplier': supplierobj,
        }  # sends the supplier and formset as context
        return render(request, self.template_name, context)

    def post(self, request, pk):
        formset = NonPurchaseItemFormset(request.POST or None)  # recieves a post method for the formset
        supplierobj = get_object_or_404(Supplier, pk=pk)  # gets the supplier object
        if formset.is_valid():
            # saves bill
            billobj = NonPurchaseBill(supplier=supplierobj)  # a new object of class 'PurchaseBill' is created with supplier field set to 'supplierobj'
            billobj.save()  # saves object into the db
            # create bill details object
            billdetailsobj = NonPurchaseBillDetails(billno=billobj)
            billdetailsobj.save()
            for form in formset:  # for loop to save each individual form as its own object
                # false saves the item and links bill to the item
                billitem = form.save(commit=False)
                billitem.billno = billobj  # links the bill object to the items
                # gets the stock item
                nonstock = get_object_or_404(NonStock,pk=billitem.nonstock.pk)

                # gets the item
                # calculates the total price
                billitem.totalprice = billitem.perprice * billitem.quantity
                # updates quantity in stock db
                nonstock.quantity += billitem.quantity  # updates quantity
                # saves bill item and stock
                nonstock.save()
                billitem.save()
            messages.success(request, "Item added successfully.")
            return redirect('nonpurchase-bill', billno=billobj.billno)
        formset = NonPurchaseItemFormset(request.GET or None)
        context = {
            'formset': formset,
            'supplier': supplierobj
        }
        return render(request, self.template_name, context)



# used to delete a bill object
@method_decorator(login_required, name='dispatch')

#deleted non-consumable item

class NonPurchaseDeleteView(SuccessMessageMixin, DeleteView):
    model = NonPurchaseBill
    template_name = "purchases/delete_nonpurchase.html"
    success_url = '/inventory/nonpurchases'

    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        items = NonPurchaseItem.objects.filter(billno=self.object.billno)
        for item in items:
            nonstock = get_object_or_404(NonStock, name=item.nonstock.name)
            if nonstock.is_deleted == False:
                nonstock.quantity -= item.quantity
                nonstock.save()
        messages.success(self.request, " Bill deleted successfully.")
        return super(NonPurchaseDeleteView, self).delete(*args, **kwargs)

#OutwardSlip(consumable,Non-consumable)

# @method_decorator(login_required, name='dispatch')

@login_required(login_url='login')

def outwardslip(request):
    if request.method == "POST":
        try:
            error = "no"
            if request.method == "POST":
                fromdate = datetime.datetime.strptime(request.POST.get('fromdate'), '%Y-%m-%d')
                todate = datetime.datetime.strptime(request.POST.get('todate'), '%Y-%m-%d')
                bills = SaleBill.objects.filter(Q(time__gte=fromdate) & Q(time__lte=todate))
                return render(request, 'sales/outwardslip.html', {"bills": bills})
            else:
                error = "yes"
                bills = SaleBill.objects.all()
                return render(request,'sales/outwardslip.html', {"bills": bills})

        except:
            error = "yes"
        return render(request, 'sales/outwardslip.html', locals())
    else:
        list = SaleBill.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(list, 10)

        try:
            bills = paginator.page(page)
        except PageNotAnInteger:
            bills = paginator.page(1)
        except EmptyPage:
            bills = paginator.page(paginator.num_pages)

        context = {
            'bills': bills,
        }
        return render(request,'sales/outwardslip.html', context)

# @method_decorator(login_required, name='dispatch')
@login_required(login_url='login')

def nonoutwardslip(request):
    if request.method == "POST":
        try:
            error = "no"
            if request.method == "POST":
                fromdate = datetime.datetime.strptime(request.POST.get('fromdate'), '%Y-%m-%d')
                todate = datetime.datetime.strptime(request.POST.get('todate'), '%Y-%m-%d')
                bills = NonSaleBill.objects.filter(Q(time__gte=fromdate) & Q(time__lte=todate))
                return render(request, 'sales/nonoutward_slip.html', {"bills": bills})
            else:
                error = "yes"
                bills = NonSaleBill.objects.all()
                return render(request, 'sales/nonoutward_slip.html', {"bills": bills})

        except:
            error = "yes"
        return render(request, 'sales/nonoutward_slip.html', locals())
    else:
        list = NonSaleBill.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(list, 10)

        try:
            bills = paginator.page(page)
        except PageNotAnInteger:
            bills = paginator.page(1)
        except EmptyPage:
            bills = paginator.page(paginator.num_pages)

        context = {
            'bills': bills,
        }
        return render(request, 'sales/nonoutward_slip.html', context)





#inward Slip(consumable,Non-Consumable)



#InwardSlip Consumable and Non-Consumable

@login_required(login_url='login')

def inwardslip(request):
    if request.method =="POST":
        try:
            error = "no"
            if request.method == "POST":
                fromdate = datetime.datetime.strptime(request.POST.get('fromdate'), '%Y-%m-%d')
                todate = datetime.datetime.strptime(request.POST.get('todate'), '%Y-%m-%d')
                bills = PurchaseBill.objects.filter(Q(time__gte=fromdate) & Q(time__lte=todate))
                return render(request, 'purchases/inwardslip.html', {"bills": bills})
            else:
                error = "yes"
                bills = PurchaseBill.objects.all()
                return render(request, 'purchases/inwardslip.html', {"bills": bills})

        except:
            error = "yes"
        return render(request, 'purchases/inwardslip.html', locals())
    else:
        list = PurchaseBill.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(list,10)

        try:
            bills = paginator.page(page)
        except PageNotAnInteger:
            bills = paginator.page(1)
        except EmptyPage:
            bills = paginator.page(paginator.num_pages)

        context = {
            'bills': bills,
        }
        return render(request, 'purchases/inwardslip.html', context)

@login_required(login_url='login')

def noninwardslip(request):
    if request.method =="POST":
        try:
            error = "no"
            if request.method == "POST":
                fromdate = datetime.datetime.strptime(request.POST.get('fromdate'), '%Y-%m-%d')
                todate = datetime.datetime.strptime(request.POST.get('todate'), '%Y-%m-%d')
                bills = NonPurchaseBill.objects.filter(Q(time__gte=fromdate) & Q(time__lte=todate))
                return render(request, 'purchases/noninwardslip.html', {"bills": bills})
            else:
                error = "yes"
                bills = NonPurchaseBill.objects.all()
                return render(request, 'purchases/noninwardslip.html', {"bills": bills})

        except:
            error = "yes"
        return render(request, 'purchases/noninwardslip.html', locals())
    else:
        list = NonPurchaseBill.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(list,10)

        try:
            bills = paginator.page(page)
        except PageNotAnInteger:
            bills = paginator.page(1)
        except EmptyPage:
            bills = paginator.page(paginator.num_pages)

        context = {
            'bills': bills,
        }
        return render(request, 'purchases/noninwardslip.html', context)



@login_required(login_url='login')

def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Expenses' +str(datetime.datetime.now()) + '.csv'
    writer = csv.writer(response)
    writer.writerow(['Billno', 'Date', 'From Whom Received','Item Name', 'Description Of Store', 'Quantity', 'Recd.By','Condition'])

    expenses = PurchaseItem.objects.all()

    for x in expenses:
        writer.writerow([x.billno.billno, x.billno.time,x.stock.name, x.stock.subcategory, x.stock.description,x.stock.quantity, x.stock.Mode_of_delivery, x.stock.condition ])
    return response

# @method_decorator(login_required, name='dispatch')
@login_required(login_url='login')

#Inward Non-consumable csv file

def nonexport_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Expenses' +str(datetime.datetime.now()) + '.csv'
    writer = csv.writer(response)
    writer.writerow(['Billno', 'Date', 'From Whom Received','Item Name', 'Description Of Store', 'Quantity', 'Recd.By','Condition'])

    expenses = NonSaleItem.objects.all()

    for x in expenses:
        writer.writerow([x.billno.billno, x.billno.time,x.nonstock.name, x.nonstock.subcategory, x.nonstock.description,x.nonstock.quantity, x.nonstock.Mode_of_delivery, x.nonstock.condition ])
    return response

#
# #outward
#
# @method_decorator(login_required, name='dispatch')

@login_required(login_url='login')

#Outward Consumable csv file

def outwardexport_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Expenses' +str(datetime.datetime.now()) + '.csv'
    writer = csv.writer(response)
    writer.writerow(['Billno', 'Customer','Item name','Description','Issued To','Quantity Sold', 'Date'])

    expenses = SaleItem.objects.all()

    for x in expenses:
        writer.writerow([x.billno.billno, x.billno.name, x.stock,x.stock.description,x.billno.issued_to, x.quantity, x.billno.time])
    return response

# @method_decorator(login_required, name='dispatch')

@login_required(login_url='login')

#outward Non-Consumable csv File

def outwardnonexport_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Expenses' +str(datetime.datetime.now()) + '.csv'
    writer = csv.writer(response)
    writer.writerow(['Billno', 'Customer','Item name','Description','Issued To','Quantity Sold', 'Date'])

    expenses = NonSaleItem.objects.all()

    for x in expenses:
        writer.writerow([x.billno.billno, x.billno.name, x.nonstock,x.nonstock.description,x.billno.issued_to, x.quantity,  x.billno.time])
    return response



# shows the list of bills of all sales

@method_decorator(login_required, name='dispatch')

class SaleView(ListView):
    model = SaleBill
    template_name = "sales/sales_list.html"
    context_object_name = 'bills'
    ordering = ['time']
    paginate_by = 10


# used to generate a bill object and save items
@method_decorator(login_required, name='dispatch')

class SaleCreateView(View):
    template_name = 'sales/new_sale.html'

    def get(self, request):
        form = SaleForm(request.GET or None)
        formset = SaleItemFormset(request.GET or None)  # renders an empty formset
        stocks = Stock.objects.filter(is_deleted=False)

        # purch/stocks = Purchase/Stock.objects.filter(is_deleted=False)
        context = {
            'form': form,
            'formset': formset,
            'stocks': stocks
        }
        return render(request, self.template_name, context)

    def post(self,request,*args, **kwargs):
        form = SaleForm(request.POST)
        formset = SaleItemFormset(request.POST)
        stocks = Stock.objects.filter(is_deleted=False)


        global c
        global d
        c = request.POST.get('mod')
        d = request.POST.get('v')
        print(c,d)

        # recieves a post method for the formset
        if form.is_valid() and formset.is_valid():
            # saves bill
            # billobj = form.save(commit=False)
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            address = form.cleaned_data['address']
            issued_to = form.cleaned_data['issued_to']
            if d == "OTHER":
                billobj = SaleBill( name=name,
                                 Mode_of_delivery=c, phone=phone, email=email,
                                address=address, issued_to=issued_to)
            else:
                billobj = SaleBill(name=name,
                                   Mode_of_delivery=d, phone=phone, email=email,
                                   address=address, issued_to=issued_to)
            billobj.save()
            # create bill details object
            billdetailsobj = SaleBillDetails(billno=billobj)
            billdetailsobj.save()
            try:
                for form in formset:  # for loop to save each individual form as its own object
                    # false saves the item and links bill to the item
                    billitem = form.save(commit=False)
                    billitem.billno = billobj  # links the bill object to the items
                    # gets the stock item
                    stock = get_object_or_404(Stock,pk=billitem.stock.pk)

                    # stock = get_object_or_404(Stock, name=billitem.stock.name
                    # billitem.totalprice = billitem.perprice * billitem.quantity
                    # updates quantity in stock db
                    stock.quantity -= billitem.quantity
                    # stock.description = billitem.description
                    # saves bill item and stock

                    stock.save()
                    billitem.save()

            except (ObjectDoesNotExist, MultipleObjectsReturned):
                pass

            messages.success(request, "Send item successfully")
            return redirect('sale-bill', billno=billobj.billno)
        form = SaleForm(request.GET or None)
        formset = SaleItemFormset(request.GET or None)
        stocks = Stock.objects.filter(is_deleted=False)

        context = {
            'form': form,
            'formset': formset,
            'stocks':stocks
         }
        return render(request, self.template_name, context,locals())



@method_decorator(login_required, name='dispatch')

#Deleted send  consumable item

class SaleDeleteView(SuccessMessageMixin, DeleteView):
    model = SaleBill
    template_name = "sales/delete_sale.html"
    success_url = '/inventory/sales'

    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        items = SaleItem.objects.filter(billno=self.object.billno)
        for item in items:
            stock = get_object_or_404(Stock, name=item.stock.name)
            if stock.is_deleted == False:
                stock.quantity += item.quantity
                stock.save()
        messages.success(self.request, "Bill deleted successfully")
        return super(SaleDeleteView, self).delete(*args, **kwargs)

@method_decorator(login_required, name='dispatch')

#Show view Bill

class SaleBillView(View):
    model = SaleBill
    template_name = "bill/sale_bill.html"
    bill_base = "bill/bill_base.html"

    def get(self, request, billno):
        context = {
            'bill': SaleBill.objects.get(billno=billno),
            'items': SaleItem.objects.filter(billno=billno),
            'billdetails': SaleBillDetails.objects.filter(billno=billno),
            'bill_base': self.bill_base,
        }
        return render(request, self.template_name, context)

    def post(self, request, billno):
        form = SaleDetailsForm(request.POST)
        if form.is_valid():
            billdetailsobj = SaleBillDetails.objects.get(billno=billno)
            billdetailsobj.save()
            messages.success(request, "Bill details updated successfully")
        context = {
            'bill': SaleBill.objects.get(billno=billno),
            'items': SaleItem.objects.filter(billno=billno),
            'billdetails': SaleBillDetails.objects.get(billno=billno),
            'bill_base': self.bill_base,
        }
        return render(request, self.template_name, context)



##nonconsumable send item

@method_decorator(login_required, name='dispatch')

class NonSaleView(ListView):
    model = NonSaleBill
    template_name = "sales/nonsales_list.html"
    context_object_name = 'bills'
    ordering = ['time']
    paginate_by = 10


# used to generate a bill object and save items

@method_decorator(login_required, name='dispatch')

class NonSaleCreateView(View):
    template_name = 'sales/new_nonsale.html'

    def get(self, request):
        form = NonSaleForm(request.GET or None)
        formset = NonSaleItemFormset(request.GET or None)  # renders an empty formset
        stocks = NonStock.objects.filter(is_deleted=False)

        # purch/stocks = Purchase/Stock.objects.filter(is_deleted=False)
        context = {
            'form': form,
            'formset': formset,
            'stocks': stocks
        }
        return render(request, self.template_name, context)

    def post(self,request,*args, **kwargs):
        form = NonSaleForm(request.POST)
        formset = NonSaleItemFormset(request.POST)
        stocks = NonStock.objects.filter(is_deleted=False)
        form = NonSaleForm(request.POST)

        global c
        global d
        c = request.POST.get('mod')
        d = request.POST.get('v')
        print(c, d)

        # recieves a post method for the formset
        if form.is_valid() and formset.is_valid():
            # saves bill
            # billobj = form.save(commit=False)
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            address = form.cleaned_data['address']
            issued_to = form.cleaned_data['issued_to']
            if d == "OTHER":
                billobj = NonSaleBill( name=name,
                                 Mode_of_delivery=c, phone=phone, email=email,
                                address=address, issued_to=issued_to)
            else:
                billobj = NonSaleBill(name=name,
                                   Mode_of_delivery=d, phone=phone, email=email,
                                   address=address, issued_to=issued_to)
            billobj.save()
            # create bill details object
            billdetailsobj = NonSaleBillDetails(billno=billobj)
            billdetailsobj.save()
            try:
                for form in formset:  # for loop to save each individual form as its own object
                    # false saves the item and links bill to the item
                    billitem = form.save(commit=False)
                    billitem.billno = billobj  # links the bill object to the items
                    # gets the stock item
                    nonstock = get_object_or_404(NonStock,pk=billitem.nonstock.pk)

                    # stock = get_object_or_404(Stock, name=billitem.stock.name
                    # billitem.totalprice = billitem.perprice * billitem.quantity
                    # updates quantity in stock db
                    nonstock.quantity -= billitem.quantity
                    # stock.description = billitem.description
                    # saves bill item and stock

                    nonstock.save()
                    billitem.save()

            except (ObjectDoesNotExist, MultipleObjectsReturned):
                pass

            messages.success(request, "Send item successfully")
            return redirect('nonsale-bill', billno=billobj.billno)
        form = NonSaleForm(request.GET or None)
        formset = NonSaleItemFormset(request.GET or None)
        stocks = NonStock.objects.filter(is_deleted=False)

        context = {
            'form': form,
            'formset': formset,
            'stocks':stocks
         }
        return render(request, self.template_name, context,locals())

@method_decorator(login_required, name='dispatch')

#Deleted Non-consumable item

class NonSaleDeleteView(SuccessMessageMixin, DeleteView):
    model = NonSaleBill
    template_name = "sales/delete_nonsale.html"
    success_url = '/inventory/nonsales'

    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        items = NonSaleItem.objects.filter(billno=self.object.billno)
        for item in items:
            nonstock = get_object_or_404(NonStock, name=item.nonstock.name)
            if nonstock.is_deleted == False:
                nonstock.quantity += item.quantity
                nonstock.save()
        messages.success(self.request, "Bill deleted successfully")
        return super(NonSaleDeleteView, self).delete(*args, **kwargs)

@method_decorator(login_required, name='dispatch')
#view  non-comsumable bill
class NonSaleBillView(View):
    model = NonSaleBill
    template_name = "bill/nonsale_bill.html"
    bill_base = "bill/bill_base.html"

    def get(self, request, billno):
        context = {
            'bill': NonSaleBill.objects.get(billno=billno),
            'items': NonSaleItem.objects.filter(billno=billno),
            'billdetails': NonSaleBillDetails.objects.get(billno=billno),
            'bill_base': self.bill_base,
        }
        return render(request, self.template_name, context)

    def post(self, request, billno):
        form = NonSaleDetailsForm(request.POST)
        if form.is_valid():
            billdetailsobj = NonSaleBillDetails.objects.get(billno=billno)
            billdetailsobj.save()
            messages.success(request, "Bill details updated successfully")
        context = {
            'bill': NonSaleBill.objects.get(billno=billno),
            'items': NonSaleItem.objects.filter(billno=billno),
            'billdetails': SaleBillDetails.objects.get(billno=billno),
            'bill_base': self.bill_base,
        }
        return render(request, self.template_name, context)

# used to delete a bill object

# used to display the purchase bill object

@method_decorator(login_required, name='dispatch')

#Add consumable bill  view

class PurchaseBillView(View):
    model = PurchaseBill
    template_name = "bill/purchase_bill.html"
    bill_base = "bill/bill_base.html"

    def get(self, request, billno):
        context = {
            'bill': PurchaseBill.objects.get(billno=billno),
            'items': PurchaseItem.objects.filter(billno=billno),
            'billdetails': PurchaseBillDetails.objects.filter(billno=billno),
            'bill_base': self.bill_base,
        }
        return render(request, self.template_name, context)

    def post(self, request, billno):
        form = PurchaseDetailsForm(request.POST)
        if form.is_valid():
            billdetailsobj = PurchaseBillDetails.objects.get(billno=billno)
            billdetailsobj.save()
            messages.success(request, "Bill details updated successfully")
        context = {
            'bill': PurchaseBill.objects.get(billno=billno),
            'items': PurchaseItem.objects.filter(billno=billno),
            'billdetails': PurchaseBillDetails.objects.get(billno=billno),
            'bill_base': self.bill_base,
        }

        return render(request, self.template_name, context)

@method_decorator(login_required, name='dispatch')

class NonPurchaseBillView(View):
    model = NonPurchaseBill
    template_name = "bill/nonpurchase_bill.html"
    bill_base = "bill/bill_base.html"

    def get(self, request, billno):
        context = {
            'bill': NonPurchaseBill.objects.get(billno=billno),
            'items': NonPurchaseItem.objects.filter(billno=billno),
            'billdetails': NonPurchaseBillDetails.objects.filter(billno=billno),
            'bill_base': self.bill_base,
        }
        return render(request, self.template_name, context)

    def post(self, request, billno):
        form = NonPurchaseDetailsForm(request.POST)
        if form.is_valid():
            billdetailsobj = NonPurchaseBillDetails.objects.get(billno=billno)

            billdetailsobj.save()
            messages.success(request, "Bill details updated successfully")
        context = {
            'bill': NonPurchaseBill.objects.get(billno=billno),
            'items': NonPurchaseItem.objects.filter(billno=billno),
            'billdetails': NonPurchaseBillDetails.objects.get(billno=billno),
            'bill_base': self.bill_base,
        }

        return render(request, self.template_name, context)





@method_decorator(login_required, name='dispatch')

# Consumable List

class StockListView(FilterView):
    filterset_class = StockFilter
    queryset = Stock.objects.filter(is_deleted=False).order_by('-quantity')
    template_name = 'inventory/inventory.html'
    paginate_by = 10



# class StockCreateView(SuccessMessageMixin, CreateView):
#     model = Stock
#     form_class = StockForm
#     template_name = "inventory/edit_stock.html"
#     success_url = '/inventory'
#     success_message = "Stock added successfully"
#
#     def get_context_data(self, **kwargs):  # used to send additional context
#         context = super().get_context_data(**kwargs)
#         context["title"] = 'New Stock'
#         context["savebtn"] = 'Add To Stock'
#
#         return context
@method_decorator(login_required, name='dispatch')

# class StockCreateView(View):
#     model = Stock
#     form_class = StockForm
#     template_name = "inventory/edit_stock.html"
#     # success_url = 'inward-bill'
#     # success_message = "Stock has been created successfully"
#
#     def get(self, request):
#         form = StockForm(request.GET or None)
#         # formset = InwardItemFormset(request.GET or None)  # renders an empty formset
#         stocks = Stock.objects.filter(is_deleted=False)
#
#         # purch/stocks = Purchase/Stock.objects.filter(is_deleted=False)
#         context = {
#             'form': form,
#             # 'formset': formset,
#             'stocks': stocks
#         }
#         return render(request, self.template_name, context)
#
#     def post(self, request, *args, **kwargs):
#         form = StockForm(request.POST)
#         # formset = InwardItemFormset(request.POST)
#         # gets the supplier object
#
#         # recieves a post method for the formset
#         if form.is_valid() :
#             form = StockForm(request.POST)
#             # billdetailsobj = PurchaseBillDetails.objects.get(billno=billno)
#
#             # saves bill
#             billobj = form.save(commit=False)
#             billobj.save()
#             # create bill details object
#             billdetailsobj = InwardBillDetails(billno=billobj)
#             billdetailsobj.save()
#             try:
#                 for form in form:
#
#                     form = StockForm(request.POST)
#
#                     billitem = form.save(commit=False)
#
#                     billitem.billno = billobj  # links the bill object to the items
#                     # gets the stock item
#                     stock = get_object_or_404(Stock, name=billitem.name)##change
#                     # print(request.GET)
#                     # stock = get_object_or_404(Stock, name=billitem.stock.subcategory)
#                     # stock.quantity += billitem.quantity
#
#                     totalprice = billitem.perprice * billitem.quantity
#                     # print(billitem.totalprice)
#                     # # updates quantity in stock db
#
#                     # saves bill item and stock
#
#                     # stock.save()
#                     # billitem.save()
#
#             except (ObjectDoesNotExist, MultipleObjectsReturned):
#                 pass
#
#             messages.success(request, "Received item successfully")
#             return redirect('inward-bill', billno=billobj.billno)
#         form = StockForm(request.GET or None)
#         inwarditems = InwardBillDetails(request.GET or None)
#
#         # formset = InwardItemFormset(request.GET or None)
#         context = {
#             'form': form,
#             'inwarditems':inwarditems,
#             # 'formset': formset,
#         }
#         return render(request, self.template_name, context, locals())
#

#add new stock in inventory

class StockCreateView(View):
    model = Stock
    form_class = StockForm
    template_name = "inventory/edit_stock.html"
    # success_url = 'inward-bill'
    # success_message = "Stock has been created successfully"

    def get(self, request):
        form = StockForm(request.GET or None)
        # formset = InwardItemFormset(request.GET or None)  # renders an empty formset
        stocks = Stock.objects.filter(is_deleted=False)

        # purch/stocks = Purchase/Stock.objects.filter(is_deleted=False)
        context = {
            'form': form,
            # 'formset': formset,
            'stocks': stocks
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = StockForm(request.POST)
        form1 = SelectConsumerForm(request.POST)
        global c
        global d
        c = request.POST.get('mod')
        d = request.POST.get('v')
        print(c,d)
        if  form.is_valid() :
            category = form.cleaned_data.get('category')
            subcategory = form.cleaned_data['subcategory']
            description = form.cleaned_data['description']
            name = form.cleaned_data['name']
            unit = form.cleaned_data['unit']
            label_code = form.cleaned_data['label_code']
            condition = form.cleaned_data['condition']
            quantity = form.cleaned_data['quantity']
            perprice = form.cleaned_data['perprice']
            totalprice = quantity * perprice
            print(category, subcategory)
            if Stock.objects.filter(category=category, subcategory=subcategory, description=description).exists():
                messages.info(
                    request, 'Add stock from here')
                return redirect('select-consumer')
            else:
                if d == "OTHER":
                    billobj = Stock(category=category, subcategory=subcategory, description=description, name=name,
                                    unit=unit, Mode_of_delivery=c, label_code=label_code, condition=condition,
                                    quantity=quantity, perprice=perprice,totalprice=totalprice)
                    History(category=category, subcategory=subcategory, description=description, name=name,
                            unit=unit, Mode_of_delivery=c, label_code=label_code, condition=condition,
                            quantity=quantity, perprice=perprice, totalprice=totalprice).save()
                else:
                    billobj = Stock(category=category, subcategory=subcategory, description=description, name=name,
                                    unit=unit, Mode_of_delivery=d, label_code=label_code, condition=condition,
                                    quantity=quantity, perprice=perprice,totalprice=totalprice)
                    History(category=category, subcategory=subcategory, description=description, name=name,
                            unit=unit, Mode_of_delivery=d, label_code=label_code, condition=condition,
                            quantity=quantity, perprice=perprice, totalprice=totalprice).save()


            billobj.save()
            billdetailsobj = InwardBillDetails(billno=billobj)
            billdetailsobj.save()
            messages.success(request,"Received item successfully")
            return redirect('inward-bill', billno=billobj.billno)
            form = StockForm(request.GET or None)
            inwarditems = InwardBillDetails(request.GET or None)
            context = {
                'form': form,
                'inwarditems': inwarditems,
            }
            return render(request, self.template_name,context, locals())




@method_decorator(login_required, name='dispatch')

# Update stock

class StockUpdateView(SuccessMessageMixin, UpdateView):  # updateview class to edit stock, mixin used to display message
    model = Stock  # setting 'Stock' model as model
    form_class = StockForm  # setting 'StockForm' form as form
    template_name = "inventory/edit_stock.html"  # 'edit_stock.html' used as the template
    success_url = '/inventory'  # redirects to 'inventory' page in the url after submitting the form
    success_message = "Stock updated successfully"  # displays message when form is submitted

    def get_context_data(self, **kwargs):  # used to send additional context
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edit Stock'
        context["savebtn"] = 'Update Stock'
        context["delbtn"] = 'Delete Stock'

        return context

@method_decorator(login_required, name='dispatch')

class StockDeleteView(View):  # view class to delete stock
    template_name = "inventory/delete_stock.html"  # 'delete_stock.html' used as the template
    success_message = "Item deleted successfully"  # displays message when form is submitted

    def get(self, request, pk):
        stock = get_object_or_404(Stock, pk=pk)
        return render(request, self.template_name, {'object': stock})

    def post(self, request, pk):
        stock = get_object_or_404(Stock, pk=pk)
        stock.is_deleted = True
        stock.save()
        messages.success(request, self.success_message)
        return redirect('inventory')

@method_decorator(login_required, name='dispatch')

class StockBillView(View):
    model = Stock
    template_name = "bill/inward_bill.html"
    bill_base = "bill/bill_base.html"

    def get(self, request, billno):
        context = {
            'bill': Stock.objects.get(billno=billno),
            'items': Stock.objects.filter(billno=billno),
            'billdetails': InwardBillDetails.objects.get(billno=billno),
            'bill_base': self.bill_base,
        }
        return render(request, self.template_name, context)

    def post(self, request, billno):
        form = InwardDetailsForm(request.POST)
        if form.is_valid():
            billdetailsobj = InwardBillDetails.objects.get(billno=billno)
            billdetailsobj.save()
            messages.success(request, "Bill details modified successfully")
        context = {
            'bill': Stock.objects.get(billno=billno),
            'items': Stock.objects.filter(billno=billno),
            'billdetails': InwardBillDetails.objects.get(billno=billno),
            'bill_base': self.bill_base,
        }
        return render(request, self.template_name, context)

class HStockBillView(View):
    model = History
    template_name = "bill/inwardbillhistory.html"
    bill_base = "bill/bill_base.html"

    def get(self, request, billno):
        context = {
            'bill': History.objects.get(billno=billno),
            'items': History.objects.filter(billno=billno),
            'bill_base': self.bill_base,
        }
        return render(request, self.template_name, context)


class NONHStockBillView(View):
    model = HNonStock
    template_name = "bill/noninwardbillhistory.html"
    bill_base = "bill/bill_base.html"

    def get(self, request, billno):
        context = {
            'bill': HNonStock.objects.get(billno=billno),
            'items': HNonStock.objects.filter(billno=billno),
            'bill_base': self.bill_base,
        }
        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')

class StockView(View):
    def get(self, request, name):
        stockobj = get_object_or_404(Stock, name=name)
        # stock = Stock.objects.get(stock=stockobj)

        context = {
            'stock': stockobj,
        }
        return render(request, 'inventory/stockdetails.html', context)


@method_decorator(login_required, name='dispatch')

#Non-consumable List

class NonStockListView(FilterView):
    filterset_class = NonStockFilter
    queryset = NonStock.objects.filter(is_deleted=False).order_by('-quantity')
    template_name = 'inventory/nonconsumable.html'
    paginate_by = 10


@method_decorator(login_required, name='dispatch')
#add new non-consumable item

class NonStockCreateView(View):
    model = NonStock
    form_class = NonStockForm
    template_name = "inventory/edit_nonstock.html"
    # success_url = 'inward-bill'
    # success_message = "Stock has been created successfully"

    def get(self, request):
        form = NonStockForm(request.GET or None)
        # formset = InwardItemFormset(request.GET or None)  # renders an empty formset
        stocks = NonStock.objects.filter(is_deleted=False)

        # purch/stocks = Purchase/Stock.objects.filter(is_deleted=False)
        context = {
            'form': form,
            # 'formset': formset,
            'stocks': stocks
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = NonStockForm(request.POST)
        form1 = SelectSupplierForm(request.POST)
        global c
        global d
        c = request.POST.get('mod')
        d = request.POST.get('v')
        print(c,d)
        if  form.is_valid() :
            category = form.cleaned_data.get('category')
            subcategory = form.cleaned_data['subcategory']
            description = form.cleaned_data['description']
            name = form.cleaned_data['name']
            unit = form.cleaned_data['unit']
            label_code = form.cleaned_data['label_code']
            condition = form.cleaned_data['condition']
            quantity = form.cleaned_data['quantity']
            perprice = form.cleaned_data['perprice']
            totalprice = quantity * perprice

            print(category, subcategory)
            if NonStock.objects.filter(category=category, subcategory=subcategory, description=description).exists():
                messages.info(
                    request, 'Add stock from here')
                return redirect('select-supplier')
            else:
                if d == "OTHER":
                    billobj = NonStock(category=category, subcategory=subcategory, description=description, name=name,
                                    unit=unit, Mode_of_delivery=c, label_code=label_code, condition=condition,
                                    quantity=quantity, perprice=perprice,totalprice=totalprice)
                    HNonStock(category=category, subcategory=subcategory, description=description, name=name,
                              unit=unit, Mode_of_delivery=c, label_code=label_code, condition=condition,
                              quantity=quantity, perprice=perprice, totalprice=totalprice).save()
                else:
                    billobj = NonStock(category=category, subcategory=subcategory, description=description, name=name,
                                    unit=unit, Mode_of_delivery=d, label_code=label_code, condition=condition,
                                    quantity=quantity, perprice=perprice,totalprice=totalprice)
                    HNonStock(category=category, subcategory=subcategory, description=description, name=name,
                              unit=unit, Mode_of_delivery=d, label_code=label_code, condition=condition,
                              quantity=quantity, perprice=perprice, totalprice=totalprice).save()

            billobj.save()
            billdetailsobj = NonInwardBillDetails(billno=billobj)
            billdetailsobj.save()
            messages.success(request,"Received item successfully")
            return redirect('inwardnc-bill', billno=billobj.billno)
            form = NonStockForm(request.GET or None)
            inwarditems = NonInwardBillDetails(request.GET or None)
            context = {
                'form': form,
                'inwarditems': inwarditems,
            }
            return render(request, self.template_name,context, locals())


@method_decorator(login_required, name='dispatch')

class NonStockBillView(View):
    model = NonStock
    template_name = "bill/inwardnc_bill.html"
    bill_base = "bill/bill_base.html"

    def get(self, request, billno):
        context = {
            'bill': NonStock.objects.get(billno=billno),
            'items': NonStock.objects.filter(billno=billno),
            'billdetails': NonInwardBillDetails.objects.get(billno=billno),
            'bill_base': self.bill_base,
        }
        return render(request, self.template_name, context)

    def post(self, request, billno):
        form = NonInwardDetailsForm(request.POST)
        if form.is_valid():
            billdetailsobj = NonInwardBillDetails.objects.get(billno=billno)
            billdetailsobj.save()
            messages.success(request, "Bill details have been modified successfully")
        context = {
            'bill': NonStock.objects.get(billno=billno),
            'items': NonStock.objects.filter(billno=billno),
            'billdetails': NonInwardBillDetails.objects.get(billno=billno),
            'bill_base': self.bill_base,
        }
        return render(request, self.template_name, context)
@method_decorator(login_required, name='dispatch')

class NonStockView(View):
    def get(self, request, name):
        stockobj = get_object_or_404(NonStock, name=name)
        # stock = Stock.objects.get(stock=stockobj)

        context = {
            'stock': stockobj,
        }
        return render(request, 'inventory/stockdetails.html', context)


@method_decorator(login_required, name='dispatch')

class NonStockUpdateView(SuccessMessageMixin, UpdateView):  # updateview class to edit stock, mixin used to display message
    model = NonStock  # setting 'Stock' model as model
    form_class = NonStockForm  # setting 'StockForm' form as form
    template_name = "inventory/edit_nonstock.html"  # 'edit_stock.html' used as the template
    success_url = '/inventory/nonconsumable'  # redirects to 'inventory' page in the url after submitting the form
    success_message = "Item updated successfully"  # displays message when form is submitted

    def get_context_data(self, **kwargs):  # used to send additional context
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edit Stock'
        context["savebtn"] = 'Update Stock'
        context["delbtn"] = 'Delete Stock'

        return context

@method_decorator(login_required, name='dispatch')

class NonStockDeleteView(View):  # view class to delete stock
    template_name = "inventory/delete_nonstock.html"  # 'delete_stock.html' used as the template
    success_message = "Item deleted successfully."  # displays message when form is submitted

    def get(self, request, pk):
        nonstock = get_object_or_404(NonStock, pk=pk)
        return render(request, self.template_name, {'object': nonstock})

    def post(self, request, pk):
        nonstock = get_object_or_404(NonStock, pk=pk)
        nonstock.is_deleted = True
        nonstock.save()
        messages.success(request, self.success_message)
        return redirect('nonconsumable')

@method_decorator(login_required, name='dispatch')

class NonStockView(View):
    def get(self, request, name):
        stockobj = get_object_or_404(NonStock, name=name)
        context = {
            'stock': stockobj,
        }
        return render(request, 'inventory/nonstockdetails.html', context)




# @method_decorator(login_required, name='dispatch')
@login_required(login_url='login')

#Add New Category

def addcategory(request):
    form=CategoryForm(request.POST)
    try:
        error = "no"
        if form.is_valid():
            category = form.cleaned_data['category']
            if Category.objects.filter(category=category).exists():
                messages.info(
                    request, 'Category already exists! ')
                return redirect('addcategory')
            form.save()
        else:
            category = form.save(commit=False)
            category.save()
            error = "yes"
    except:
        error = "yes"
    return render(request, "Master/addcategory.html", locals())



# @method_decorator(login_required, name='dispatch')
@login_required(login_url='login')

#Add new Unit

def addunit(request):
    form=UnitForm(request.POST)
    try:
        error = "no"
        if form.is_valid():
            unit = form.cleaned_data['unit']
            if Unit.objects.filter(unit=unit).exists():
                messages.info(
                    request, 'Unit already exists! ')
                return redirect('add-unit')
            form.save()
        else:
            unit = form.save(commit=False)
            unit.save()
            error = "yes"
    except:
        error = "yes"
    return render(request, "Master/add_unit.html", locals())

# @method_decorator(login_required, name='dispatch')
@login_required(login_url='login')

# Add New SubCategory

def addsubcategory(request):
    form=SubcategoryForm(request.POST or None)
    try:
        error = "no"
        if form.is_valid():
            form.save()
        else:
            error = "yes"
    except:
        error = "yes"
    return render(request,"Master/addsubcategory.html",locals())

# @method_decorator(login_required, name='dispatch')
@login_required(login_url='login')

#Add New Description

def adddescription(request):
    form=DescriptionForm(request.POST or None)
    try:
        error = "no"
        if form.is_valid():
            form.save()
        else:
            error = "yes"
    except:
        error = "yes"
    return render(request, "Master/adddescription.html", locals())
# @method_decorator(login_required, name='dispatch')
@login_required(login_url='login')

# Add New Non-Consumable Category

def addnoncategory(request):
    form=NonCategoryForm(request.POST)
    try:
        error = "no"
        if form.is_valid():
            category = form.cleaned_data['category']
            if NonCategory.objects.filter(category=category).exists():
                messages.info(
                    request, 'Category already exists! ')
                return redirect('addnoncategory')
            form.save()
        else:
            category = form.save(commit=False)
            category.save()
            error = "yes"
    except:
        error = "yes"
    return render(request, "Master/addnoncategory.html", locals())
# @method_decorator(login_required, name='dispatch')
@login_required(login_url='login')

# Add New Non-Consumable SubCategory

def addnonsubcategory(request):
    form=NonSubcategoryForm(request.POST or None)
    try:
        error = "no"
        if form.is_valid():
            form.save()
            # return redirect('inventory')
        else:
            error = "yes"
    except:
        error = "yes"
    return render(request,"Master/addnonsubcategory.html",locals())

# @method_decorator(login_required, name='dispatch')
@login_required(login_url='login')

# Add New Non-Consumable Description

def addnondescription(request):
    form=NonDescriptionForm(request.POST or None)
    try:
        error = "no"
        if form.is_valid():
            form.save()
        else:
            error = "yes"
    except:
        error = "yes"
    return render(request, "Master/addnondescription.html", locals())

# @method_decorator(login_required, name='dispatch')
@login_required(login_url='login')

# Master Page

def master(request):
    return render(request,'Master/master.html')


# @method_decorator(login_required, name='dispatch')
@login_required(login_url='login')

# Sorted SubCategory with category

def subcategorys(request):
    data = json.loads(request.body)
    category_id=data['id']
    subcategorys = Subcategory.objects.filter(category_id=category_id)
    return JsonResponse(list(subcategorys.values("id","subcategory")), safe=False)

# @method_decorator(login_required, name='dispatch')
@login_required(login_url='login')

# Sorted Description on category,SbCategory

def descriptions(request):
    data = json.loads(request.body)
    subcategory_id=data['id']
    descriptions = Description.objects.filter(subcategory_id=subcategory_id)
    return JsonResponse(list(descriptions.values("id","description")), safe=False)



# @method_decorator(login_required, name='dispatch')

@login_required(login_url='login')

# Sorted Description on category,SbCategory

def nonsubcategorys(request):
    data = json.loads(request.body)
    category_id=data['id']
    subcategorys = NonSubcategory.objects.filter(category_id=category_id)
    return JsonResponse(list(subcategorys.values("id","subcategory")), safe=False)

# @method_decorator(login_required, name='dispatch')

@login_required(login_url='login')

# Sorted Non-consumale Description
def nondescriptions(request):
    data = json.loads(request.body)
    subcategory_id=data['id']
    descriptions = NonDescription.objects.filter(subcategory_id=subcategory_id)
    return JsonResponse(list(descriptions.values("id","description")), safe=False)




# #History
# @method_decorator(login_required, name='dispatch')
@login_required(login_url='login')
# Display History Page
def get_trs(request):
    object_list=trs.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(object_list,500)

    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        object_list = paginator.page(1)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)
    context = {
        'object_list': object_list,
    }
    return render(request, 'History/trs_list.html', context)

import requests
    # import pandas as pd
import json
@login_required(login_url='login')

def my_form(request):
  if request.method == "POST":
    form = ConsumerForm(request)
    # b=form.data['gstin']
    # print(b)
    print('GST Number Is:',request.POST.get('gstin'))
    d=request.POST.get('gstin')
    # data = request.GET['gstin']
    # gstin = form.c["gstin"]
    print(type(d))
    # d = input("enter the ")
    url = ("http://sheet.gstincheck.co.in/check/e33d005358c1ecc5bc0229186afa1adc/" + d)
    r = requests.get(url)
    a = r.json()
    e = a['flag']
    print(e)
    if e == True:
        b = a['data']['lgnm']
        c = a['data']['pradr']['adr']
        print('Name:', b)
        print("address:", c)
        # return HttpResponse(f"Name:{b} and Address:{c}")
        return render(request,'suppliers/demo.html',{'b':b,'c':c,'d':d})
    else:
        print("GST Number is invalid Please Fill valid GST Number")
        return HttpResponse("invalid GST Number")
  else:
      form = ConsumerForm()
  return render(request,'suppliers/edit_consumer.html', {'form': form})


@login_required(login_url='login')

def gstverify(request):
    # if request.method=="POST":
    #     username = request.GET.get('username')
        global e
        global a
        global body
        # global name,body,address
        name = request.GET.get('name')
        phone = request.GET.get('phone')
        body = request.GET.get('gstin')
        email = request.GET.get('email')
        address = request.GET.get('address')
        print(name,phone,email,address)
        print(body)
        url = ("http://sheet.gstincheck.co.in/check/e33d005358c1ecc5bc0229186afa1adc/" + str(body))
        r = requests.get(url)
        a = r.json()
        e = a['flag']
        print(e)
        if e == True:
            b = a['data']['lgnm']
            c = a['data']['pradr']['adr']
            print('Name:', b)
            print("address:", c)
            return redirect('gst')
        return render(request, 'suppliers/demo1.html',{'e':e,'gstin':body})




@login_required(login_url='login')

def gstverify1(request):
    # if request.method=="POST":
    #     username = request.GET.get('username')
        global e
        global a
        global body
        # global name,body,address
        name = request.GET.get('name')
        phone = request.GET.get('phone')
        body = request.GET.get('gstin')
        email = request.GET.get('email')
        address = request.GET.get('address')
        print(name,phone,email,address)
        print(body)
        url = ("http://sheet.gstincheck.co.in/check/e33d005358c1ecc5bc0229186afa1adc/" + str(body))
        r = requests.get(url)
        a = r.json()
        e = a['flag']
        print(e)
        if e == True:
            b = a['data']['lgnm']
            c = a['data']['pradr']['adr']
            print('Name:', b)
            print("address:", c)
            return redirect('gst1')

        return render(request,'suppliers/demo1.html',{'e':e,'gstin':body})



@login_required(login_url='login')

def gst(request):
        b = a['data']['lgnm']
        c = a['data']['pradr']['adr']
        print('Name:', b)
        print("address:", c)
        if request.method == "POST":
            name = request.POST['name']
            phone = request.POST['phone']
            gstin = request.POST['gstin']
            email = request.POST['email']
            address = request.POST['address']
            if Consumer.objects.filter(gstin=gstin).exists():
                messages.success(request, 'GST Number is already exits. !')
            else:
                Consumer(name=name, phone=phone, address=address, email=email, gstin=gstin).save()
                return redirect('consumer-list')
        return render(request, 'suppliers/demo.html', {'b': b, 'c': c, 'd': body})

@login_required(login_url='login')

def gst1(request):
    b = a['data']['lgnm']
    c = a['data']['pradr']['adr']
    print('Name:', b)
    print("address:", c)
    if request.method == "POST":
        name = request.POST['name']
        phone = request.POST['phone']
        gstin = request.POST['gstin']
        email = request.POST['email']
        address = request.POST['address']
        if Supplier.objects.filter(gstin=gstin).exists():
            messages.success(request, 'GST Number is already exits !')
        else:
            Supplier(name=name, phone=phone, address=address, email=email, gstin=gstin).save()
            return redirect('suppliers-list')
    return render(request, 'suppliers/demo.html', {'b': b, 'c': c, 'd': body})

@login_required(login_url='login')
def inwardsliphistory(request):
    if request.method =="POST":
        try:
            error = "no"
            if request.method == "POST":
                fromdate = datetime.datetime.strptime(request.POST.get('fromdate'), '%Y-%m-%d')
                todate = datetime.datetime.strptime(request.POST.get('todate'), '%Y-%m-%d')
                bills = PurchaseBill.objects.filter(Q(time__gte=fromdate) & Q(time__lte=todate))
                return render(request, 'purchases/inwardsliphistory.html', {"bills": bills})
            else:
                error = "yes"
                bills = PurchaseBill.objects.all()
                return render(request, 'purchases/inwardsliphistory.html', {"bills": bills})

        except:
            error = "yes"
        return render(request, 'purchases/inwardsliphistory.html', locals())
    else:
        list = PurchaseBill.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(list,10)

        try:
            bills = paginator.page(page)
        except PageNotAnInteger:
            bills = paginator.page(1)
        except EmptyPage:
            bills = paginator.page(paginator.num_pages)

        context = {
            'bills': bills,
        }
        return render(request, 'purchases/inwardsliphistory.html', context)
@login_required(login_url='login')
def noninwardsliphistory(request):
    if request.method =="POST":
        try:
            error = "no"
            if request.method == "POST":
                fromdate = datetime.datetime.strptime(request.POST.get('fromdate'), '%Y-%m-%d')
                todate = datetime.datetime.strptime(request.POST.get('todate'), '%Y-%m-%d')
                bills = NonPurchaseBill.objects.filter(Q(time__gte=fromdate) & Q(time__lte=todate))
                return render(request, 'purchases/noninwardsliphistory.html', {"bills": bills})
            else:
                error = "yes"
                bills = NonPurchaseBill.objects.all()
                return render(request, 'purchases/noninwardsliphistory.html', {"bills": bills})

        except:
            error = "yes"
        return render(request, 'purchases/noninwardsliphistory.html', locals())
    else:
        list = NonPurchaseBill.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(list,10)

        try:
            bills = paginator.page(page)
        except PageNotAnInteger:
            bills = paginator.page(1)
        except EmptyPage:
            bills = paginator.page(paginator.num_pages)

        context = {
            'bills': bills,
        }
        return render(request, 'purchases/noninwardsliphistory.html', context)

def inwardHistory(request):
    obj = History.objects.all()
    return render(request, 'purchases/inwardsliphistory.html', {'bills': obj})

def noninwardHistory(request):
    obj = HNonStock.objects.all()
    return render(request, 'purchases/noninwardsliphistory.html', {'bills': obj})