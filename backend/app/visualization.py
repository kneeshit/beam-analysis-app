import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import io
import base64
from typing import List, Tuple
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

def draw_beam(length: float, support1: float, support2: float, 
              f1: List[List[float]], f2: List[List[float]], 
              f3: List[List[float]], f4: List[List[float]]) -> str:
    """
    Draw beam schematic and return as base64 encoded image
    """
    image = Image.new("RGB", (400, 400), "pink")
    draw = ImageDraw.Draw(image)
    
    # Draw the beam
    rectangle_coords = [(50, 190), (350, 210)]
    draw.rectangle(rectangle_coords, outline="black", fill=(246, 167, 89), width=2)
    
    # Draw the supports
    X = [support1 * 300 / length + 50, support2 * 300 / length + 50]
    y = 210
    side = 30
    for x in X:
        draw.polygon([
            x, y, 
            x - side * np.cos(np.pi/3), y + side * np.cos(np.pi/6), 
            x + side * np.cos(np.pi/3), y + side * np.cos(np.pi/6)
        ], fill=(174, 94, 14), outline='black', width=2)
    
    # Draw point moments
    for moment in f1:
        moment_location = moment[1] * 300 / length + 50
        bounding_box = (moment_location - 25, 175, moment_location + 25, 225)
        start_angle = -130
        end_angle = 130
        value = str(round(abs(moment[0]), 2))
        draw.arc(bounding_box, start=start_angle, end=end_angle, fill="black", width=3)
        draw.text([moment_location, 150], value, fill="black")
        
        if moment[0] < 0:
            draw.line([moment_location - 16.07, 219.151, moment_location - 16.07, 229.151], fill='black', width=3)
            draw.line([moment_location - 16.07, 219.151, moment_location - 6.07, 213.151], fill='black', width=3)
        else:
            draw.line([moment_location - 16.07, 180.849, moment_location - 6.07, 186.849], fill='black', width=3)
            draw.line([moment_location - 16.07, 180.849, moment_location - 16.07, 170.849], fill='black', width=3)
    
    # Draw point forces
    for force in f2:
        load_location = force[1] * 300 / length + 50
        value = str(round(abs(force[0]), 2))
        draw.text([load_location, 130], value, fill="black")
        
        if force[0] < 0:
            draw.line([load_location, 155, load_location, 190], fill='black', width=3)
            draw.line([load_location + 0.5, 190, load_location + 15 * np.cos(np.pi/4), 190 - 15 * np.sin(np.pi/4)], fill='black', width=3)
            draw.line([load_location + 0.5, 190, load_location - 15 * np.cos(np.pi/4), 190 - 15 * np.sin(np.pi/4)], fill='black', width=3)
        else:
            draw.line([load_location, 155, load_location, 190], fill='black', width=3)
            draw.line([load_location + 0.5, 155, load_location + 15 * np.cos(np.pi/4), 155 + 15 * np.sin(np.pi/4)], fill='black', width=3)
            draw.line([load_location + 0.5, 155, load_location - 15 * np.cos(np.pi/4), 155 + 15 * np.sin(np.pi/4)], fill='black', width=3)
    
    # Draw constant force profiles
    for profile in f3:
        load_start_location = profile[1] * 300 / length + 50
        load_end_location = profile[2] * 300 / length + 50
        value = str(round(abs(profile[0]), 2))
        draw.rectangle([(load_start_location, 155), (load_end_location, 190)], outline="black", fill=(163, 163, 163, 40), width=2)
        draw.text([(load_end_location + load_start_location) / 2, 130], value, fill="black")
        
        if profile[0] < 0:
            draw.line([load_start_location + 0.5, 190, load_start_location + 15 * np.cos(np.pi/4), 190 - 15 * np.sin(np.pi/4)], fill='black', width=3)
            draw.line([load_start_location + 0.5, 190, load_start_location - 15 * np.cos(np.pi/4), 190 - 15 * np.sin(np.pi/4)], fill='black', width=3)
            draw.line([load_end_location + 0.5, 190, load_end_location + 15 * np.cos(np.pi/4), 190 - 15 * np.sin(np.pi/4)], fill='black', width=3)
            draw.line([load_end_location + 0.5, 190, load_end_location - 15 * np.cos(np.pi/4), 190 - 15 * np.sin(np.pi/4)], fill='black', width=3)
        else:
            draw.line([load_start_location + 0.5, 155, load_start_location + 15 * np.cos(np.pi/4), 155 + 15 * np.sin(np.pi/4)], fill='black', width=3)
            draw.line([load_start_location + 0.5, 155, load_start_location - 15 * np.cos(np.pi/4), 155 + 15 * np.sin(np.pi/4)], fill='black', width=3)
            draw.line([load_end_location + 0.5, 155, load_end_location + 15 * np.cos(np.pi/4), 155 + 15 * np.sin(np.pi/4)], fill='black', width=3)
            draw.line([load_end_location + 0.5, 155, load_end_location - 15 * np.cos(np.pi/4), 155 + 15 * np.sin(np.pi/4)], fill='black', width=3)
    
    # Draw triangular force profiles
    for profile in f4:
        load_start_location = profile[1] * 300 / length + 50
        load_end_location = profile[2] * 300 / length + 50
        slope = 55 / (load_end_location - load_start_location) if load_end_location != load_start_location else 0
        value = str(round(abs(profile[0]), 2))
        draw.polygon([
            load_start_location, 190, 
            load_end_location, 190 - slope * (load_end_location - load_start_location), 
            load_end_location, 190
        ], outline="black", fill=(163, 163, 163, 40), width=2)
        draw.text([load_end_location, 115], value, fill="black")
        
        if profile[0] < 0:
            draw.line([load_end_location + 0.5, 190, load_end_location + 15 * np.cos(np.pi/4), 190 - 15 * np.sin(np.pi/4)], fill='black', width=3)
            draw.line([load_end_location + 0.5, 190, load_end_location - 15 * np.cos(np.pi/4), 190 - 15 * np.sin(np.pi/4)], fill='black', width=3)
        else:
            draw.line([load_end_location + 0.5, 190, load_end_location + 15 * np.cos(np.pi/4), 155 + 15 * np.sin(np.pi/4)], fill='black', width=3)
            draw.line([load_end_location + 0.5, 190, load_end_location - 15 * np.cos(np.pi/4), 155 + 15 * np.sin(np.pi/4)], fill='black', width=3)
    
    # Convert to base64
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    
    return f"data:image/png;base64,{image_base64}"

def create_engineering_plot(x_data: List[float], y_data: List[float],
                          title: str, xlabel: str, ylabel: str,
                          support1: float, support2: float) -> str:
    """
    Create engineering diagram (shear force, bending moment, etc.) and return as base64
    """
    plt.figure(figsize=(10, 6))
    plt.plot(x_data, y_data, 'b-', linewidth=2)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.axhline(0, color='red', linestyle='-', alpha=0.7)
    plt.axvline(support1, color='green', linestyle='--', alpha=0.7, label='Support 1')
    plt.axvline(support2, color='black', linestyle='--', alpha=0.7, label='Support 2')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()

    # Convert to base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    plt.close()  # Important: close the figure to free memory

    return f"data:image/png;base64,{image_base64}"
