from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from markdown2 import Markdown
from . import util
from django import forms
from random import randint

class AddForm(forms.Form):
    title = forms.CharField(label="Title", max_length=100)
    content = forms.CharField(widget=forms.Textarea, label="Content(md supported)", max_length=2500)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def show(request, title):
    # print(title)
    if title in util.list_entries():
        markdowner = Markdown()
        return render(request, "encyclopedia/show.html", {
            "entry": markdowner.convert(util.get_entry(title)), 
            "title": title
        })
    else:
        return render(request, "encyclopedia/notFound.html", {
            "title": title
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
                "form": form
            })
    else:
        form=AddForm()
    return render(request, "encyclopedia/add.html", {
        "form": AddForm()
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
                "form": form
            })
    else:
        initial_dict = {
            "title": title,
            "content": content
        }
        form=AddForm(initial=initial_dict)
    return render(request, "encyclopedia/edit.html", {
        'form': form
    })


