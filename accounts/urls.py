

from django.urls import path
from django.views.generic.base import TemplateView
from . import views
from django.conf.urls import url

urlpatterns = [
    path('signup/', views.adminin.signup, name="signup"),  
    path('activate/<uidb64>/<token>/',views.adminin.activate, name='activate'),  
    path('', views.viewing.dashboard, name='home'),
    path('invoice', views.viewing.invoice, name='invoice'),
    path('invoice/add', views.adding.invoice, name='addinvoice'),
    url(r'^invoice/edit/(?P<stockid>[0-9]+)/$', views.editing.invoice , name='editinvoice'),
    url(r'^invoice/return/(?P<stockid>[0-9]+)/$', views.editing.goodsreturn , name='goodsreturn'),
    path('dailysheet', views.viewing.dlsheet, name='dlsheet'),
    path('dailysheet/add', views.adding.dlsheet, name='adddlsheet'),
    url(r'^dailysheet/edit/(?P<stockid>[0-9]+)/$', views.editing.dlsheet , name='editdailysheet'),
    url(r'^dailysheet/receipt/(?P<stockid>[0-9]+)/$', views.adding.dlrsheet , name='dlrsheet'),
    url(r'^dailysheet/purchase/(?P<stockid>[0-9]+)/$', views.adding.dlpsheet , name='dlpsheet'),
    url(r'^dailysheet/transaction/(?P<stockid>[0-9]+)/$', views.adding.dlisheet , name='dlisheet'),

#ADMIN-----------------------------------------------------------------------------

    path('companyadd', views.administrative.addcompany , name='cadder'),
    path('fyadd', views.administrative.addfy , name='fyadder'),
    path('fyauth', views.administrative.fauth , name='fyauth'),
    path('cauth', views.administrative.coauth , name='cauth'),
    path('fyd', views.administrative.fyd , name='fyd'),
    path('cd', views.administrative.cd , name='cd'),
 
#PERSONAL---------------------------------------------------------------------------------------
#Accounts Info----------------------------------------------------------------------------------

        
    path('groups', views.viewing.group, name='groups'),
    url(r'^groups/edit/(?P<stockid>[0-9]+)/$', views.editing.group , name='editgroups'),
    url(r'^groups/add', views.adding.group , name='addgroups'),

    path('ledgers', views.viewing.ledger, name='ledgers'),
    url(r'^ledgers/edit/(?P<stockid>[0-9]+)/$', views.editing.ledger , name='editledgers'),
    url(r'^ledgers/add', views.adding.ledger , name='addledgers'),


    path('costcenter', views.viewing.costcenter, name='cost_centers'),
    url(r'^costcenters/edit/(?P<stockid>[0-9]+)/$', views.editing.costcenter , name='editcost_centers'),
    url(r'^costcenters/add', views.adding.costcenter , name='addcost_centers'),
#Inventory Info--------------------------------------------------------------------------------
#Stock---------------------------------------------------------------------
    path('stock', views.viewing.stock, name = 'stock'),
    path('stock/add', views.adding.stock, name = 'addstock'),
    url(r'^stock/edit/(?P<stockid>[0-9]+)/$', views.editing.stock , name='editstock'),
    url(r'^stock/transfer/(?P<stockid>[0-9]+)/$', views.stocktransfer , name='stocktransfer'),

#Warehouses------------------------------------------------------------------------------------------
    path('warehouse/add', views.adding.warehouse, name = 'addwarehouse'),
    path('warehouse', views.viewing.warehouse, name = 'warehouse'),
    url(r'^warehouse/edit/(?P<stockid>[0-9]+)/$', views.editing.warehouse , name='editwarehouse'),

#Vouchers-----------------------------------------------------------------------------------------
     path('voucher', views.viewing.voucher, name='vouchers'),
    url(r'^Purchase/edit/(?P<stockid>[0-9]+)/$', views.editing.purchase , name='editpurchase'),
    url(r'^Purchase/add/(?P<stockid>[0-9]+)/$', views.adding.purchase , name='addpurchasefinal'),
    url(r'^Receipt/add/(?P<stockid>[0-9]+)/$', views.adding.receipt , name='addreceiptfinal'),
    url(r'^Receipt/edit/(?P<stockid>[0-9]+)/$', views.editing.receipt , name='editreceipt'),
    url(r'^Purchase/add', views.adding.plselector , name='addpurchase'),
    url(r'^Receipt/add', views.adding.lselector, name='addreceipt'),

#Reports--------------------------------------------------------------------------------------------
   url(r'^balancesheet', views.Reports.balancesheet , name='balancesheet'),
   url(r'^pnl', views.Reports.pnl , name='pnl'),



 ]


