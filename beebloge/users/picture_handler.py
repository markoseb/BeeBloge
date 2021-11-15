# users/picture_handler.py

import os
from PIL import Image
from flask import current_app


def add_pic(pic_upload, username_post,folder_name,pic_size=(200, 200)):
    filename = pic_upload.filename
    # "mypicture.jpg"
    ext_type = filename.split('.')[-1]
    # "username.jpg"
    username_post= ''.join([i if (ord(i) < 128 and i!=' ') else '-' for i in username_post])#delete all non asci
    storage_filename = str(username_post) + '.' + ext_type

    filepath = os.path.join(current_app.root_path, f'static/{folder_name}', storage_filename)

    output_size = pic_size

    pic = Image.open(pic_upload)
    pic.thumbnail(output_size)
    pic.save(filepath)

    return storage_filename

def del_pic(fileName,folder_name='product_pics'):

    filepath = os.path.join(current_app.root_path, f'static/{folder_name}', fileName)

    if os.path.exists(filepath):
        os.remove(filepath)