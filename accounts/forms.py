from django.forms import ModelForm, DateInput
from .models import *
from django.contrib.auth.forms import UserCreationForm  
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):  
        class Meta:  
            model = User  
            fields = ('email', 'first_name', 'last_name', 'username')


class cauthform(ModelForm):
    class Meta:
        model = cauth
        fields = ['company']
        
    def __init__(self, user, *args, **kwargs):
           super(cauthform, self).__init__(*args, **kwargs)
           # without the next line label_from_instance does NOT work
           self.fields['company'].queryset = Company.objects.filter(user = user)
           self.fields['company'].label_from_instance = lambda obj: "%s" % (obj.name)

class fyauthform(ModelForm):
    class Meta:
        model = fyauth
        fields = ['year']
        
    def __init__(self, company ,*args, **kwargs):
           super(fyauthform, self).__init__(*args, **kwargs)
           # without the next line label_from_instance does NOT work
           self.fields['year'].queryset = financial_year.objects.filter(company = company)
           self.fields['year'].label_from_instance = lambda obj: "%s" % (obj.year)


class Stockadder(ModelForm):
    class Meta:
        model = Stock
        fields = ['Name','Model','Size','Color','Quantity','Price','Warehouse']
    def __init__(self,user, *args, **kwargs):
        super(Stockadder, self).__init__(*args, **kwargs)
        # without the next line label_from_instance does NOT work
        self.fields['Warehouse'].queryset = Warehouse.objects.filter(company=user)
        self.fields['Warehouse'].label_from_instance = lambda obj: "%s" % (obj.name)
      
class Warehouseadder(ModelForm):
    class Meta:
        model = Warehouse
        fields = ['name']
    
class Cost_centeradder(ModelForm):
    class Meta:
        model = Cost_Center
        fields = ['Name','Description','ltype']
    def __init__(self, user,*args, **kwargs):
           super(Cost_centeradder, self).__init__(*args, **kwargs)
           # without the next line label_from_instance does NOT work
           self.fields['ltype'].queryset = Ledger.objects.filter(company=user).filter(cc = True)
           self.fields['ltype'].label_from_instance = lambda obj: "%s" % (obj.name)

class Groupadder(ModelForm):
    class Meta:
        model = default_group
        fields = ['name','type']

class ledgerselector(ModelForm):
    class Meta:
        model = Cost_Center
        fields = ['ltype']
    def __init__(self,user, *args, **kwargs):
           super(ledgerselector, self).__init__(*args, **kwargs)
           # without the next line label_from_instance does NOT work
           self.fields['ltype'].queryset = Ledger.objects.filter(company = user)
           self.fields['ltype'].label_from_instance = lambda obj: "%s" % (obj.name)
    

class Ledgeradder(ModelForm):
    class Meta:
        model = Ledger
        fields = ['name','header','cc']
    def __init__(self,user, *args, **kwargs):
           super(Ledgeradder, self).__init__(*args, **kwargs)
           # without the next line label_from_instance does NOT work
           self.fields['header'].queryset = default_group.objects.filter(user = user)
           self.fields['header'].label_from_instance = lambda obj: "%s" % (obj.name)
           self.fields['header'].label = 'Group'
           self.fields['cc'].label = 'Cost Center'
       
class Companyadder(ModelForm):
    class Meta:
        model = Company
        fields = ['name']

class fyadder(ModelForm):
    class Meta:
        model = financial_year
        fields = ['year']

class stocktransferer(ModelForm):
    class Meta:
        model = Stock
        fields = ['Quantity','Warehouse']
    def __init__(self, user,*args, **kwargs):
        super(stocktransferer, self).__init__(*args, **kwargs)
        # without the next line label_from_instance does NOT work
        self.fields['Warehouse'].queryset = Warehouse.objects.filter(company=user)
        self.fields['Warehouse'].label_from_instance = lambda obj: "%s" % (obj.name)


class DateInput(DateInput):
    input_type = 'date'


