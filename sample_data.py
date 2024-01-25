import json,os
data_path='../autodl-tmp/dataset_ROP'
with open(os.path.join(data_path,'annotations.json'),'r') as f:
    data_dict=json.load(f)
with open('./model_prediction.json','r') as f:
    model_predictions=json.load(f)
label_gt={}
for image_name in model_predictions:
    label_gt[image_name]=data_dict[image_name]['stage']
# Define the rule for assigning zones
zone_rule = [[0, 5, 5, 5],
             [4, 1, 7, 8],
             [4, 6, 2, 8],
             [4, 6, 7, 3]]

# Function to assign images to zones based on predictions and labels
def assign_to_zones(model_predictions, zone_rule):
    zones_map={}
    for image_name in model_predictions:
        pred, label = model_predictions[image_name], label_gt[image_name]
        zone = zone_rule[pred][label]
        zones_map[image_name]=zone
    return zones_map

zones_map=assign_to_zones(model_predictions,zone_rule)

sample_for_zone= {
    0:19,
    1:8,
    2:5,
    3:3,
    4:4,
    5:2,
    6:4,
    7:3,
    8:2
}

import random
import shutil

def sample_and_save_images(zones_map, sample_for_zone, data_dict, num_seeds=5):
    base_dir = './experiments'
    os.makedirs(base_dir, exist_ok=True)

    for seed in range(1, num_seeds + 1):
        random.seed(seed)
        seed_dir = os.path.join(base_dir, f"random_seed_{seed}")
        os.makedirs(seed_dir, exist_ok=True)

        # Directories for stage, image, and ridge data
        visual_dir = os.path.join(seed_dir, "stage")
        image_dir = os.path.join(seed_dir, "image")
        ridge_dir = os.path.join(seed_dir, "ridge")
        os.makedirs(visual_dir, exist_ok=True)
        os.makedirs(image_dir, exist_ok=True)
        os.makedirs(ridge_dir, exist_ok=True)

        for zone, num_samples in sample_for_zone.items():
            # Create zone directories in visual, image, and ridge folders
            zone_visual_dir = os.path.join(visual_dir, str(zone))
            zone_image_dir = os.path.join(image_dir, str(zone))
            zone_ridge_dir = os.path.join(ridge_dir, str(zone))
            os.makedirs(zone_visual_dir, exist_ok=True)
            os.makedirs(zone_image_dir, exist_ok=True)
            os.makedirs(zone_ridge_dir, exist_ok=True)

            images_in_zone = [img for img, z in zones_map.items() if z == zone]
            sampled_images = random.sample(images_in_zone, min(num_samples, len(images_in_zone)))

            for image_name in sampled_images:
                # Determine source paths
                src_path_visual = data_dict[image_name].get('visual_stage_path', data_dict[image_name]['image_path'])
                src_path_image = data_dict[image_name]['image_path']
                src_path_ridge = data_dict[image_name].get('ridge_visual_path', data_dict[image_name]['image_path'])

                # Copy files to respective directories
                dest_path_visual = os.path.join(zone_visual_dir, os.path.basename(image_name))
                dest_path_image = os.path.join(zone_image_dir, os.path.basename(image_name))
                dest_path_ridge = os.path.join(zone_ridge_dir, os.path.basename(image_name))
                shutil.copy(src_path_visual, dest_path_visual)
                shutil.copy(src_path_image, dest_path_image)
                shutil.copy(src_path_ridge, dest_path_ridge)


# Call the function with the required parameters
sample_and_save_images(zones_map, sample_for_zone, data_dict)
