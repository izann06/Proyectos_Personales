from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    sizes = [256, 128, 64, 48, 32, 16]
    images = []
    
    # Colores
    blood_red = (196, 30, 58, 255)
    blood_highlight = (230, 57, 70, 200)
    blood_shadow = (139, 0, 0, 255)
    
    for size in sizes:
        # Fondo transparente total
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        # Para mejorar el antialiasing, dibujamos al cuádruple de tamaño y luego reducimos
        scale = 4
        big_size = size * scale
        big_img = Image.new('RGBA', (big_size, big_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(big_img)
        
        # Geometría de la gota gigante (ocupa casi todo el icono)
        cx = big_size // 2
        
        # El centro de la bola inferior
        cy = int(big_size * 0.65)
        radius = int(big_size * 0.3)
        
        # El pico superior de la gota
        top_y = int(big_size * 0.05)
        
        # Puntos del triángulo que forma la punta de la gota
        # Hacemos una curva bezier o un polígono
        left_x = cx - radius
        right_x = cx + radius
        
        # Dibujar polígono superior (punta de la gota)
        points = [
            (cx, top_y),
            (right_x, cy),
            (left_x, cy)
        ]
        
        # Sombra
        draw.polygon([(x, y+scale*2) for x, y in points], fill=blood_shadow)
        draw.ellipse([left_x, cy - radius + scale*2, right_x, cy + radius + scale*2], fill=blood_shadow)
        
        # Gota principal
        draw.polygon(points, fill=blood_red)
        draw.ellipse([left_x, cy - radius, right_x, cy + radius], fill=blood_red)
        
        # Brillo sutil (forma de medialuna)
        highlight_rect = [cx - int(radius*0.6), cy - int(radius*0.6), cx - int(radius*0.2), cy + int(radius*0.2)]
        draw.pieslice(highlight_rect, 180, 270, fill=blood_highlight)
        
        # Reducir imagen con Lanczos (máxima calidad antialiasing)
        img = big_img.resize((size, size), Image.Resampling.LANCZOS)
        images.append(img)
    
    # Guardar como .ico
    icon_path = os.path.join(os.path.dirname(__file__), "app_hd.ico")
    images[0].save(
        icon_path,
        format='ICO',
        sizes=[(s, s) for s in sizes],
        append_images=images[1:]
    )
    print(f"Icono HD creado: {icon_path}")
    return icon_path

if __name__ == "__main__":
    create_icon()
