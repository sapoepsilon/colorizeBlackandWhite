# -*- coding: utf-8 -*-
"""Untitled1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1hAZH24KZKlbEGVD85Vt4GYQ9db9DaZaQ
"""

!git clone https://github.com/jantic/DeOldify.git DeOldify

cd DeOldify

#NOTE:  This must be the first call in order to work properly!
from deoldify import device
from deoldify.device_id import DeviceId
#choices:  CPU, GPU0...GPU7
device.set(device=DeviceId.GPU0)

import torch

if not torch.cuda.is_available():
    print('GPU not available.')

!pip install voila

!pip install -r colab_requirements.txt

import fastai
from deoldify.visualize import *

torch.backends.cudnn.benchmark = True

import ipywidgets as widgets
from ipywidgets import interact, interactive, fixed, interact_manual

!mkdir 'models'
!wget https://www.dropbox.com/s/usf7uifrctqw9rl/ColorizeStable_gen.pth?dl=0 -O ./models/ColorizeStable_gen.pth

!wget https://media.githubusercontent.com/media/jantic/DeOldify/master/resource_images/watermark.png -O ./resource_images/watermark.png



colorizer = get_image_colorizer(artistic=False)

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



def colorizer_func (source_url, render_factor):
      isOnce = True
      if isOnce:
        image_path = colorizer.plot_transformed_image_from_url(url=source_url, render_factor=render_factor, compare=True, watermarked=True)
        show_image_in_notebook(image_path)
        isOnce = False

# DISPLAY BUTTON  

out = widgets.Output()

def on_button_clicked(event):
  with out:
     if name.value is not None and name.value !='':
       colorizer_func(name.value, grand.value)
     else:
       print('Provide an image url and try again.')

text = widgets.HTML(value="Please provide text to colorize picture: ")
left_box = widgets.VBox([text, name])
renderText = widgets.HTML(value="Please select the render factor: ")
second_row = widgets.VBox([renderText, grand])
vbox_result = widgets.VBox([left_box, second_row, button, out])
vbox_result

# linking button and function together using a button's method
# displaying button and its output together
