import os,json
from shutil import copy
import random
from utils import visual_mask,draw_bbox
data_path= '../autodl-tmp/dataset_ROP/'
tar_path="../autodl-tmp/guoPan/AssitDemo/"
os.makedirs(tar_path,exist_ok=True)
os.system(f"rm -rf {tar_path}/*")
with open(data_path+'/annotations.json','r') as f:
    data_dict=json.load(f)
    
#
image_name_list=[]
cnt=0
for image_name in data_dict:
    data= data_dict[image_name]
    if "stage_result" in data and len(data["stage_result"]['points'])>0 and 'ridge' in data:
        image_name_list.append(image_name)
        cnt+=1
        if cnt>4:
            break
## begin
total_cnt=len(image_name_list)
print(total_cnt)
idx_shuffle_list=[i for i in range(cnt)]
random.shuffle(idx_shuffle_list)
cnt=0
for i in range(total_cnt):
    image_name=image_name_list[i]
    data=data_dict[image_name]
    copy(data['image_path'],
                      tar_path+f"{str(idx_shuffle_list[i])}.jpg")
    copy(data['image_path'],
                      tar_path+f"{str(i+total_cnt)}.jpg")
    copy(data['enhanced_path'],
                      tar_path+f"{str(i+total_cnt*2)}.jpg")
    visual_mask(data['image_path'],data['ridge_seg']["ridge_seg_path"],
                save_path=tar_path+f"{str(i+total_cnt*3)}.jpg")
    draw_bbox(data['image_path'],data['stage_result']['points'],data['stage_result']['box_width'],
              tar_path+f"{str(i+total_cnt*4)}.jpg",data['stage_result']['values'])