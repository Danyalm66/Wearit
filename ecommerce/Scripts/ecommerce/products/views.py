from django.shortcuts import render
from django.core.paginator import Paginator
from django.conf import settings
import pymongo
import re
client = pymongo.MongoClient("localhost",27017)
db=client.scraped_data.all_brands


# Create your views here.

def get_random():
    li=list(db.find().sort([("Price", pymongo.ASCENDING)]))
    return li
random_products=get_random()

def categories():
    raw_data=get_random()
    all_categories=[]
    for doc in raw_data:
        if doc.get('cat_name') not in all_categories:
            all_categories.append(doc.get('cat_name'))

    return all_categories
categories=categories()

def brands():
    raw_data=random_products
    all_brands=[]
    for doc in raw_data:
        if doc.get('Brand') not in all_brands:
            all_brands.append(doc.get('Brand'))

    return all_brands
brands=brands()

def count_brands(li):
    raw_data=li
    all_brands=[]
    for doc in raw_data:
        if doc.get('Brand') not in all_brands:
            all_brands.append(doc.get('Brand'))

    return len(all_brands)
def pagination(request,doc):
    paginator=Paginator(doc,15)
    page=request.GET.get('page')
    doc=paginator.get_page(page)
    return doc



def index(request):
    template='products/home.html'
    documents=pagination(request,random_products)
    return render(request,template)




def filter_form(request):
     if request.method == 'GET':
        query_dict=request.GET
        select_brands= query_dict.__getitem__('searched')
        price_range=query_dict.__getitem__('range').split('-')
        
        min_price=int(re.search(r'([\D]+)([\d,]+)',price_range[0]).group(2).replace(',',''))
        max_price=int(re.search(r'([\D]+)([\d,]+)',price_range[-1]).group(2).replace(',',''))
        listOfDocumets=[]
        
        listOfDocumets=list(db.find({'$or' :[{'title': {'$regex': "(?i)"+select_brands} ,'Price': { '$gte': min_price,
        '$lte':  max_price }} , {'Brand': {'$regex': "(?i)"+select_brands} ,'Price': { '$gte': min_price,
        '$lte':  max_price }} , {'cat_name': {'$regex': "(?i)"+select_brands} ,'Price': { '$gte': min_price,
        '$lte':  max_price }}]}).sort([("Price", pymongo.ASCENDING)]))
        if len(listOfDocumets)>0:
            paginated_data=pagination(request,listOfDocumets)
            return render(request, 'products/products.html',{"documents": paginated_data, 'searched': select_brands,'Total_products':len(listOfDocumets), "count_brands":count_brands(listOfDocumets), 'min_price':listOfDocumets[0]['Price'], 'max_price':listOfDocumets[-1]['Price']})
        else:
            return render(request,'products/errorpage.html')
        
def search_query(request):
    if request.method == 'GET':
        query_dict=request.GET
        select_brands= query_dict.__getitem__('search')
        if select_brands!='':
            listOfDocumets=list(db.find({'$or' :[{'title': {'$regex': "(?i)"+select_brands}} , {'Brand': {'$regex': "(?i)"+select_brands}} , {'cat_name': {'$regex': "(?i)"+select_brands}}]}).sort([("Price", pymongo.ASCENDING)]))
            if len(listOfDocumets)>0:
                documents=pagination(request,listOfDocumets)
                return render(request, 'products/products.html',{"documents": documents, 'searched': select_brands,'Total_products':len(listOfDocumets), "count_brands":count_brands(listOfDocumets), 'min_price':listOfDocumets[0]['Price'], 'max_price':listOfDocumets[-1]['Price']})
            else:
                return render(request,'products/errorpage.html')
        
        else:
            return(index(request))


def range(min_price,max_price, cat):
    listOfDocumets=list(cat)
    if min_price!='':
        listOfDocumets=list(filter(lambda item:item.get('Price') >= int(min_price),listOfDocumets))
    if max_price!='':
        listOfDocumets=list(filter(lambda item:item.get('Price') <= int(max_price),listOfDocumets))
    return listOfDocumets

def error(request,exception=None):
   
    return render(request,'products/errorpage.html')
