import shutil
import os,json

def copy_all_files(src_folder, dst_folder, map_list, cnt):
    """
    Copies all files from src_folder (and its subdirectories) to dst_folder.
    Sequentially names the files and stores the mapping in map_list.
    """
    os.makedirs(dst_folder, exist_ok=True)
    
    for root, dirs, files in sorted(os.walk(src_folder)):
        dirs.sort()  # Sort directories
        for file in sorted(files):  # Sort files
            src_path = os.path.join(root, file)
            dst_path = os.path.join(dst_folder, f'{cnt}.jpg')
            shutil.copy2(src_path, dst_path)
            map_list[src_path] = dst_path
            cnt += 1
    return cnt
# Paths for source folders
folder_1_image = './experiments/random_seed_1/image'
folder_2_stage = './experiments/random_seed_2/stage'
folder_2_ridge = './experiments/random_seed_2/ridge'
folder_2_image = './experiments/random_seed_2/image'
os.makedirs('./data',exist_ok=True)
os.system('rm -rf ./data/*')
map_list={}
cnt=1
# Copy operations
cnt=copy_all_files(folder_1_image, './data/folder_1',map_list,cnt)
copy_all_files(folder_2_image, './data/zone',map_list,cnt)
copy_all_files(folder_2_stage, './data/visual',map_list,cnt)
copy_all_files(folder_2_ridge, './data/ridge',map_list,cnt)
copy_all_files(folder_2_image, './data/folder_2',map_list,cnt)
print(cnt)
with open('./data/map_list.json','w') as f:
    json.dump(map_list,f)
print("Copy operations completed successfully.")