class invoicemaker(ModelForm):
    class Meta:
        model = Invoice
        fields = ['name','Cost_Center','Itype','Date']
        widgets = {
            'Date': DateInput(),}
    def __init__(self, user,*args, **kwargs):
        super(invoicemaker, self).__init__(*args, **kwargs)
        # without the next line label_from_instance does NOT work
        self.fields['Cost_Center'].queryset = Cost_Center.objects.filter(company = user)
        self.fields['Cost_Center'].label_from_instance = lambda obj: "%s" % (obj.Name)



class Receiptadder(ModelForm):
    class Meta:
        model = Receipt
        fields = ['Cost_Center','money_account','Amount','Date']
        widgets = {
            'Date': DateInput(),}
        
    def __init__(self,user,ledger, *args, **kwargs):
        super(Receiptadder, self).__init__(*args, **kwargs)
        # without the next line label_from_instance does NOT work
        self.fields['Date'].required = False
        self.fields['Cost_Center'].queryset = Cost_Center.objects.filter(company = user, df= False).filter(ltype = ledger)
        self.fields['Cost_Center'].label_from_instance = lambda obj: "%s" % (obj.Name)
        self.fields['money_account'].queryset = Ledger.objects.get(company = user, name= "Money Account").Cost_Center.all()
        self.fields['money_account'].label_from_instance = lambda obj: "%s" % (obj.Name)
    

class Purchaseadder(ModelForm):
    class Meta:
        model = Purchase
        fields = ['Cost_Center','money_account','Amount','Date']
        widgets = {
            'Date': DateInput(),}
        
    def __init__(self, user,ledger, *args, **kwargs):
        super(Purchaseadder, self).__init__(*args, **kwargs)
        # without the next line label_from_instance does NOT work
        self.fields['Date'].required = False
        self.fields['Cost_Center'].queryset = Cost_Center.objects.filter(company = user, df=False).filter(ltype = ledger)
        self.fields['Cost_Center'].label_from_instance = lambda obj: "%s" % (obj.Name)
        self.fields['money_account'].queryset = Ledger.objects.get(company = user, name= "Money Account").Cost_Center.all()
        self.fields['money_account'].label_from_instance = lambda obj: "%s" % (obj.Name)
    



class dlsheetReceiptadder(ModelForm):
    class Meta:
        model = Receipt
        fields = ['Cost_Center','money_account','Amount','Date']
        widgets = {
            'Date': DateInput(),}
        
    def __init__(self,user, *args, **kwargs):
        super(dlsheetReceiptadder, self).__init__(*args, **kwargs)
        # without the next line label_from_instance does NOT work
        self.fields['Date'].required = False
        self.fields['Cost_Center'].queryset = Cost_Center.objects.filter(company = user, df= False)
        self.fields['Cost_Center'].label_from_instance = lambda obj: "%s" % (obj.Name)
        self.fields['money_account'].queryset = Ledger.objects.get(company = user, name= "Money Account").Cost_Center.all()
        self.fields['money_account'].label_from_instance = lambda obj: "%s" % (obj.Name)
    

class dlsheetPurchaseadder(ModelForm):
    class Meta:
        model = Purchase
        fields = ['Cost_Center','money_account','Amount','Date']
        widgets = {
            'Date': DateInput(),}
        
    def __init__(self, user, *args, **kwargs):
        super(dlsheetPurchaseadder, self).__init__(*args, **kwargs)
        # without the next line label_from_instance does NOT work
        self.fields['Date'].required = False
        self.fields['Cost_Center'].queryset = Cost_Center.objects.filter(company = user, df=False)
        self.fields['Cost_Center'].label_from_instance = lambda obj: "%s" % (obj.Name)
        self.fields['money_account'].queryset = Ledger.objects.get(company = user, name= "Money Account").Cost_Center.all()
        self.fields['money_account'].label_from_instance = lambda obj: "%s" % (obj.Name)











class dlsheetadder(ModelForm):
    class Meta:
        model = dlsheet
        fields = ['Date']
        widgets = {
            'Date': DateInput(),}
