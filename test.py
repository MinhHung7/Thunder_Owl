import colorsys

def hex_to_rgb(hex_color):
    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)
    return r, g, b

def rgb_to_hex(rgb_color):
    return "#{:02x}{:02x}{:02x}".format(*rgb_color)

def adjust_brightness(hex_color, factor):
    r, g, b = hex_to_rgb(hex_color)
    
    h, l, s = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
    l = min(1.0, max(0.0, l * factor))
    
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    rgb_color = (int(r * 255), int(g * 255), int(b * 255))
    
    return rgb_to_hex(rgb_color)

# Example
original_color = "#3498db"
highlight_color = adjust_brightness(original_color, 1.2)  # Increase brightness (adjust factor as needed)
print(f"Original color: {original_color}")
print(f"Highlight color: {highlight_color}")