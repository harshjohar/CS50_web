from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from markdown2 import Markdown
from . import util
from django import forms
from random import randint
markdowner = Markdown()
class AddForm(forms.Form):
    title = forms.CharField(label="Title", max_length=100)
    content = forms.CharField(widget=forms.Textarea, label="Content(md supported)", max_length=2500)

class Search(forms.Form):
    item = forms.CharField(widget=forms.TextInput(attrs={'class' : 'myfieldclass', 'placeholder': 'Search'}))

def index(request):
    entries = util.list_entries()
    searched = []
    if request.method == "POST":
        form = Search(request.POST)
        if form.is_valid():
            item = form.cleaned_data["item"]
            for i in entries:
                if item in entries:
                    page = util.get_entry(item)
                    page_converted = markdowner.convert(page)

                    context = {
                        'page': page_converted,
                        'title': item, 
                        'form': Search()
                    }
                    return render(request, 'encyclopedia/show.html', context)
                if item.lower() in i.lower():
                    searched.append(i)
                    context = {
                        'searched': searched,
                        'form': Search()
                    }

            return render(request, 'encyclopedia/search.html', context)
        else:
            return render(request, 'encyclopedia/index.html', {'form': form})
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "form": Search()
        })

def show(request, title):
    # print(title)
    if title in util.list_entries():
        page = util.get_entry(title)
        converted = markdowner.convert(page)
        return render(request, "encyclopedia/show.html", {
            "entry": converted, 
            "title": title,
            'form': Search()
        })
    else:
        return render(request, "encyclopedia/notFound.html", {
            "title": title,
            'form': Search()
        })

def add(request):
    if request.method=="POST":
        form = AddForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            util.save_entry(title, content)
            return redirect("../")
        else:
            return render(request, "encylclopedia/add.html", {
                "add": form,
                'form': Search()
            })
    else:
        form=AddForm()
    return render(request, "encyclopedia/add.html", {
        "add": AddForm(),
        'form': Search()
    })

def random(request):
    list_titles = util.list_entries()
    hi = len(list_titles)
    r = randint(1, hi-1)
    title = list_titles[r]
    page = show(request, title)
    return page


def edit(request, title):
    content = util.get_entry(title)
    if request.method == "POST":
        form = AddForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            util.save_entry(title, content)
            return redirect("../")
        else:
            return render(request, "encylclopedia/edit.html", {
                "edit": form,
                'form': Search()
            })
    else:
        initial_dict = {
            "title": title,
            "content": content,
            'form': Search()
        }
        form=AddForm(initial=initial_dict)
    return render(request, "encyclopedia/edit.html", {
        'edit': form,
        'form': Search()
    })