from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
import qrcode
import os
from pathlib import Path
from . import forms
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def genhome(request):
    template = loader.get_template("generator/gen1_index.html")
    context = {}
    if request.method == "POST":
            form = forms.GenForm(request.POST)
            # Create a QR code instance
            qr = qrcode.QRCode(
                version=1,  # controls the size of the QR Code
                error_correction=qrcode.constants.ERROR_CORRECT_L,  # controls the error correction used for the QRCode
                box_size=10,
                border=4,  
            )
            # Data to be encoded in the QR code
            data = request.POST.get('data', '')

            qr.add_data(data)
            qr.make(fit=True)

            # Create an image from the QR Code instance
            img = qr.make_image(fill_color="black", back_color="white")

            # Save the image or display it
            BASE_DIR = Path(__file__).resolve().parent.parent
            static_path = os.path.join(BASE_DIR, 'generator')
            img.save(f"{static_path}/static/img/q.png")
            context.update({"qrcodeimage": f"{static_path}/my_qrcode.png"})
            context.update({"form": form})
            
            return HttpResponse(template.render(context, request))
    else:
        form = forms.GenForm()
        context.update({"form": form})
        return HttpResponse(template.render(context, request))
   
    return HttpResponse(template.render())

# Create your views here.
