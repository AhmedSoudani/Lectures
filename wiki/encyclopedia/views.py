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
