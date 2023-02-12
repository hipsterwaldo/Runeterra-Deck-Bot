from PIL import Image

def merge_images(image_list):
    # Open images and store them in a list
    total_width = 0
    max_height = 0
    # find the width and height of the final image
    for img in image_list:
        total_width += img.size[0]
        max_height = max(max_height, img.size[1])
    # create a new image with the appropriate height and width
    new_img = Image.new('RGB', (total_width, max_height))
    # Write the contents of the new image
    current_width = 0
    for img in image_list:
        new_img.paste(img, (current_width,0))
        current_width += img.size[0]
    # Save the image
    new_img.save('NewImage.jpg')