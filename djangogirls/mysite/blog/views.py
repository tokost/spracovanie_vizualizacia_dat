from django.shortcuts import render

# Create your views here.
def post_list(request):     # ziadost
    return render(request, 'blog/post_list.html', {})   # skombinuje danu sablonu s requestom a vrati to ako odpoved