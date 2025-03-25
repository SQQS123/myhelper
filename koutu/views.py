import cv2
import numpy as np
from removebg import RemoveBg
from django.shortcuts import render
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from .forms import ImageUploadForm


def koutu_(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_instance = form.save(commit=False)
            image_instance.save()

            # 使用Remove.bg API进行抠图
            rmbg = RemoveBg("your_api_key", "error.log")  # 替换为你的API密钥
            result = rmbg.remove_background_from_img_file(image_instance.original_image.path)
            processed_image_path = image_instance.original_image.path.replace('.jpg', '_processed.png')
            with open(processed_image_path, "wb") as out:
                out.write(result.read())
            
            # 保存处理后的图片路径到模型
            image_instance.processed_image = processed_image_path.replace('original_images/', 'processed_images/')
            image_instance.save()

            return render(request, 'koutu/koutu.html', {'image': image_instance})
    else:
        form = ImageUploadForm()
    return render(request, 'koutu/koutu.html', {'form': form})




def process_image(image_path):
    img = cv2.imread(image_path)
    mask = np.zeros(img.shape[:2], np.uint8)
    bgd_model = np.zeros((1, 65), np.float64)
    fgd_model = np.zeros((1, 65), np.float64)
    
    # 设置矩形区域（可根据实际需求调整）
    rect = (50, 50, 400, 400)
    cv2.grabCut(img, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)
    
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
    img = img * mask2[:, :, np.newaxis]
    
    # 保存处理后的图片
    processed_image_path = image_path.replace('.jpg', '_processed.jpg')
    cv2.imwrite(processed_image_path, img)
    return processed_image_path

def koutu(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_instance = form.save(commit=False)
            image_instance.save()

            # 使用OpenCV进行抠图
            processed_image_path = process_image(image_instance.original_image.path)
            print(processed_image_path)
            # 保存处理后的图片路径到模型
            with open(processed_image_path, 'rb') as f:
                image_instance.processed_image.save(
                    'processed_image.jpg',
                    ContentFile(f.read())
                )
            image_instance.save()

            return render(request, 'koutu/result.html', {'image': image_instance})
    else:
        form = ImageUploadForm()
    return render(request, 'koutu/koutu.html', {'form': form})
