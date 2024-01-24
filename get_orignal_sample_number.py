import os
import json

# Load model predictions from JSON file
def load_predictions(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

# Define the rule for assigning zones
zone_rule = [[0, 5, 5, 5],
             [4, 1, 7, 8],
             [4, 6, 2, 8],
             [4, 6, 7, 3]]

# Function to assign images to zones based on predictions and labels
def assign_to_zones(model_predictions, zone_rule):
    zones = {i: [] for i in range(9)}
    for image_name, data in model_predictions.items():
        pred, label = data["pred"], data["label"]
        zone = zone_rule[pred][label]
        zones[zone].append(image_name)
    return zones

# Load the model predictions
model_predictions = load_predictions('./model.json')

# Assign images to zones
zones = assign_to_zones(model_predictions, zone_rule)

# The 'zones' dictionary now contains the images categorized by zones
# print(zones)
for zone in zones:
    print(len(zones[zone]))
import math

# Calculate total number of images
total_images = sum(len(zone_images) for zone_images in zones.values())

# Function to calculate sample numbers for each zone
def calculate_samples(zones, total_images, total_samples=50):
    samples = {}

    # Calculate and round up sample numbers for zones 1-8
    for zone, images in zones.items():
        if zone != 0:
            proportion = len(images) / total_images
            samples[zone] = math.ceil(total_samples * proportion)

    # Adjust sample number for zone 0
    samples[0] = total_samples - sum(samples.values())

    return samples

# Calculate the sample numbers
sample_numbers = calculate_samples(zones, total_images)

print(sample_numbers)
# {1: 5, 2: 2, 3: 1, 4: 3, 5: 1, 6: 3, 7: 2, 8: 1, 0: 32}
# after human modify as th zone 0 is meaningless.
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
