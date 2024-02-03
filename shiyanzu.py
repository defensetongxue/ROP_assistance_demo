import shutil
import os,json

def copy_all_files(src_folder, dst_folder, map_list, index_disc):
    """
    Copies all files from src_folder (and its subdirectories) to dst_folder.
    Sequentially names the files and stores the mapping in map_list.
    """
    os.makedirs(dst_folder, exist_ok=True)
    cnt=0
    for root, dirs, files in sorted(os.walk(src_folder)):
        dirs.sort()  # Sort directories
        for file in sorted(files):  # Sort files
            src_path = os.path.join(root, file)
            dst_path = os.path.join(dst_folder, f'{index_disc[cnt]}.jpg')
            shutil.copy2(src_path, dst_path)
            map_list[src_path] = dst_path
            cnt += 1
            
from PIL import Image, ImageDraw, ImageFont
import os
import shutil

def draw_label(src_path, dst_path, prediction):
    """
    Copies all files from src_folder (and its subdirectories) to dst_folder.
    Sequentially names the files, writes prediction on them, and stores the mapping in map_list.
    """
    font_path = './arial.ttf'  # Path to the arial.ttf font file
    font_size = 40
    font = ImageFont.truetype(font_path, font_size)  # Load the custom font
    file=os.path.basename(src_path)
    with Image.open(src_path) as img:
        draw = ImageDraw.Draw(img)
        text = f"prediction: {str(prediction[file])}"
        draw.text((10, 10), text, (255, 255, 255), font=font)  # Position (10,10) and white color
        img.save(dst_path)
            

# Paths for source folders
folder_1_image = './experiments/random_seed_1/image'
folder_2_stage = './experiments/random_seed_2/stage'
folder_2_ridge = './experiments/random_seed_2/ridge'
folder_2_image = './experiments/random_seed_2/image'
folder_2_enhance = './experiments/random_seed_2/enhance'
with open('./map_list.json','r') as f:
    map_list=json.load(f)
with open('./model_prediction.json','r') as f:
    preds=json.load(f)
for src_path in map_list:
    if 'visual' in map_list[src_path]:
        draw_label(src_path,map_list[src_path],preds)
    else:
        shutil.copy(src_path,map_list[src_path])
    
# os.makedirs('./data',exist_ok=True)
# os.system('rm -rf ./data/*')
# map_list={}
# index_disc=[i for i in range(1,51)]
# from random import shuffle
# shuffle(index_disc)
# # Copy operations
# copy_all_files(folder_1_image, './data/folder_1',map_list,index_disc)
# shuffle(index_disc)
# with open('./model_prediction.json','r') as f:
#     preds=json.load(f)
# copy_all_files(folder_2_enhance, './data/enhance',map_list,index_disc)
# draw_label(folder_2_stage, './data/visual',map_list,index_disc,preds)
# copy_all_files(folder_2_ridge, './data/ridge',map_list,index_disc)
# copy_all_files(folder_2_image, './data/folder_2',map_list,index_disc)
# # draw_label(folder_2_image, './data/folder_2',map_list,index_disc,preds)
# with open('./data/map_list.json','w') as f:
#     json.dump(map_list,f)
# print("Copy operations completed successfully.")
