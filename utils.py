from PIL import Image,ImageDraw,ImageFont
import random
import numpy as np
def visual_mask(image_path, mask_path,save_path='./tmp.jpg'):
    # Open the image file.
    image = Image.open(image_path).convert("RGBA")  # Convert image to RGBA
    # Create a blue mask.
    mask=Image.open(mask_path).convert('L')
    mask_np = np.array(mask)/255
    mask_blue = np.zeros((mask_np.shape[0], mask_np.shape[1], 4), dtype=np.uint8)  # 4 for RGBA
    mask_blue[..., 2] = 255  # Set blue channel to maximum
    mask_blue[..., 3] = (mask_np * 127.5).astype(np.uint8)  # Adjust alpha channel according to the mask value

    # Convert mask to an image.
    mask_image = Image.fromarray(mask_blue)

    # Overlay the mask onto the original image.
    composite = Image.alpha_composite(image, mask_image)
    # Define font and size.
    rgb_image = composite.convert("RGB")
    # Save the image with mask to the specified path.
    rgb_image.save(save_path)

def draw_bbox(image_path, points, width,  save_path, values=None, font_size=40, value_font_size=24):
    # Load the image
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    # Load the font for texts and values
    font_path = './arial.ttf'
    value_font = ImageFont.truetype(font_path, value_font_size)

    # Draw the squares if there are points
    if points:
        if len(points) > 3:
            points = random.sample(points, 3)
            if values is not None:
                values = random.sample(values, 3)

        for i, (x, y) in enumerate(points):
            # Define the position of the squares
            top_left = (x - width // 2, y - width // 2)
            bottom_right = (x + width // 2, y + width // 2)
            # Draw the squares
            draw.rectangle([top_left, bottom_right], outline="green", width=5)
            
            # Draw the values on the top left of the square
            if values is not None:
                # print(values[i])
                value=round(values[i], 2)
                # print(value)
                val_text = str(value)
                # Calculate position for the text
                val_x, val_y = top_left
                draw.text((val_x, val_y - value_font_size), val_text, fill="yellow", font=value_font)
    # Save the image
    img.save(save_path)
