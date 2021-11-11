from .models import *
from django.shortcuts import get_object_or_404,render
from django.contrib import messages
from .forms import *
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.forms import formset_factory,DateInput
from django import forms 
#Signupp

#login--------------------------------------------------------------------------------------------------------------------------------------------------
from django.http import HttpResponse

#Signup-------------------------------------------------------------------------------------------
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

UserModel = get_user_model()
from .forms import SignUpForm

class adminin():
 def default_creator(user,company):
        Type_Choices = ["Capital Account","Loans(Liability)","Current Liabilities","Fixed Assets","Investments","Current Assets","Branch Divisions","Suspense AC","Sales Account","Purchase Accounts","Direct Incomes","Direct Expenses","Indirect Incomes","Indirect Expenses"]
        for x in Type_Choices:
          c = default_group(name  = x,df=True,type=x,user=user)
          c.save()
        q = Ledger(name = "Sales Register",df=True,company=company, header=default_group.objects.filter(name='Sales Account')[0],cc=False)
        w = Ledger(name = "Money Account",df=True,company=company, header=default_group.objects.filter(name='Current Assets')[0],cc = True)
        q.save()
        w.save()
        print(w)
        print(q)
        Cost_Center(Name = "Cash",df=True,company=company, ltype=w,Description="Default Cash Account").save()
        Cost_Center(Name = "Sales Register",df=True,company=company, ltype=q,Description="Default Sales Register").save()

 def signup(request):
    if request.method == 'GET':
        return render(request, 'registration/signup.html')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        # print(form.errors.as_data())
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            print(request.POST['company'])
            c = Company(name = request.POST['company'], user=user)
            c.save()
            adminin.default_creator(user,c)
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('emails/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


 def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponseRedirect(reverse_lazy("home"))
    else:
      return HttpResponse('Activation link is invalid!')




@login_required
def stocktransfer(request, stockid):
    item = Stock.objects.get(pk=stockid)
    if request.method == 'POST':
        form = stocktransferer(request.user.cauth.company, request.POST)
        if form.is_valid():  
              quantity = request.POST['Quantity']
              warehouse = request.POST['Warehouse']
              item.Quantity -= int(quantity)
              item.save()
              if Stock.objects.filter(Name = item.Name, Price = item.Price,Color = item.Color,Warehouse = Warehouse.objects.get(pk=warehouse),Model=item.Model, Size = item.Size,company= request.user.cauth.company):
                 z = Stock.objects.filter(Name = item.Name, Price = item.Price,Color = item.Color,Warehouse = Warehouse.objects.get(pk=warehouse),Model=item.Model, Size = item.Size,company= request.user.cauth.company)[0]
                 z.Quantity += int(quantity)
                 z.save()
              else:
                 r = Stock(Name = item.Name, Price = item.Price,Color = item.Color,Warehouse = Warehouse.objects.get(pk=warehouse),Model=item.Model,Quantity = quantity, Size = item.Size,company= request.user.cauth.company)
                 r.save()
              return HttpResponseRedirect('/stock/edit/'+str(stockid))
    else:
      
      form = stocktransferer(request.user.cauth.company,instance = item)

    context = {'form':form}
    template = "stock/stocktransfer.html"
    return render(request, template, context)


#-----------------------------------------------------------------------------------------------------------------------



class administrative:
    @login_required
    def addcompany(request):
      if request.method == 'POST':
        form = Companyadder(request.POST)
        if form.is_valid():
              instance = form.save(commit = False) 
              instance.user = request.user 
              instance.save()
              return HttpResponseRedirect(reverse_lazy("home"))
      else:
       form = Companyadder()

      context = {'form':form}
      template = "company/addcompany.html"
      return render(request, template, context)

    @login_required
    def addfy(request):
        if request.method == 'POST':
            form = fyadder(request.POST)
            if form.is_valid():
              instance = form.save(commit = False) 
              instance.company = request.user.cauth.company 
              instance.save()
              return HttpResponseRedirect(reverse_lazy("home"))
        else:
          form = fyadder()

        context = {'form':form}
        template = "company/addfy.html"
        return render(request, template, context)

    @login_required
    def fyd(request):
      fyauth.objects.get(user = request.user).delete() 
      return HttpResponseRedirect(reverse_lazy("home"))

    @login_required
    def cd(request):
          cauth.objects.get(user = request.user).delete() 
          fyauth.objects.get(user = request.user).delete() 
          return HttpResponseRedirect(reverse_lazy("home"))

    @login_required
    def fauth(request):
        company = request.user.cauth.company
        if request.method == 'POST':
            form = fyauthform(company, request.POST)
            if form.is_valid():
              a = form.save(commit = False)
              if fyauth.objects.filter(user=request.user).exists():
                  s = fyauth.objects.get(user = request.user)
              else:
                  s = fyauth(user = request.user)
              s.year = a.year 
              s.save()

              return HttpResponseRedirect("/")

        else:
          form = fyauthform(company)
        context = {'form':form}
        template = "registration/fyauth.html"
        return render(request, template, context)

    @login_required
    def coauth(request):
        company = request.user
        if request.method == 'POST':
            form = cauthform(company, request.POST)
            if form.is_valid():
              a = form.save(commit = False)
              if cauth.objects.filter(user=request.user).exists():
                  s = cauth.objects.get(user = request.user)
              else:
                  s = cauth(user = request.user)
              s.company = a.company 
              s.save()

              return HttpResponseRedirect("/")

        else:
          form = cauthform(company)
        context = {'form':form}
        template = "registration/cauth.html"
        return render(request, template, context)

class viewing:
    @login_required
    def voucher(request):
      stock = Purchase.objects.filter(company = request.user.cauth.company,fy = request.user.fyauth.year)
      othr = Receipt.objects.filter(company = request.user.cauth.company,fy = request.user.fyauth.year)
      context = {'stock': stock, 'othr':othr}
      template = "bills/bill.html"
      return render(request, template, context)

    @login_required
    def dashboard(request):
        template = "dashboard/dashboard.html"
        return render(request, template)
 
    @login_required
    def group(request):
        stock = default_group.objects.filter(user = request.user)
        context = {'stock': stock}
        template = "Groups/default.html"
        return render(request, template, context)  

    @login_required
    def ledger(request):
        stock = Ledger.objects.filter(company = request.user.cauth.company)
        context = {'stock': stock}
        template = "ledger/category.html"
        return render(request, template, context)  

    @login_required
    def costcenter(request):
       stock = Cost_Center.objects.filter(company = request.user.cauth.company)
       context = {'stock': stock}
       template = "Costcenter/ledger.html"
       return render(request, template, context)  

    @login_required
    def stock(request):
      stock = Stock.objects.filter(company=request.user.cauth.company)
      context = {'stock': stock}
      template = "stock/tables.html"
      return render(request, template, context)

    @login_required
    def warehouse(request):
       stock = Warehouse.objects.filter(company=request.user.cauth.company)
       context = {'stock': stock}
       template = "stock/warehouse.html"
       return render(request, template, context)

    @login_required
    def invoice(request):
        stock = Invoice.objects.filter(company = request.user.cauth.company,fy = request.user.fyauth.year)
        context = {'stock': stock}
        template = "invoices/invoices.html"
        return render(request, template, context)  

    @login_required
    def dlsheet(request):
      stock = dlsheet.objects.filter(company=request.user.cauth.company,fy = request.user.fyauth.year)
      context = {'stock': stock}
      template = "DailySheets/Dailysheet.html"
      return render(request, template, context)



class adding:
    @login_required
    def group(request):
        if request.method == 'POST':
            form = Groupadder(request.POST)
            if form.is_valid():
              instance = form.save(commit = False)
              instance.user = request.user 
              instance.df = False
              instance.save()
              return HttpResponseRedirect(reverse_lazy('groups'))
        else:
          form = Groupadder()

        context = {'form':form}
        template = "Groups/adddefault.html"
        return render(request, template, context)

    @login_required
    def ledger(request):
        if request.method == 'POST':
            form = Ledgeradder(request.user,request.POST)
            if form.is_valid():
              instance = form.save(commit = False)
              instance.company = request.user.cauth.company 
              instance.df = False
              instance.save()
              if not instance.cc: 
                 y = Cost_Center(Name=instance.name,df = instance.df,Description = "Default",ltype=instance,company = instance.company)
                 y.save()

              messages.success(request, "Group Added")
              return HttpResponseRedirect(reverse_lazy('ledgers'))
        else:
          form = Ledgeradder(request.user)

        context = {'form':form}
        template = "ledger/addcategory.html"
        return render(request, template, context)

    @login_required
    def costcenter(request):
        if request.method == 'POST':
            form = Cost_centeradder(request.user.cauth.company,request.POST)
            if form.is_valid():
              instance = form.save(commit = False)
              instance.company = request.user.cauth.company 
              instance.df = False
              instance.save()
              return HttpResponseRedirect(reverse_lazy('cost_centers'))
        else:
          form = Cost_centeradder(request.user.cauth.company)

        context = {'form':form}
        template = "Costcenter/addledger.html"
        return render(request, template, context)
    
    @login_required
    def stock(request):
        if request.method == 'POST':
            form = Stockadder(request.user.cauth.company,request.POST)
            if form.is_valid():
              a = form.save(commit=False)
              a.company = request.user.cauth.company
              if a.Size == 'SET':
                  import copy
                  a.Size = '22'
                  b = copy.copy(a)
                  c = copy.copy(b)
                  b.Size = '24'
                  c.Size = '26'
                  a.save() 
                  b.save()
                  c.save()
              else:
                  a.save()
              messages.success(request, "Stock Added")
              return HttpResponseRedirect(reverse_lazy('stock'))

        else:
          form = Stockadder(request.user.cauth.company)

        context = {'form':form}
        template = "stock/addstock.html"
        return render(request, template, context)

    @login_required
    def warehouse(request):
        if request.method == 'POST':
            form = Warehouseadder(request.POST)
            if form.is_valid():
              instance = form.save(commit = False)
              instance.company = request.user.cauth.company
              instance.save() 
              messages.success(request, "Warehouse Added")
              return HttpResponseRedirect(reverse_lazy('warehouse'))
        else:
          form = Warehouseadder()
        context = {'form':form}
        template = "stock/addwarehouse.html"
        return render(request, template, context)

    @login_required
    def invoice(request):
        if request.method == 'POST':
            form = invoicemaker(request.user.cauth.company,request.POST)
            if form.is_valid():
              instance = form.save(commit = False)
              instance.company = request.user.cauth.company
              instance.fy = request.user.fyauth.year 
              instance.final = False
              instance.amount = 0
              instance.save()
              return HttpResponseRedirect('/invoice/edit/'+str(instance.pk))
        else:
          form = invoicemaker(request.user.cauth.company)

        context = {'form':form}
        template = "invoices/addinvoice.html"
        return render(request, template, context)

    @login_required
    def purchase(request,stockid):
        if request.method == 'POST':
            form = Purchaseadder(request.user.cauth.company,stockid,request.POST)
            if form.is_valid():
              instance = form.save(commit=False)
              instance.company = request.user.cauth.company
              instance.fy = request.user.fyauth.year
              instance.save() 
              return HttpResponseRedirect(reverse_lazy('vouchers'))
        else:
          form = Purchaseadder(request.user.cauth.company,stockid)

        context = {'form':form,'stockid':stockid}
        template = "bills/addbill.html"
        return render(request, template, context)

    @login_required
    def receipt(request,stockid):
        if request.method == 'POST':
            form = Receiptadder(request.user.cauth.company,stockid,request.POST)
            if form.is_valid():
              instance = form.save(commit=False)
              instance.company = request.user.cauth.company
              instance.fy = request.user.fyauth.year
              instance.save() 
              return HttpResponseRedirect(reverse_lazy('vouchers'))
        else:
          form = Receiptadder(request.user.cauth.company,stockid)

        context = {'form':form,'stockid':stockid}
        template = "bills/addcredit.html"
        return render(request, template, context)

    @login_required
    def dlsheet(request):
      if request.method == 'POST':
            form = dlsheetadder(request.POST)
            if form.is_valid():
              instance = form.save(commit = False)
              instance.company = request.user.cauth.company
              instance.fy = request.user.fyauth.year 
              instance.save()
              return HttpResponseRedirect(reverse_lazy("editdailysheet", kwargs={'stockid':instance.id }))
      else:
          form = dlsheetadder()

      context = {'form':form}
      template = "DailySheets/Adddlsheet.html"
      return render(request, template, context)

    @login_required
    def dlrsheet(request,stockid):
      ArticleFormSet = formset_factory(dlsheetReceiptadder)
      if request.method == 'POST':
        formset = ArticleFormSet(request.POST, request.FILES,form_kwargs={'user': request.user.cauth.company})
        if formset.is_valid():
            r = dlsheet.objects.get(id=stockid)
            for form in formset:
              instance = form.save(commit=False)
              instance.company = request.user.cauth.company
              instance.fy = request.user.fyauth.year
              instance.save()  
              r.Receipts.add(instance)
            return HttpResponseRedirect(reverse_lazy('editdailysheet', kwargs={'stockid': stockid}))
            # do something with the formset.cleaned_data
          
      else:
        formset = ArticleFormSet(form_kwargs={'user': request.user.cauth.company})
      return render(request, 'DailySheets/test.html', {'formset': formset})

    @login_required
    def dlpsheet(request,stockid):
      ArticleFormSet = formset_factory(dlsheetPurchaseadder)
      if request.method == 'POST':
        formset = ArticleFormSet(request.POST, request.FILES,form_kwargs={'user': request.user.cauth.company})
        if formset.is_valid():
            r = dlsheet.objects.get(id=stockid)
            for form in formset:
              print(form)
              instance = form.save(commit=False)
              instance.company = request.user.cauth.company
              instance.fy = request.user.fyauth.year
              instance.save()
              r.Purchases.add(instance)

            return HttpResponseRedirect(reverse_lazy('editdailysheet', kwargs={'stockid': stockid}))
            # do something with the formset.cleaned_data
      else:
        formset = ArticleFormSet(form_kwargs={'user': request.user.cauth.company})
      return render(request, 'DailySheets/test.html', {'formset': formset})

    

    @login_required
    def dlisheet(request,stockid):
      ReceiptFormSet = formset_factory(dlsheetReceiptadder)
      PurchaseFormSet = formset_factory(dlsheetPurchaseadder)
      if request.method == 'POST':
        receipt_formset = ReceiptFormSet(request.POST, request.FILES, prefix='receipt',form_kwargs={'user': request.user.cauth.company})
        purchase_formset = PurchaseFormSet(request.POST, request.FILES, prefix='purchase',form_kwargs={'user': request.user.cauth.company})
        if receipt_formset.is_valid() and purchase_formset.is_valid():
            r = dlsheet.objects.get(id=stockid)
            for form in receipt_formset:
              instance = form.save(commit=False)
              instance.company = request.user.cauth.company
              instance.fy = request.user.fyauth.year
              instance.Date = r.Date
              instance.save()
              r.Receipts.add(instance)
            for form in purchase_formset:
              instance = form.save(commit=False)
              instance.company = request.user.cauth.company
              instance.fy = request.user.fyauth.year
              instance.Date = r.Date
              instance.save()
              r.Purchases.add(instance)
             
            return HttpResponseRedirect(reverse_lazy('editdailysheet', kwargs={'stockid': stockid}))
        else:
          print('Receipt')
          print(receipt_formset.errors)
          print(receipt_formset.non_form_errors())
          print('purchase')
          print(purchase_formset.errors)
          print(purchase_formset.non_form_errors())
     
      else:
        receipt_formset = ReceiptFormSet(prefix='receipt',form_kwargs={'user': request.user.cauth.company})
        purchase_formset = PurchaseFormSet(prefix='purchase',form_kwargs={'user': request.user.cauth.company})
      return render(request, 'DailySheets/test.html', {'receipt_formset': receipt_formset,'purchase_formset': purchase_formset,'stockid':stockid})

    @login_required
    def lselector(request):
      if request.method == 'POST':
            form = ledgerselector(request.user.cauth.company,request.POST)
            if form.is_valid():
              instance = form.save(commit = False)
              return HttpResponseRedirect(reverse_lazy('addreceiptfinal', kwargs={'stockid': instance.ltype.id }))
      else:
          form = ledgerselector(request.user.cauth.company)

      context = {'form':form}
      template = "ledger/lselector.html"
      return render(request, template, context)

    @login_required
    def plselector(request):
      if request.method == 'POST':
            form = ledgerselector(request.user.cauth.company,request.POST)
            if form.is_valid():
              instance = form.save(commit = False)
              return HttpResponseRedirect(reverse_lazy('addpurchasefinal', kwargs={'stockid': instance.ltype.id }))
      else:
          form = ledgerselector(request.user.cauth.company)

      context = {'form':form}
      template = "ledger/plselector.html"
      return render(request, template, context)

class editing:
  @login_required
  def group(request, stockid):
    item = default_group.objects.get(pk=stockid)
    items = Ledger.objects.filter(header = item, company = request.user.cauth.company)
    if request.method == 'POST':
        form = Groupadder(request.POST, instance = item)
        if form.is_valid():
              if request.POST['save'] == "save":
                  form.save()
                  return HttpResponseRedirect(reverse_lazy("groups"))
              elif request.POST['save'] == "delete":
                  item.delete() 
                  return HttpResponseRedirect(reverse_lazy("groups"))
       
    else:
      form = Groupadder(instance = item)
    
    if item.df:
       context = {'form':form, 'stock': [item],'items':items}
       template = "Groups/viewgroups.html"
    else:
       context = {'form':form, 'stock': items}
       template = "Groups/editdefault.html"
    return render(request, template, context)

  @login_required
  def ledger(request, stockid):
    item = Ledger.objects.get(pk=stockid)
    items = Cost_Center.objects.filter(ltype = item, company = request.user.cauth.company)
    if request.method == 'POST':
        form = Ledgeradder(request.user,request.POST, instance = item)
        if form.is_valid():
              if request.POST['save'] == "save":
                  form.save()
                  return HttpResponseRedirect(reverse_lazy("ledgers"))
              elif request.POST['save'] == "delete":
                  item.delete() 
                  return HttpResponseRedirect(reverse_lazy("ledgers"))
              
    else:
      
      form = Ledgeradder(request.user,instance = item)
    if item.df:
       context = {'form':form, 'stock': [item]}
       template = "ledger/category.html"
    else:
       context = {'form':form, 'stock': items}
       template = "ledger/editcategory.html"
    return render(request, template, context)

  @login_required
  def costcenter(request, stockid):
    item = Cost_Center.objects.get(pk = stockid)
    othr = Receipt.objects.filter(Cost_Center = item, company = request.user.cauth.company, fy=request.user.fyauth.year)
    stock = Purchase.objects.filter(Cost_Center = item, company = request.user.cauth.company, fy=request.user.fyauth.year)
    invc = Invoice.objects.filter(Cost_Center = item, company = request.user.cauth.company, fy=request.user.fyauth.year)
    if request.method == 'POST':
        form = Cost_centeradder(request.user.cauth.company,request.POST, instance = item)
        if form.is_valid():
              if request.POST['save'] == "save":
                  form.save()
                  return HttpResponseRedirect(reverse_lazy("cost_centers"))
              elif request.POST['save'] == "delete":
                  item.delete() 
                  return HttpResponseRedirect(reverse_lazy("cost_centers"))
              
    else:
      
      form = Cost_centeradder(request.user.cauth.company,instance = item)

    if item.df:
       context = {'form':form,'othr':othr, 'stock': [item],'invc':invc}
       template = "Costcenter/ledger.html"
    else:
       context = {'form':form, 'othr':othr, 'stock':stock,'invc':invc}
       template = "Costcenter/editledger.html"
    return render(request, template, context)

  @login_required
  def stock(request, stockid):
    item = Stock.objects.get(pk=stockid)
    if request.method == 'POST':
        form = Stockadder(request.user.cauth.company,request.POST, instance = item)
        if form.is_valid():
              if request.POST['save'] == "save":
                  form.save()
                  return HttpResponseRedirect("/stock")
              elif request.POST['save'] == "delete":
                  item.delete() 
                  return HttpResponseRedirect("/stock")
              
    else:
      
      form = Stockadder(request.user.cauth.company,instance = item)

    context = {'form':form}
    template = "stock/editstock.html"
    return render(request, template, context)

  @login_required
  def warehouse(request, stockid):
    item = Warehouse.objects.get(pk=stockid)
    items = Stock.objects.filter(Warehouse = item)
    if request.method == 'POST':
        form = Warehouseadder(request.POST, instance = item)
        if form.is_valid():
              if request.POST['save'] == "save":
                  form.save()
                  return HttpResponseRedirect("/warehouse")
              elif request.POST['save'] == "delete":
                  item.delete() 
                  return HttpResponseRedirect("/warehouse")
              
    else:
      
      form = Warehouseadder(instance = item)

    context = {'form':form, 'stock':items}
    template = "stock/editwarehouse.html"
    return render(request, template, context)

  @login_required
  def invoice(request, stockid):
    item = Invoice.objects.get(pk=stockid)
    Orderss = item.Orders.all()
    error_f = 0 
    if not item.final: 
     items = Stock.objects.filter(company = request.user.cauth.company)
     if request.method == 'POST':     
        if request.POST.get('save') == 'add':
                  instance = Order(stock_id = request.POST['ID'] ,Model = request.POST['Model'],Quantity = request.POST['Quantity'],Size = request.POST['Size'],Name = request.POST['Name'],Price = request.POST['Price'],Color = request.POST['Color'],Warehouse =  request.POST['Warehouse'] )
                  instance.company = request.user.cauth.company
                  instance.fy = request.user.fyauth.year 
                  instance.save()
                  item.Orders.add(instance)
                  item.numberoforders += 1
                  item.save()
                  item.amount += int(instance.Price)
        elif request.POST.get('save') == 'save':
            tot = 0
            for ite in Orderss:
             ite.Size = request.POST['Size_' + str(ite.id)]
             ite.Quantity = request.POST['Quantity_' + str(ite.id)]
             ite.Price = request.POST['Price_' + str(ite.id)]
             ite.save()
             tot += int(ite.Quantity) * int(ite.Price)

            item.amount = tot
            item.save()
        elif request.POST.get('save') == 'finalize' and (item.Itype == "Credit Bill" or item.Itype == "Cash"):
            tot = 0
            valid = True
            for ite in Orderss:
             ite.Size = request.POST['Size_' + str(ite.id)]
             ite.Quantity = request.POST['Quantity_' + str(ite.id)]
             ite.Price = request.POST['Price_' + str(ite.id)]
             ite.save()
             tot += int(ite.Quantity) * int(ite.Price)
             x = Stock.objects.get(id = ite.stock_id)
             if x.Quantity >= int(ite.Quantity):
                 x.Quantity -= int(ite.Quantity)
                 x.save()
             else: 
                 valid = False
                 error_f = "Not Enough Stock"
            if item.Itype == "Credit Bill":
              ty = Receipt(Cost_Center= item.Cost_Center,Date= item.Date,Amount = tot,company= item.company, fy = item.fy, money_account = Cost_Center.objects.get(Name='Cash',company = item.company))
              ty.save()
            elif item.Itype == "Cash":
              ty = Receipt(Cost_Center= Cost_Center.objects.get(Name='Cash',company = item.company),Date= item.Date,Amount = tot,company= item.company, fy = item.fy, money_account = Cost_Center.objects.get(Name='Cash',company = item.company))
              ty.save()

      
            
            tr = Receipt(Cost_Center= Cost_Center.objects.get(Name='Sales Register',company = item.company),Date= item.Date,Amount = tot,company= item.company, fy = item.fy, money_account = Cost_Center.objects.get(Name='Cash',company = item.company))
            tr.save()



            if valid:
                item.amount = tot
                item.final = True
                item.save()
                return HttpResponseRedirect(reverse_lazy('editinvoice', kwargs={'stockid': stockid}))
            else:
                template = "invoices/editinvoices.html"
                context = {'items':items,'stock':Orderss, 'item':item, 'form':error_f} 
                return render(request, template, context)

     template = "invoices/editinvoices.html"
     context = {'items':items,'stock':Orderss, 'item':item} 
    elif item.final:
         template = "invoices/viewinvoice.html"
         context = {'stock':Orderss, 'item':item} 

    
    return render(request, template, context)   

  @login_required
  def purchase(request, stockid):
    item = Purchase.objects.get(pk=stockid)
    if request.method == 'POST':
        form = Purchaseadder(request.user.cauth.company,request.POST, instance = item)
        if form.is_valid():
              if request.POST['save'] == "save":
                  form.save()
                  return HttpResponseRedirect(reverse_lazy("vouchers"))
              elif request.POST['save'] == "delete":
                  item.delete() 
                  return HttpResponseRedirect(reverse_lazy("vouchers"))
              
    else:
      
      form = Purchaseadder(request.user.cauth.company,instance = item)

    context = {'form':form}
    template = "bills/editbill.html"
    return render(request, template, context)  

  @login_required
  def receipt(request, stockid):
    item = Receipt.objects.get(pk=stockid)
    if request.method == 'POST':
        form = Receiptadder(request.user.cauth.company,stockid,request.POST, instance = item)
        if form.is_valid():
              if request.POST['save'] == "save":
                  form.save()
                  return HttpResponseRedirect(reverse_lazy("vouchers"))
              elif request.POST['save'] == "delete":
                  item.delete() 
                  return HttpResponseRedirect(reverse_lazy("vouchers"))
              
    else:
      
      form = Receiptadder(request.user.cauth.company,stockid,instance = item)

    context = {'form':form}
    template = "bills/editcredit.html"
    return render(request, template, context)   
   
  @login_required 
  def goodsreturn(request, stockid):
    item = Invoice.objects.get(pk=stockid)
    Orderss = item.Orders.all()
    if request.method == 'POST':
        tot = 0
        for ite in Orderss:
             ini = ite.Quantity
             ite.Quantity = request.POST['Quantity_' + str(ite.id)]
             ite.save()
             x = Stock.objects.get(id = ite.stock_id)
             diff = ini - int(ite.Quantity)
             x.Quantity += diff
             x.save()
             tot += int(ite.Quantity) * int(ite.Price)
        if item.Itype == "Credit Bill":
              ty = Receipt(Name = item.name,Cost_Center= item.Cost_Center,Date= item.Date,Amount = tot,company= item.company, fy = item.fy)
              ty.save()
        elif item.Itype == "Cash":
              ty = Receipt(Name = item.name,Cost_Center= Cost_Center.objects.get(Name='Cash',company = item.company),Date= item.Date,Amount = tot,company= item.company, fy = item.fy)
              ty.save()
    else:
      
      form = Receiptadder(request.user.cauth.company,instance = item)







    template = "invoices/goodsreturn.html"
    context = {'stock':Orderss, 'item':item} 
    return render(request, template, context)  

  @login_required
  def dlsheet(request,stockid):
      return render(request, 'DailySheets/Editdlsheet.html', {'stock': dlsheet.objects.get(id=stockid)})
  
  


class Reports:
    
    def amount_calculator(z_credits,fy,company):
        debit_amounts = []
        total_amount = 0
        for xrd in z_credits:
            name = xrd.name
            id = xrd.id
            x_amount = 0
            z = xrd.Ledger.filter(company = company)  
            for d in z:
                print(d.name)
                l = d.Cost_Center.filter(company = company)
                for u in l:
                    p = u.Purchase.filter(company = company,fy = fy)
                    r = u.Receipt.filter(company = company,fy = fy)
                    if id == 15:
                       print(p)
                       print(r)
                    for e in p:
                        x_amount -= e.Amount
                    for i in r:
                        x_amount += i.Amount
            debit_amounts.append([x_amount,name,id])
            total_amount += x_amount
        return [debit_amounts,total_amount]

    def balancesheet(request):
        stock = default_group.objects.filter(user= request.user)
        debits = stock.filter(type__in=['Current Liabilities','Loans(Liability)','Capital Account'])
        credits = stock.filter(type__in=['Current Assets','Fixed Assets','Investments'])
     
        fy = request.user.fyauth.year
        company = request.user.cauth.company
        x = Reports.amount_calculator(debits,fy,company)
        y = Reports.amount_calculator(credits,fy,company)
        tot = x[1] + y[1]



        context = {'debits': x[0],'credits': y[0], 'dt':x[1],'ct':y[1],'tot':tot}
        template = "Reports/bill.html"
        return render(request, template, context)  

    def pnl(request):
        stock = default_group.objects.filter(user= request.user)
        debits = stock.filter(type__in=['Direct Expenses','Indirect Expenses','Purchase Accounts'])
        credits = stock.filter(type__in=['Indirect Incomes','Sales Account'])
        fy = request.user.fyauth.year
        company = request.user.cauth.company
        
        x = Reports.amount_calculator(debits,fy,company)
        y = Reports.amount_calculator(credits,fy,company)
        tot = x[1] + y[1]



        context = {'debits': x[0],'credits': y[0], 'dt':x[1],'ct':y[1],'tot':tot}
        template = "Reports/pnl.html"
        return render(request, template, context)  

