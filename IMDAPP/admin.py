
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Category, Subcategory, Description, Stock, Supplier, PurchaseBill, PurchaseBillDetails, \
    PurchaseItem, SaleBill, SaleItem, SaleBillDetails, NonDescription, NonSubcategory, NonCategory, NonStock, \
    NonPurchaseBillDetails, NonPurchaseItem, NonPurchaseBill, NonSaleBill, NonSaleItem, NonSaleBillDetails, trs, \
    InwardBillDetails, NonInwardBillDetails, Unit, Consumer

admin.site.register(Stock)
admin.site.register(Unit)
admin.site.register(Consumer)
admin.site.register(NonStock)
admin.site.register(PurchaseBill)
admin.site.register(PurchaseBillDetails)
admin.site.register(InwardBillDetails)
admin.site.register(NonInwardBillDetails)
admin.site.register(PurchaseItem)
admin.site.register(SaleBill)
admin.site.register(NonSaleBill)
admin.site.register(SaleItem)
admin.site.register(NonSaleItem)
admin.site.register(SaleBillDetails)
admin.site.register(NonSaleBillDetails)
admin.site.register(NonPurchaseBill)
admin.site.register(NonPurchaseBillDetails)
admin.site.register(NonPurchaseItem)
admin.site.register(Category)
admin.site.register(NonCategory)
admin.site.register(Subcategory)
admin.site.register(NonSubcategory)
admin.site.register(Description)
admin.site.register(NonDescription)
admin.site.register(Supplier)
# admin.site.register(trs)

#
@admin.register(trs)
class trs(ImportExportModelAdmin):
    pass

