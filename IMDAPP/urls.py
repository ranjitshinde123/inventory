from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import static



urlpatterns = [
    path('', views.StockListView.as_view(), name='inventory'),
    path('new', views.StockCreateView.as_view(), name='new-stock'),
    path('stock/<pk>/edit', views.StockUpdateView.as_view(), name='edit-stock'),
    path('stock/<pk>/delete', views.StockDeleteView.as_view(), name='delete-stock'),
    path('stock/<name>', views.StockView.as_view(), name='stockdetails'),

    path('nonconsumable/', views.NonStockListView.as_view(), name='nonconsumable'),
    path('nonnew', views.NonStockCreateView.as_view(), name='new-nonstock'),
    path('nonstock/<pk>/edit', views.NonStockUpdateView.as_view(), name='edit-nonstock'),
    path('nonstock/<pk>/delete', views.NonStockDeleteView.as_view(), name='delete-nonstock'),
    path('nonstock/<name>', views.NonStockView.as_view(), name='nonstockdetails'),
    path('stock/<name>', views.StockView.as_view(), name='stockdetails'),

    path('consumers/', views.ConsumerListView.as_view(), name='consumer-list'),
    path('consumers/new', views.ConsumerCreateView.as_view(), name='new-consumer'),
    path('consumers/<pk>/edit', views.ConsumerUpdateView.as_view(), name='edit-consumer'),
    path('consumers/<pk>/delete', views.ConsumerDeleteView.as_view(), name='delete-consumer'),
    path('consumers/<name>', views.ConsumerView.as_view(), name='consumer'),


    path('suppliers/', views.SupplierListView.as_view(), name='suppliers-list'),
    path('suppliers/new', views.SupplierCreateView.as_view(), name='new-supplier'),
    path('suppliers/<pk>/edit', views.SupplierUpdateView.as_view(), name='edit-supplier'),
    path('suppliers/<pk>/delete', views.SupplierDeleteView.as_view(), name='delete-supplier'),
    path('suppliers/<name>', views.SupplierView.as_view(), name='supplier'),


    path('purchases/', views.PurchaseView.as_view(), name='purchases-list'),
    path('purchases/new', views.SelectConsumerView.as_view(), name='select-consumer'),
    path('purchases/new/<pk>', views.PurchaseCreateView.as_view(), name='new-purchase'),
    path('purchases/<pk>/delete', views.PurchaseDeleteView.as_view(), name='delete-purchase'),


    path('nonpurchases/', views.NonPurchaseView.as_view(), name='nonpurchases-list'),
    path('nonpurchases/new', views.SelectSupplierView.as_view(), name='select-supplier'),
    path('nonpurchases/new/<pk>', views.NonPurchaseCreateView.as_view(), name='non-purchase'),
    path('nonpurchases/<pk>/delete', views.NonPurchaseDeleteView.as_view(), name='delete-nonpurchase'),


    # path('stockreport/', views.showresult, name='stockreport'),
    path('outwardslip/', views.outwardslip, name='outwardslip'),
    path('nonoutwardslip/', views.nonoutwardslip, name='nonoutwardslip'),
    path('inwardslip/', views.inwardslip, name='inwardslip'),
    path('noninwardslip/', views.noninwardslip, name='noninwardslip'),


    path('export/', views.export_csv, name='stockre'),
    path('nonexport/', views.nonexport_csv, name='nonstockre'),
    path('outwardexport_csv/', views.outwardexport_csv, name='outwardexport_csv'),
    path('outwardnonexport_csv/', views.outwardnonexport_csv, name='outwardnonexport_csv'),

    path('sales/', views.SaleView.as_view(), name='sales-list'),
    path('sales/new', views.SaleCreateView.as_view(), name='new-sale'),
    path('sales/<pk>/delete', views.SaleDeleteView.as_view(), name='delete-sale'),
    path("sales/<billno>", views.SaleBillView.as_view(), name="sale-bill"),

    path('nonsales/', views.NonSaleView.as_view(), name='nonsales-list'),
    path('nonsales/new', views.NonSaleCreateView.as_view(), name='new-nonsale'),
    path('nonsales/<pk>/delete', views.NonSaleDeleteView.as_view(), name='delete-nonsale'),
    path("nonsales/<billno>", views.NonSaleBillView.as_view(), name="nonsale-bill"),

    path("purchases/<billno>", views.PurchaseBillView.as_view(), name='purchase-bill'),

    path('nonpurchases/<billno>', views.NonPurchaseBillView.as_view(), name='nonpurchase-bill'),





    path('Master/new',views.addcategory, name='addcategory'),
    path('Master/',views.master,name='master'),

    path('Master/subcategory',views.addsubcategory, name='addsubcategory'),
    path('Master/description',views.adddescription, name='adddescription'),

    path('Master/nonnew', views.addnoncategory, name='addnoncategory'),
    path('Master/nonsubcategory', views.addnonsubcategory, name='addnonsubcategory'),
    path('Master/nondescription', views.addnondescription, name='addnondescription'),

    path('subcategorys', views.subcategorys, name="subcategorys"),
    path('descriptions', views.descriptions, name="descriptions"),

    path('nonsubcategorys', views.nonsubcategorys, name="nonsubcategorys"),
    path('nondescriptions', views.nondescriptions, name="nondescriptions"),

    #History
    path('historypage/', views.get_trs, name="trs")

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
