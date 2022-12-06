from django import forms
from django.forms import formset_factory
from .models import (
    Supplier,
    PurchaseBill,
    PurchaseItem,
    PurchaseBillDetails,
    SaleBill,
    SaleItem,
    SaleBillDetails, Stock, Category, Subcategory, Description, NonStock, NonDescription, NonSubcategory, NonCategory,
    NonPurchaseBill, NonPurchaseBillDetails, NonPurchaseItem, Consumer, NonSaleBill, NonSaleBillDetails, NonSaleItem
)
class StockForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['subcategory'].queryset = Subcategory.objects.none()

            if 'category' in self.data:
                try:
                    category_id = int(self.data.get('category'))
                    self.fields['subcategory'].queryset = Subcategory.objects.filter(category_id=category_id).order_by(
                        'category')
                except (ValueError, TypeError):
                    pass  # invalid input from the client; ignore and fallback to empty City queryset
            elif self.instance.pk:
                self.fields['subcategory'].queryset = self.instance.category.subcategory_set.order_by('subcategory')

            self.fields['description'].queryset = Description.objects.none()
            if 'subcategory' in self.data:
                try:
                    subcategory_id = int(self.data.get('subcategory'))
                    self.fields['description'].queryset = Description.objects.filter(
                        subcategory_id=subcategory_id).order_by(
                        'subcategory')
                except (ValueError, TypeError):
                    pass  # invalid input from the client; ignore and fallback to empty City queryset
            elif self.instance.pk:
                self.fields['description'].queryset = self.instance.subcategory.description_set.order_by('description')
            self.fields['name'].widget.attrs.update({'class': 'textinput form-control', 'pattern' : '[a-zA-Z\s]{1,50}', 'title' : 'Alphabets and Spaces only'})
            self.fields['category'].widget.attrs.update({'class': 'textinput form-control'})
            self.fields['subcategory'].widget.attrs.update({'class': 'textinput form-control'})
            self.fields['description'].widget.attrs.update({'class': 'textinput form-control'})
            self.fields['quantity'].widget.attrs.update({'class': 'textinput form-control', 'min': '0'})
            self.fields['unit'].widget.attrs.update({'class': 'textinput form-control'})
            self.fields['Mode_of_delivery'].widget.attrs.update({'class': 'textinput form-control'})
            self.fields['condition'].widget.attrs.update({'class': 'textinput form-control'})
            self.fields['label_code'].widget.attrs.update({'class': 'textinput form-control'})




    class Meta:
        model = Stock
        fields = ['name','category','subcategory','description','quantity','unit','Mode_of_delivery','condition','label_code']

class NonStockForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)


            if 'category' in self.data:
                try:
                    category_id = int(self.data.get('category'))
                    self.fields['subcategory'].queryset = NonSubcategory.objects.filter(category_id=category_id).order_by(
                        'category')
                except (ValueError, TypeError):
                    pass  # invalid input from the client; ignore and fallback to empty City queryset
            elif self.instance.pk:
                pass


            if 'subcategory' in self.data:
                try:
                    subcategory_id = int(self.data.get('subcategory'))
                    self.fields['description'].queryset = NonDescription.objects.filter(
                        subcategory_id=subcategory_id).order_by(
                        'subcategory')
                except (ValueError, TypeError):
                    pass  # invalid input from the client; ignore and fallback to empty City queryset
            elif self.instance.pk:
                pass
            self.fields['name'].widget.attrs.update({'class': 'textinput form-control'})
            self.fields['category'].widget.attrs.update({'class': 'textinput form-control'})
            self.fields['subcategory'].widget.attrs.update({'class': 'textinput form-control'})
            self.fields['description'].widget.attrs.update({'class': 'textinput form-control'})
            self.fields['quantity'].widget.attrs.update({'class': 'textinput form-control', 'min': '0'})
            self.fields['Mode_of_delivery'].widget.attrs.update({'class': 'textinput form-control'})
            self.fields['condition'].widget.attrs.update({'class': 'textinput form-control'})
            self.fields['label_code'].widget.attrs.update({'class': 'textinput form-control'})




    class Meta:
        model = NonStock
        fields = ['name','category','subcategory','description','quantity','Mode_of_delivery','condition','label_code']



# form used to select a supplier
class SelectSupplierForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['supplier'].queryset = Supplier.objects.filter(is_deleted=False)
        self.fields['supplier'].widget.attrs.update({'class': 'textinput form-control'})
    class Meta:
        model = NonPurchaseBill
        fields = ['supplier']


# form used to render a single stock item form
class PurchaseItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['stock'].queryset = Stock.objects.filter(is_deleted=False)
        self.fields['stock'].widget.attrs.update({'class': 'textinput form-control setprice stock', 'required': 'true'})
        self.fields['quantity'].widget.attrs.update({'class': 'textinput form-control setprice quantity', 'min': '0', 'required': 'true'})
        self.fields['perprice'].widget.attrs.update({'class': 'textinput form-control setprice price', 'min': '0', 'required': 'true'})

    class Meta:
        model = PurchaseItem
        fields = ['stock', 'quantity', 'perprice']

