from django.shortcuts import render,redirect
from . import util
from markdown2 import Markdown
import random


    
#Markdown to HTML Conversion   
def convert_mk_to_html(title):
    content=util.get_entry(title)
    markdown=Markdown()
    if content == None:
        return None
    else:
        return markdown.convert(content)

#Index Page
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
    
    
#Entry Page    
def entry(request ,title):
    html_content=convert_mk_to_html(title)
    if html_content == None:
        return render(request, "encyclopedia/error.html" , {
            'msg':'the page not found'
        })
    else:
        return render(request , "encyclopedia/EntryPage.html" , {
            'title':title,
            'content':html_content,
        })
        
#Search       
def search(request):
    if request.method == 'POST':
        entry_search=request.POST['q'] 
        content=convert_mk_to_html(entry_search)
        if content != None:
            return render(request , "encyclopedia/EntryPage.html" , {
            'title':entry_search,
            'content':content,
           })
        else:
            suggestion=[]
            entries=util.list_entries()  
            for entry in entries:
                if  entry_search.lower()  in entry.lower():
                    suggestion.append(entry)
            return render(request , "encyclopedia/SearchPage.html" , {
                'suggestion':suggestion
            })  
            
#New Page            
def new(request):
    if request.method == "GET":
        return render(request , "encyclopedia/NewPage.html")   
    else:
        title=request.POST['title']  
        content=request.POST['content']  
        ExistTitle=util.get_entry(title)  
        if ExistTitle is not None:
            return render(request ,"encyclopedia/error.html", {
                'msg':'Entry aleardy Exists'
            })  
        else:
            util.save_entry(title,content)  
            html_content=convert_mk_to_html(title)
            return render(request,"encyclopedia/EntryPage.html",{
                'title':title,
                'content':html_content,
            } )         
                    
#Edit Page
def edit(request):
    if request.method =='POST':
        title=request.POST['entry_title'] 
        content=util.get_entry(title) 
        return render(request ,"encyclopedia/EditPage.html" ,{
            'title':title,
            'content':content,
        })  
        
def save_edit(request):
    if request.method == 'POST':
        title=request.POST['title']
        content=request.POST['content']  
        util.save_entry(title , content) 
        html_content=convert_mk_to_html(title)
        return render(request,"encyclopedia/EntryPage.html",{
                'title':title,
                'content':html_content,
            } )       
          
#Random Page          
def randy(request):  
    entries=util.list_entries()
    random_entry=random.choice(entries)
    html_content=convert_mk_to_html(random_entry)
    return render(request,"encyclopedia/EntryPage.html",{
                'title':random_entry,
                'content':html_content,
            } ) 
            
          
  

