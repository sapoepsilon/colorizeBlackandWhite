# -*- coding: utf-8 -*-
"""Untitled1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1hAZH24KZKlbEGVD85Vt4GYQ9db9DaZaQ
"""

!git clone https://github.com/jantic/DeOldify.git DeOldify

!pip install voila
!pip install anvil-uplink

import anvil.server

anvil.server.connect("M23EUBR77WA6L5L5ZXK2RRSZ-MRLXTM7NCLUXNVFA")

cd DeOldify

#NOTE:  This must be the first call in order to work properly!
from deoldify import device
from deoldify.device_id import DeviceId
#choices:  CPU, GPU0...GPU7
device.set(device=DeviceId.GPU0)

import torch

if not torch.cuda.is_available():
    print('GPU not available.')





!pip install -r colab_requirements.txt

import fastai
from deoldify.visualize import *

torch.backends.cudnn.benchmark = True

import ipywidgets as widgets
from ipywidgets import interact, interactive, fixed, interact_manual

!mkdir 'models'
!wget https://www.dropbox.com/s/usf7uifrctqw9rl/ColorizeStable_gen.pth?dl=0 -O ./models/ColorizeStable_gen.pth

!wget https://data.deepai.org/deoldify/ColorizeArtistic_gen.pth -O ./models/ColorizeArtistic_gen.pth

!wget https://media.githubusercontent.com/media/jantic/DeOldify/master/resource_images/watermark.png -O ./resource_images/watermark.png

import anvil.media

colorizer = get_image_colorizer(artistic=True)

grand = widgets.IntSlider(min=7,max=49)
name = widgets.Text(placeholder='Please put url here: ')
file = widgets.FileUpload(
    accept='',  # Accepted file extension e.g. '.txt', '.pdf', 'image/*', 'image/*,.pdf'
    multiple=False  # True to accept multiple files upload else False
)
button = widgets.Button(description='Colorize',
    tooltip='Click me',
    icon='check' # (FontAwesome names without the `fa-` prefix)
    )
uploader = widgets.FileUpload()

import io
from io import BytesIO
@anvil.server.callable
def colorizer_func (source_url, render_factor):
 
        image_path = colorizer.plot_transformed_image_from_url(url=source_url, render_factor=render_factor, compare=True, watermarked=True)
        isOnce = False
        colored = Image.open(image_path)
        byte_io = BytesIO()
        colored.save(byte_io, 'JPEG')
        print(byte_io.getvalue() )
        return anvil.BlobMedia("image/jpeg", byte_io.getvalue() , name='colored image')



import io
from io import BytesIO
from PIL import Image

@anvil.server.callable
def colorizer_func_withFile(file, renderfactor):
  
  image = Image.open(io.BytesIO(file.get_bytes()))
  image.save('/content/DeOldify/newImage.jpg', 'JPEG')
  image_path = colorizer.plot_transformed_image(path='/content/DeOldify/newImage.jpg', render_factor=40, compare=True, watermarked=False)
  colored = Image.open(image_path)
  byte_io = BytesIO()
  colored.save(byte_io, 'JPEG')
  print(byte_io.getvalue() )
  return anvil.BlobMedia("image/jpeg", byte_io.getvalue() , name='colored image')

  


  print(image)
  # os.chdir('/content/DeOldify')
  # p= 'IMAGES/'+ file
  # try:
  #   image_path = colorizer.plot_transformed_image(path=p, render_factor=renderfactor, compare=True, watermarked=False)
  #   colored = Image.open(image_path)
  #   byte_io = BytesIO()
  #   colored.save(byte_io, 'JPEG')
  #   print(byte_io.getvalue() )
  #   return anvil.BlobMedia("image/jpeg", byte_io.getvalue() , name='colored image')
  #   picture = picture.save('COLORIZED_'+image)
  # except:
  #   print(image + ' Is not a supported file type!')


    #   image_object = Image.open(io.BytesIO(file.get_bytes()))
    # p = image_object.
    # image_path = colorizer.plot_transformed_image(path=p, render_factor=renderfactor, compare=True, watermarked=False)
    # colored = Image.open(image_path)
    # byte_io = BytesIO()
    # colored.save(byte_io, 'JPEG')
    # print(byte_io.getvalue() )
    # return anvil.BlobMedia("image/jpeg", byte_io.getvalue() , name='colored image')
    # picture = picture.save('COLORIZED_'+image)



# DISPLAY BUTTON  

out = widgets.Output()

def on_button_clicked(event):
  isOnce = True
  if isOnce:
    with out:
      if name.value is not None and name.value !='':
                show_image_in_notebook(colorizer_func(name.value, grand.value))
      else:
        print('Provide an image url and try again.')

button.on_click(on_button_clicked)
text = widgets.HTML(value="Please provide text to colorize picture: ")
left_box = widgets.VBox([text, name])
renderText = widgets.HTML(value="Please select the render factor: ")
second_row = widgets.VBox([renderText, grand])
vbox_result = widgets.VBox([left_box, second_row, button, out])
vbox_result

# linking button and function together using a button's method
# displaying button and its output together

anvil.server.wait_forever()