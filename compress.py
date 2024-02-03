import os
from PIL import Image

def resize_image(file_path, output_size=(800, 600)):
    with Image.open(file_path) as img:
        img = img.resize(output_size, Image.ANTIALIAS)
        img.save(file_path)

def process_directory(directory):
    for folder in os.listdir(directory):
        if folder.endswith('.json'):
            continue
        for filename in os.listdir(os.path.join(directory,folder)):
            if filename.endswith('.jpg'):
                file_path = os.path.join(directory,folder,filename)
                resize_image(file_path)

if __name__ == "__main__":
    data_directory = './data'
    process_directory(data_directory)
    print("Image resizing completed.")
