"""
Genera un icono .ico para Dark Passenger Backup.
Crea un icono con un cuchillo/gota de sangre sobre fondo negro.
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    sizes = [256, 128, 64, 48, 32, 16]
    images = []
    
    for size in sizes:
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Fondo circular oscuro
        margin = int(size * 0.05)
        draw.ellipse(
            [margin, margin, size - margin, size - margin],
            fill=(13, 13, 13, 255),
            outline=(139, 0, 0, 255),
            width=max(1, size // 32)
        )
        
        # Gota de sangre (forma de gota)
        cx = size // 2
        cy = size // 2
        drop_h = int(size * 0.45)
        drop_w = int(size * 0.25)
        
        # Triángulo superior de la gota
        top_y = cy - int(drop_h * 0.5)
        mid_y = cy + int(drop_h * 0.1)
        bottom_y = cy + int(drop_h * 0.5)
        
        # Dibujar la gota con polígono + elipse
        points = [
            (cx, top_y),
            (cx + drop_w, mid_y),
            (cx + drop_w - 2, bottom_y - drop_w // 2),
            (cx - drop_w + 2, bottom_y - drop_w // 2),
            (cx - drop_w, mid_y),
        ]
        draw.polygon(points, fill=(196, 30, 58, 255))
        
        # Parte redonda inferior de la gota
        draw.ellipse(
            [cx - drop_w, mid_y - drop_w // 2, cx + drop_w, bottom_y],
            fill=(196, 30, 58, 255)
        )
        
        # Brillo pequeño en la gota
        highlight_size = max(2, size // 16)
        hx = cx - drop_w // 3
        hy = mid_y + drop_w // 4
        draw.ellipse(
            [hx, hy, hx + highlight_size, hy + highlight_size],
            fill=(230, 57, 70, 200)
        )
        
        images.append(img)
    
    # Guardar como .ico
    icon_path = os.path.join(os.path.dirname(__file__), "app.ico")
    images[0].save(
        icon_path,
        format='ICO',
        sizes=[(s, s) for s in sizes],
        append_images=images[1:]
    )
    print(f"Icono creado: {icon_path}")
    return icon_path

if __name__ == "__main__":
    create_icon()
