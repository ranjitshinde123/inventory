
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Category, Subcategory, Description, Stock, Supplier, PurchaseBill, PurchaseBillDetails,PurchaseItem, SaleBill, SaleItem, SaleBillDetails, NonDescription, NonSubcategory, NonCategory, NonStock,NonPurchaseBillDetails, NonPurchaseItem, Consumer, NonPurchaseBill, NonSaleBill, NonSaleItem, NonSaleBillDetails,trs

admin.site.register(Stock)
admin.site.register(NonStock)
admin.site.register(PurchaseBill)
admin.site.register(PurchaseBillDetails)
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
admin.site.register(Consumer)
admin.site.register(Supplier)
# admin.site.register(trs)

#
@admin.register(trs)
class trs(ImportExportModelAdmin):
    pass

# @admin.register(Category)
# class Category(ImportExportModelAdmin):
#     pass
#
#
# @admin.register(Subcategory)
# class Subcategory(ImportExportModelAdmin):
#     pass
#
#
# @admin.register(Description)
# class Description(ImportExportModelAdmin):
#     pass
#
# @admin.register(NonCategory)
# class NonCategory(ImportExportModelAdmin):
#     pass
#
#
# @admin.register(NonSubcategory)
# class NonSubcategory(ImportExportModelAdmin):
#     pass
#
#
# @admin.register(NonDescription)
# class NonDescription(ImportExportModelAdmin):
#     pass
#
#
#
# @admin.register(Supplier)
# class Supplier(ImportExportModelAdmin):
#     pass
#
# @admin.register(Consumer)
# class Consumer(ImportExportModelAdmin):
#     pass