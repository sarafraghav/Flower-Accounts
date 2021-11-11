from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator




class Company(models.Model):
    name = models.CharField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="company")

class financial_year(models.Model):
    year = models.CharField(max_length=1000)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="financial_year")
    

class fyauth(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    year = models.ForeignKey(financial_year,on_delete=models.CASCADE)

class cauth(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    


# Create your models here.

class Warehouse(models.Model):
    name = models.CharField(max_length=200, unique=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="Warehouse")

class Stock(models.Model):
    Model = models.CharField(max_length=100)
    Quantity = models.IntegerField(validators = [MinValueValidator(0)])
    Size = models.CharField(max_length=100)
    Name = models.CharField(max_length=100)
    Price = models.IntegerField()
    Color = models.CharField(max_length=200)
    Warehouse =  models.ForeignKey(Warehouse, on_delete=models.CASCADE, to_field='id', default='1')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="Stock")


        

    
#Multi Group--------------------------------------------------------------


class default_group(models.Model):
    Type_Choices = (("Capital Account","Capital Account"),("Loans(Liability)","Loans(Liability)"),("Current Liabilities","Current Liabilities"),("Fixed Assets","Fixed Assets"),("Investments","Investments"),("Current Assets","Current Assets"),("Branch Divisions","Branch Divisions"),("Suspense AC","Suspense AC"),("Sales Account","Sales Account"),("Purchase Accounts","Purchase Accounts"),("Direct Incomes","Direct Incomes"),("Direct Expenses","Direct Expenses"),("Indirect Incomes","Indirect Incomes"),("Indirect Expenses","Indirect Expenses"))
    df = models.BooleanField()
    type = models.CharField(max_length=100, choices=Type_Choices,default =Type_Choices[0])
    name = models.CharField(max_length=2000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)



class Ledger(models.Model):
    name = models.CharField(max_length = 100)
    df = models.BooleanField()
    cc = models.BooleanField()
    header = models.ForeignKey(default_group, on_delete=models.CASCADE, related_name="Ledger")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="Ledger")
    
    

class Cost_Center(models.Model):
    Name = models.CharField(max_length = 100)
    df = models.BooleanField()
    Description = models.CharField(max_length=50000)
    ltype = models.ForeignKey(Ledger, on_delete= models.CASCADE, related_name="Cost_Center")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="Cost_Center")

#Group---------------------------------------------------------------------

class Order(models.Model):
    Model = models.CharField(max_length=200)
    Quantity = models.IntegerField()
    Size = models.CharField(max_length=100)
    Name = models.CharField(max_length=100)
    Price = models.IntegerField()
    Color = models.CharField(max_length=200)
    Warehouse =  models.CharField(max_length=200)
    stock_id = models.IntegerField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="Order")
    fy = models.ForeignKey(financial_year, on_delete=models.CASCADE, related_name="Order")
    
    

class Invoice(models.Model):
    final = models.BooleanField()
    amount = models.IntegerField()
    Date  = models.DateField()
    Type_Choices = (("Cash","Cash"),("Credit Bill","Credit Bill"),("Goods Return","Goods Return"))
    name = models.CharField(max_length=1000)
    Cost_Center = models.ForeignKey(Cost_Center,on_delete=models.CASCADE, to_field='id', related_name="Invoices" )
    Orders = models.ManyToManyField(Order, related_name="Invoice" )
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="Invoice")
    fy = models.ForeignKey(financial_year, on_delete=models.CASCADE, related_name="Invoice")
    numberoforders = models.IntegerField(default = 0)
    Itype = models.CharField(max_length=100, choices=Type_Choices,default =Type_Choices[0] )
    def orders(self):
        return ', '.join([a.Name for a in self.Orders.all()])

class Receipt(models.Model):
    Cost_Center = models.ForeignKey(Cost_Center, on_delete=models.CASCADE, related_name="Receipt")
    money_account = models.ForeignKey('Cost_Center' ,on_delete=models.CASCADE, related_name="Receipt_money_account")
    Date  = models.DateField()
    Amount = models.IntegerField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="Receipt")
    fy = models.ForeignKey(financial_year, on_delete=models.CASCADE, related_name="Receipt")
    

class Purchase(models.Model):
    Cost_Center = models.ForeignKey(Cost_Center, on_delete=models.CASCADE, related_name="Purchase")
    money_account = models.ForeignKey('Cost_Center', on_delete=models.CASCADE, related_name="Purchase_money_account")
    Date  = models.DateField()
    Amount = models.IntegerField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="Purchase")
    fy = models.ForeignKey(financial_year, on_delete=models.CASCADE, related_name="Purchase")

    
class dlsheet(models.Model):
    Date  = models.DateField()
    Receipts = models.ManyToManyField(Receipt)
    Purchases = models.ManyToManyField(Purchase)
    Invoices = models.ManyToManyField(Invoice)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="dlsheet")
    fy = models.ForeignKey(financial_year, on_delete=models.CASCADE, related_name="dlsheet")
