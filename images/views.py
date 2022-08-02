from django.shortcuts import render, redirect
from .models import Image
from .forms import ImageUploadForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


@login_required
def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save(commit=False)
            upload.user = request.user
            upload.save()
            messages.success(request, 'Image Uploaded Successfully')
            return redirect(upload.get_absolute_url())

    else:
        form = ImageUploadForm(data=request.GET)
    return render(request, 'images/image_upload.html', {'section': 'images', 'form': form})


def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    return render(request, 'images/image_detail.html',  {'section': 'images', 'image': image})


@login_required()
def my_images(request):
    images = Image.objects.filter(user=request.user)
    page = request.GET.get('page', 1)
    paginator = Paginator(images, 5)

    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        images = paginator.page(paginator.num_pages)
    return render(request, 'images/my_images.html', {'section': 'images', 'images': images})






