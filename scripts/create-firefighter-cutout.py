import numpy as np
from PIL import Image

def make_cutout():
    img = Image.open('images/bombeiro-oficial.jpg').convert('RGBA')
    arr = np.array(img, dtype=np.float32)
    
    # Calculate luminance or distance from pure white (255, 255, 255)
    r, g, b, a = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2], arr[:, :, 3]
    
    # White background threshold
    # Pixels where r, g, b are all close to 255 are background
    min_rgb = np.minimum(np.minimum(r, g), b)
    
    # Alpha mask: if min_rgb > 248 -> 0, if min_rgb < 210 -> 255, smooth in between
    alpha = np.clip((252 - min_rgb) / (252 - 215) * 255, 0, 255)
    
    # For dark/colored firefighter areas, ensure alpha is 255
    # The firefighter has saturated orange/yellow/black colors
    color_diff = np.maximum(np.maximum(np.abs(r - g), np.abs(g - b)), np.abs(b - r))
    # Where color_diff > 15, alpha should be 255
    firefighter_mask = np.clip(color_diff / 15 * 255, 0, 255)
    
    final_alpha = np.maximum(alpha, firefighter_mask)
    
    # Also ensure dark pixels (black helmet/straps/tank) have full alpha
    dark_mask = np.clip((180 - min_rgb) / 30 * 255, 0, 255)
    final_alpha = np.maximum(final_alpha, dark_mask)
    
    arr[:, :, 3] = np.clip(final_alpha, 0, 255)
    
    result = Image.fromarray(arr.astype(np.uint8))
    result.save('images/bombeiro-recorte-transparente.png', 'PNG')
    print('Saved images/bombeiro-recorte-transparente.png successfully!')

if __name__ == '__main__':
    make_cutout()