# formset used to render multiple 'PurchaseItemForm'
PurchaseItemFormset = formset_factory(PurchaseItemForm, extra=1)

# form used to accept the other details for purchase bill
class PurchaseDetailsForm(forms.ModelForm):
    class Meta:
        model = PurchaseBillDetails
        fields = ['total']

#nonConsumable


class SelectConsumerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['consumer'].queryset = Consumer.objects.filter(is_deleted=False)
        self.fields['consumer'].widget.attrs.update({'class': 'textinput form-control'})
    class Meta:
        model = PurchaseBill
        fields = ['consumer']

class NonPurchaseItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nonstock'].queryset = NonStock.objects.filter(is_deleted=False)
        self.fields['nonstock'].widget.attrs.update({'class': 'textinput form-control setprice stock', 'required': 'true'})
        self.fields['quantity'].widget.attrs.update({'class': 'textinput form-control setprice quantity', 'min': '0', 'required': 'true'})
        self.fields['perprice'].widget.attrs.update({'class': 'textinput form-control setprice price', 'min': '0', 'required': 'true'})
    class Meta:
        model = NonPurchaseItem
        fields = ['nonstock', 'quantity', 'perprice']

# formset used to render multiple 'PurchaseItemForm'
NonPurchaseItemFormset = formset_factory(NonPurchaseItemForm, extra=1)


# form used to accept the other details for purchase bill
class NonPurchaseDetailsForm(forms.ModelForm):
    class Meta:
        model = NonPurchaseBillDetails
        fields = ['total']


