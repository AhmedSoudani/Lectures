from django.shortcuts import render
import markdown2
from . import util
import os
from django.conf import settings


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki_page_view(request, title):
    title = title + '.md'
    try:
        html = markdown2.markdown(title)
    except FileNotFoundError:
        return render(request, "encyclopedia/Page_error")
    title = title.replace('.md', '')
    return render(request, "encyclopedia/wiki_page.html", {
            'title': title,
            'content' : html
        })
def check(title):
    entries = util.list_entries()
    if title in entries:
        return False
    else:
        return True 
