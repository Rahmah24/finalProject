from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from .models import Items,ItemDetails,Card
from .forms import CreateUserForm,LoginUserForm
from django.contrib.auth import login, logout ,authenticate
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
     template=loader.get_template('index.html')
     return HttpResponse(template.render())
def admin(request):
     template=loader.get_template('admin.py')
     return HttpResponse(template.render())

def showphone(request):
     template=loader.get_template('showphone.html')
     phone=ItemDetails.objects.select_related('itemsid')
     print(phone.query)
     return HttpResponse(template.render({'phone':phone,'request':request}))


def details(request , id):
     template=loader.get_template('details.html')
     currentuser=request.user
     print(currentuser.id)
     phone=ItemDetails.objects.select_related('itemsid').filter(id=id)
     #print(phone.query)

     context={
          'phone':phone,
          'request':request
      }
     return HttpResponse(template.render(context))

@csrf_exempt
def auth_register(request):
     template=loader.get_template('auth_register.html')
     form = CreateUserForm()
     if request.method== "POST":
          form=CreateUserForm(request.POST)
          if form.is_valid():
               form.save()
               return redirect('auth_login')
     context={'registerform':form }
     return HttpResponse(template.render(context=context))

@csrf_exempt
def auth_login(request):
     template=loader.get_template('auth_login.html')
     form = LoginUserForm()
     if request.method== "POST":
          form=LoginUserForm(data=request.POST)
          if form.is_valid():
               username=form.cleaned_data['username']
               password=form.cleaned_data['password']
               user=authenticate(username=username,password=password)
               if user:
                    if user.is_active:
                         login(request,user)
                         return render(request,'index.html')
     context={'form':form }
     return render(request,'auth_login.html',context)
@csrf_exempt
def auth_logout(request):
     if request.method=="POST":
          logout(request)
          return redirect("/")



@login_required(login_url='/auth_login/')
def checkout(request):
     template=loader.get_template('checkout.html')
     current_user = request.user.id
     card = Card.objects.all().filter(Id_user=current_user).first()
     product=Items.objects.get(id=card.Id_product)
     #print(product)
     context={ 
          'card':card,
          'productname':product,
          'request':request
      }
     
     return HttpResponse(template.render(context=context))

def add_to_card(request , id):
     currentuser=request.user
     discounts=2
     state=False
     phone=ItemDetails.objects.select_related('itemsid').filter(id=id)
     for item in phone:
           net=item.total-discounts
     card = Card(
      Id_product=item.id,
      Id_user=currentuser.id,
      price=item.price,
      qty=item.qty,
      tax=item.tax,
      total=item.total,
      discounts=discounts,
      net=net,
      status=state
)
     

     currentuser=request.user.id
     count=Card.objects.filter(Id_user=currentuser).count()
     print(count)
     card.save()
     request.session['countcard']=count
     return redirect("/showphone")
     