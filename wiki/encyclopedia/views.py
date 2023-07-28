from django.shortcuts import render
import markdown2
from . import util
import os
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from urllib.parse import urlencode
import random


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki_page_view(request, title):
    file_path = os.path.abspath(os.path.join("entries", title + '.md'))

    try:
        with open(file_path, 'r') as file:
            markdown_content = file.read()
        html = markdown2.markdown(markdown_content)
    except FileNotFoundError:
        return render(request, "encyclopedia/Page_error.html", {
            "title": title,
        })

    title = title.replace('.md', '')

    return render(request, "encyclopedia/wiki_page.html", {
        'title': title,
        'content': html
    })

def search_result(request):
    query = request.GET.get('q', '').strip()
    entries = util.list_entries()

    results = [entry for entry in entries if query.lower() in entry.lower()]

    return render(request, "encyclopedia/search_result.html", {
        "results" : results,
        "query": query
    })

def new_page(request):
    if request.method == 'POST':
        title = request.POST['titlearea']
        content = request.POST['textarea']
        entries = util.list_entries()

        if title in entries:
            return render(request, "encyclopedia/new_page.html", {
                'title_exists': True,
                'existing_title': title
            })
        html_content = markdown2.markdown(content)
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse("new_page") + "?" + urlencode({
            "title": title,
            "content": html_content
        }))
    return render(request, "encyclopedia/new_page.html")


def random_page(request):
    entries = util.list_entries()
    random_title = random.choice(entries)
    return HttpResponseRedirect(reverse("wiki_page", args=[random_title]))

def edit_page(request, title):
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/Page_error", {
            "title": title
        })
    return render(request, "encyclopedia/edit_page.html", {
        "title": title,
        "content": content
    })

def save_page(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']

        util.save_entry(title, content)

        return HttpResponseRedirect(reverse("wiki_page", args=[title]))
    
    return HttpResponseRedirect(reverse("index"))