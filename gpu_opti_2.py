import taichi as ti



# Initialisation sur GPU
ti.init(arch=ti.vulkan)

res_x, res_y = 1920, 1200
pixels = ti.Vector.field(3, dtype=ti.f32, shape=(res_x, res_y))
# Champ supplémentaire pour stocker l'image précédente et lisser
accum_buffer = ti.Vector.field(3, dtype=ti.f32, shape=(res_x, res_y))

@ti.func # Fonction à l'interieur du kernel
def n_and_grad(rel_pos, rs):
    r = rel_pos.norm()
    n = 1.0 / ti.sqrt(1.0 - rs / r)
    dn_dr = -rs / (2.0 * (r**2) * (1.0 - rs / r)**1.5)
    grad_n = dn_dr * (rel_pos / r)
    return n, grad_n


@ti.kernel  # Code compilé par taichi et envoyé sur GPU (appelé par code python)
def render(rs: ti.f32, mouse_x: ti.f32, mouse_y: ti.f32, reset_accum: ti.i32, t: ti.f32):
    # Paramètres caméra
    radius_cam = 8.0
    theta = mouse_x * 6.28 + t
    phi = (mouse_y - 0.5) * 3.14 * 0.95
    
    cam_pos = ti.Vector([
        radius_cam * ti.cos(phi) * ti.sin(theta),
        radius_cam * ti.sin(phi),
        radius_cam * ti.cos(phi) * ti.cos(theta)
    ])
    
    # Cible verrouillée au centre
    target = ti.Vector([0.0, 0.0, 0.0])
    forward = (target - cam_pos).normalized()
    right = forward.cross(ti.Vector([0.0, 1.0, 0.0])).normalized()
    up = right.cross(forward)

    for i, j in pixels:
        # --- SSAA : On ajoute un jitter (tremblement) aléatoire ---
        # Cela permet de calculer des points légèrement différents à chaque frame
        jitter_x = ti.random() - 0.5
        jitter_y = ti.random() - 0.5
        
        uv_x = (2.0 * (i + 0.5 + jitter_x) / res_x - 1.0) * (res_x / res_y)
        uv_y = (2.0 * (j + 0.5 + jitter_y) / res_y - 1.0)
        
        dir = (forward + uv_x * right + uv_y * up).normalized()
        
        r = cam_pos
        v = dir
        color = ti.Vector([0.01, 0.01, 0.04]) # Fond Espace
        ds = 0.04 # Pas d'intégration plus fin pour plus de précision

        # Lancer de rayon (Ray Marching)
        for step in range(600):
            dist = r.norm()
            if dist < 5.0:
                n, grad = n_and_grad(r, rs)
                if n < 0 or dist < rs * 1.05:
                    color = ti.Vector([0, 0, 0])
                    break
                
                # Physique : déviation de la lumière
                dv = (grad - v * v.dot(grad)) / n
                r += v * ds
                v = (v + dv * ds).normalized()
                
                # Disque d'accrétion
                if r.y * (r.y - v.y * ds) <= 0:
                    d = r.norm()
                    if rs * 2.2 < d < 4.2:
                        intensity = ti.exp(-1.6 * (d - 2.8)**2) * 20
                        color = ti.Vector([0.05, 0.30, 1.00]) * intensity #[0.420, 0.482, 1.000] [1.00, 0.30, 0.05]
                        if (d * 12) % 2.0 > 1.8: color *= 0.0
                        break
            else:
                r += v * ds * 2.0
            
            if r.norm() > 25.0:
                # Étoiles procédurales
                if ti.sin(v.x*100) * ti.sin(v.y*30) * ti.sin(v.z*90) > 0.9:
                    color = ti.Vector([1, 1, 1])
                break

        # --- MÉLANGE TEMPOREL (SSAA) ---
        if reset_accum == 1:
            accum_buffer[i, j] = color
        else:
            # On garde 50% de l'ancienne image et 50% de la nouvelle
            # C'est ce qui crée le lissage parfait (Anti-aliasing)
            accum_buffer[i, j] = accum_buffer[i, j] * 0.5 + color * 0.5
        
        pixels[i, j] = accum_buffer[i, j]

# Interface
gui = ti.GUI("Trou Noir", res=(res_x, res_y), fast_gui=True)

last_mouse = [0.0, 0.0]

t = 0
while gui.running:
    t += 0.004  # Vitesse de rotation
    mouse = gui.get_cursor_pos()
    
    # Si la souris bouge, on reset un peu plus fort pour éviter le flou de mouvement
    reset = 0
    if abs(mouse[0] - last_mouse[0]) > 0.01 or abs(mouse[1] - last_mouse[1]) > 0.01:
        reset = 1
    last_mouse = mouse
    
    render(0.5, mouse[0], mouse[1], reset, t)
    
    gui.set_image(pixels)
    gui.show()