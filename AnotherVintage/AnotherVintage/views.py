from copy import copy
from django import db
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import pymongo
from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm
from .forms import ProductForm
import random
import PIL
from datetime import datetime
import time
import os
from PIL import Image


def dbconn():
    connect_string = 'mongodb://root:rootpassword@127.0.0.1:27017' 
    my_client = pymongo.MongoClient(connect_string)
    db = my_client["AnotherVintage"]
    return db

def index(request):
    
    return render(request, 'home.html')

def shop(request):
    db = dbconn()
    rawprods = list(db["stock"].find({"status":"stocked"}))
    # Format products to presented by page
    for i in range(len(rawprods)):
        rawprods[i]["id"] = rawprods[i]["_id"]
        rawprods[i].pop("_id")
    return render(request,"shop.html",
    {"products":rawprods })

def stock_control(request):
    if not request.user.is_authenticated:
        if not request.user.groups.filter(name='controller').exists():
            return redirect("account")
    db = dbconn()
    rawprods = list(db["stock"].find())
    for i in range(len(rawprods)):
        rawprods[i]["id"] = rawprods[i]["_id"]
    form = ProductForm()
    if request.method=="POST":
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            # Process input data for database use
            _id = form.cleaned_data["_id"]
            name = form.cleaned_data["name"]
            colour = form.cleaned_data["colour"]
            bought_at = float(form.cleaned_data["bought_at"])
            price = float(form.cleaned_data["price"])
            size = form.cleaned_data["size"]
            brand = form.cleaned_data["brand"]
            img = form.cleaned_data["image"]
            conv = Image.open(img)
            nextid = 0
            # Either check provided ID valid or generate next available ID
            for prod in rawprods:
                if _id == None:
                    if prod["_id"] >= nextid:
                        nextid = prod["_id"] + 1
                else:
                    if prod["_id"] == _id:
                        form = ProductForm()
                        return render(request,"stock_control.html",{"products":rawprods,"form":form,"warning":"ID in use"})
            # Database submission and saving of image
            if _id == None:
                db["stock"].insert_one({"_id":nextid,"name":name,"colour":colour,"bought_at":bought_at,
                "brand":brand,"status":"stocked","size":size,"price":price,"stocked_at": datetime.today().replace(microsecond=0)})
                conv.save(f"{settings.MEDIA_ROOT}{nextid}.jpg","JPEG")
            else:
                db["stock"].insert_one({"_id":_id,"name":name,"colour":colour,"bought_at":bought_at,
                "brand":brand,"status":"stocked","size":size,"price":price,"stocked_at": datetime.today().replace(microsecond=0)})
                conv.save(f"{settings.MEDIA_ROOT}{_id}.jpg","JPEG")
            form = ProductForm()
            return render(request,"stock_control.html",{"products":rawprods,"form":form,"warning":"success"})
        else:
            # Invalid Form
            
            return render(request,"stock_control.html",{"products":rawprods,"form":form})
    else:
        
        return render(request,"stock_control.html",{"products":rawprods,"form":form})
def about(request):
    return render(request,"about.html")
def account(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='controller').exists():
            return redirect("stock")
        else:
            db =dbconn()
            uid = dict(db["auth_user"].find_one({"username":str(request.user)}))
            uid = uid["_id"]
            uncomplete = db["orders"].find({"userID":uid,"status":"uncomplete"})
            if list(uncomplete) != []:
                db["orders"].delete_one({"_id":uncomplete[0]["_id"]})
            pids = db["orders"].find({"userID":uid})
            prods = []
            for pid in pids:
                temp = db["stock"].find_one({"_id":pid["stockID"]})
                temp["bought_at"] = pid["sold"]
                prods.append(temp.copy())
            return render(request,"account.html",{"orders":prods})
    else:        
        return redirect("index")

def individual_stock(request,pid):
    if not request.user.is_authenticated:
        if not request.user.groups.filter(name='controller').exists():
            return redirect("account")
    db = dbconn()
    product = db["stock"].find_one({"_id":pid})
    product["id"] = product["_id"]
    if request.method == "POST":
        if request.POST.get("attr") in product.keys() and request.POST.get("attr") != "_id":
            db["stock"].update_one({"_id":pid},{ "$set": { request.POST.get("attr") : request.POST.get("val") } })
            product = db["stock"].find_one({"_id":pid})
            product["id"] = product["_id"]
    return render(request,"stock.html",{"product":product})
def delete(request,pid):
    if not request.user.is_authenticated:
        if not request.user.groups.filter(name='controller').exists():
            return redirect("account")
    db = dbconn()
    db["stock"].delete_one({"_id":pid})
    os.remove(f"{settings.MEDIA_ROOT}{pid}.jpg")
    return redirect("/account")
@csrf_exempt
def payment_done(request):
    db = dbconn()
    uid = dict(db["auth_user"].find_one({"username":str(request.user)}))
    order = db["orders"].find_one({"userID":uid,"status":"uncomplete"})
    db["orders"].update_one({"userID":uid,"status":"uncomplete"},{ "$set" : {"status":"completed"}})
    db["stock"].update_one({"_id":order["stockID"]},{"$set":{"status":"sold"}})
    return render(request, 'success.html')


@csrf_exempt
def payment_canceled(request):
    db = dbconn()
    uid = dict(db["auth_user"].find_one({"username":str(request.user)}))
    uncomplete = db["orders"].find({"userID":uid,"status":"uncomplete"})
    db["orders"].delete_one({"_id":uncomplete[0]["_id"]})
    return render(request, 'paypal_cancel.html')

def prodpage(request,itemno):
    db = dbconn()
    if request.method == "POST":
        host = request.get_host()
        rawprod = db["stock"].find_one({"_id":itemno})
        userid = dict(db["auth_user"].find_one({"username":str(request.user)}))["_id"]
        uncomplete = db["orders"].find({"userID":userid,"status":"uncomplete"})
        if uncomplete != {}:
             db["orders"].delete_one({"_id":uncomplete[0]["_id"]})

        db["orders"].insert_one({"userID":userid,"stockID":itemno,"status":"uncomplete","sold": datetime.today().replace(microsecond=0)})
        orderID = db["orders"].find_one({"userID":userid,"stockID":itemno})["_id"]
        paydict = {
            "business": 'sb-ksklz9099109@business.example.com',
            "amount": rawprod["price"],
            "currency_code": "GBP",
            "item_name": rawprod["name"],
            "invoice": orderID,
            'notify_url': 'http://{}{}'.format(host,
                                           reverse('paypal-ipn')),
            'return_url': 'http://{}{}'.format(host,
                                           reverse('payment_done')),
            'cancel_return': 'http://{}{}'.format(host,
                                              reverse('payment_cancelled')),

        }
        form = PayPalPaymentsForm(initial=paydict)
        if not request.GET._mutable:
            request.GET._mutable = True
        request.GET["oid"] = orderID
        return render(request,"payment.html",{"form":form})
    else:
        
        rawprod = db["stock"].find_one({"_id":itemno})
        if rawprod == None:
            return redirect("/shop")
        if rawprod["status"] == "sold":
            return render(request,"sold.html")
        product = {"id":itemno,"price":rawprod["price"],"size":rawprod["size"],"name":rawprod["name"],"listed_since":rawprod["stocked_at"]}
        return render(request,"product.html",{"product":product})