# form used for supplier
class SupplierForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['phone'].widget.attrs.update({'class': 'textinput form-control', 'maxlength': '10', 'pattern': '[0-9]{10}', 'title': 'Numbers only'})
        self.fields['email'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['gstin'].widget.attrs.update({'class': 'textinput form-control', 'maxlength': '15', 'pattern': '[A-Z0-9]{15}','title': 'GSTIN Format Required'})

    class Meta:
        model = Supplier
        fields = ['name', 'phone', 'address', 'email','gstin']
        widgets = {
            'address': forms.Textarea(
                attrs={
                    'class': 'textinput form-control',
                    'rows': '1'
                }
            )
        }


class ConsumerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['phone'].widget.attrs.update({'class': 'textinput form-control', 'maxlength': '10', 'pattern': '[0-9]{10}', 'title': 'Numbers only'})
        self.fields['email'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['U_Type'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['gstin'].widget.attrs.update({'class': 'textinput form-control', 'maxlength': '15', 'pattern': '[A-Z0-9]{15}','title': 'GSTIN Format Required'})


    class Meta:
        model = Consumer
        fields = ['name', 'phone', 'address', 'email','U_Type','gstin']
        widgets = {
            'address': forms.Textarea(
                attrs={
                    'class': 'textinput form-control',
                    'rows': '1'
                }
            )
        }



# form used to get customer details
class SaleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = Subcategory.objects.filter(category_id=category_id).order_by(
                    'category')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            pass

        if 'subcategory' in self.data:
            try:
                subcategory_id = int(self.data.get('subcategory'))
                self.fields['description'].queryset = Description.objects.filter(
                    subcategory_id=subcategory_id).order_by(
                    'subcategory')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            pass
        self.fields['name'].widget.attrs.update({'class': 'textinput form-control', 'pattern' : '[a-zA-Z\s]{1,50}', 'title' : 'Alphabets and Spaces only', 'required': 'true'})
        self.fields['phone'].widget.attrs.update({'class': 'textinput form-control', 'maxlength': '10', 'pattern' : '[0-9]{10}', 'title' : 'Numbers only', 'required': 'true'})
        self.fields['email'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['address'].widget.attrs.update({'class': 'textinput form-control', 'pattern' : '[a-zA-Z\s]{1,50}', 'title' : 'Alphabets and Spaces only', 'required': 'true'})
        self.fields['issued_to'].widget.attrs.update({'class': 'textinput form-control', 'pattern' : '[a-zA-Z\s]{1,50}', 'title' : 'Alphabets and Spaces only', 'required': 'true'})
        self.fields['category'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['description'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['subcategory'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['Mode_of_delivery'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['label_code'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['gstin'].widget.attrs.update({'class': 'textinput form-control', 'maxlength': '15', 'pattern': '[A-Z0-9]{15}','title': 'GSTIN Format Required'})




    class Meta:
        model = SaleBill
        fields = ['name', 'phone', 'email','address','issued_to','category','subcategory','Mode_of_delivery','label_code','description','gstin']




class SaleItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['stock'].queryset = Stock.objects.filter(is_deleted=False)
        self.fields['stock'].widget.attrs.update({'class': 'textinput form-control setprice stock', 'required': 'true'})
        self.fields['quantity'].widget.attrs.update({'class': 'textinput form-control setprice quantity', 'min': '0', 'required': 'true'})
        self.fields['perprice'].widget.attrs.update({'class': 'textinput form-control setprice price', 'min': '0', 'required': 'true'})

    class Meta:
        model = SaleItem
        fields = ['stock', 'quantity', 'perprice']

# formset used to render multiple 'SaleItemForm'
SaleItemFormset = formset_factory(SaleItemForm, extra=1)

# form used to accept the other details for sales bill
class SaleDetailsForm(forms.ModelForm):
    class Meta:
        model = SaleBillDetails
        fields = ['total']

#nonconsumable


class NonSaleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = NonSubcategory.objects.filter(category_id=category_id).order_by(
                    'category')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['subcategory'].queryset = self.instance.category.subcategory_set.order_by('subcategory')

        if 'subcategory' in self.data:
            try:
                subcategory_id = int(self.data.get('subcategory'))
                self.fields['description'].queryset = NonDescription.objects.filter(
                    subcategory_id=subcategory_id).order_by(
                    'subcategory')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            pass
            self.fields['description'].queryset = self.instance.subcategory.description_set.order_by('description')
        self.fields['name'].widget.attrs.update({'class': 'textinput form-control', 'pattern' : '[a-zA-Z\s]{1,50}', 'title' : 'Alphabets and Spaces only', 'required': 'true'})
        self.fields['phone'].widget.attrs.update({'class': 'textinput form-control', 'maxlength': '10', 'pattern' : '[0-9]{10}', 'title' : 'Numbers only', 'required': 'true'})
        self.fields['email'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['address'].widget.attrs.update({'class': 'textinput form-control', 'pattern' : '[a-zA-Z\s]{1,50}', 'title' : 'Alphabets and Spaces only', 'required': 'true'})
        self.fields['issued_to'].widget.attrs.update({'class': 'textinput form-control', 'pattern' : '[a-zA-Z\s]{1,50}', 'title' : 'Alphabets and Spaces only', 'required': 'true'})
        self.fields['category'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['description'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['subcategory'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['Mode_of_delivery'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['label_code'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['gstin'].widget.attrs.update({'class': 'textinput form-control', 'maxlength': '15', 'pattern': '[A-Z0-9]{15}','title': 'GSTIN Format Required'})




    class Meta:
        model = NonSaleBill
        fields = ['name', 'phone', 'email','address','issued_to','category','subcategory','Mode_of_delivery','label_code','description','gstin']



#
class NonSaleItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nonstock'].queryset = NonStock.objects.filter(is_deleted=False)
        self.fields['nonstock'].widget.attrs.update({'class': 'textinput form-control setprice nonstock', 'required': 'true'})
        self.fields['quantity'].widget.attrs.update({'class': 'textinput form-control setprice quantity', 'min': '0', 'required': 'true'})
        self.fields['perprice'].widget.attrs.update({'class': 'textinput form-control setprice price', 'min': '0', 'required': 'true'})

    class Meta:
        model = NonSaleItem
        fields = ['nonstock', 'quantity', 'perprice']

# formset used to render multiple 'SaleItemForm'
NonSaleItemFormset = formset_factory(NonSaleItemForm, extra=1)

# form used to accept the other details for sales bill
class NonSaleDetailsForm(forms.ModelForm):
    class Meta:
        model = NonSaleBillDetails
        fields = ['total']




class CategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].widget.attrs.update({'class': 'textinput form-control'})


    class Meta:
        model = Category
        fields = ['category']

class SubcategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['subcategory'].widget.attrs.update({'class': 'textinput form-control'})



    class Meta:
        model = Subcategory
        fields = ['category','subcategory']


class DescriptionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['subcategory'].widget.attrs.update({'class': 'textinput form-control'})


    class Meta:
        model = Description
        fields = ['category','subcategory','description']
        widgets = {
            'description': forms.Textarea(
                attrs={
                    'class': 'textinput form-control',
                    'rows': '2'
                }
            )
        }


class NonCategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].widget.attrs.update({'class': 'textinput form-control'})

    class Meta:
        model = NonCategory
        fields = ['category']

class NonSubcategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['subcategory'].widget.attrs.update({'class': 'textinput form-control'})



    class Meta:
        model = NonSubcategory
        fields = ['category','subcategory']


class NonDescriptionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['subcategory'].widget.attrs.update({'class': 'textinput form-control'})


    class Meta:
        model = NonDescription
        fields = ['category','subcategory','description']
        widgets = {
            'description': forms.Textarea(
                attrs={
                    'class': 'textinput form-control',
                    'rows': '2'
                }
            )
        }