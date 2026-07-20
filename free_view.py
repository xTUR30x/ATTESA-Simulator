import pygame
import math
import random

class FreeDriveView:
    def __init__(self):
        self.particles = []

    def update_movement(self, car):
        car.angle += car.steering * (car.speed * 0.15)
        car.x += car.speed * math.sin(math.radians(car.angle))
        car.y -= car.speed * math.cos(math.radians(car.angle))
        
        # Wrap de bordes de pantalla
        if car.x > 1920: car.x = 0
        if car.x < 0: car.x = 1920
        if car.y > 1080: car.y = 0
        if car.y < 0: car.y = 1080

        # --- GESTIÓN DE PARTÍCULAS DE HUMO ---
        if (car.rear_slip > 4.0 or car.handbrake) and car.speed > 0.5:
            rad = math.radians(car.angle)
            back_x = car.x - 30 * math.sin(rad)
            back_y = car.y + 30 * math.cos(rad)

            for _ in range(2):
                p_x = back_x + random.uniform(-8, 8)
                p_y = back_y + random.uniform(-8, 8)
                p_radius = random.uniform(2, 5)
                p_alpha = random.randint(100, 180)
                p_vx = -math.sin(rad) * 0.5 + random.uniform(-0.3, 0.3)
                p_vy = math.cos(rad) * 0.5 + random.uniform(-0.3, 0.3)
                
                self.particles.append([p_x, p_y, p_radius, p_alpha, p_vx, p_vy])

        for p in self.particles[:]:
            p[0] += p[4]
            p[1] += p[5]
            p[2] += 0.2
            p[3] -= 4
            if p[3] <= 0:
                self.particles.remove(p)

    def draw(self, surface, car):
        # 1. Dibujar las partículas de humo
        for p in self.particles:
            smoke_surf = pygame.Surface((int(p[2]*2), int(p[2]*2)), pygame.SRCALPHA)
            pygame.draw.circle(smoke_surf, (200, 200, 205, p[3]), (int(p[2]), int(p[2])), int(p[2]))
            surface.blit(smoke_surf, (int(p[0] - p[2]), int(p[1] - p[2])))

        # 2. Construir la superficie del coche
        car_surf = pygame.Surface((car.width, car.length), pygame.SRCALPHA)
        
        # Chasis principal
        pygame.draw.rect(car_surf, (70, 75, 80), (0, 0, car.width, car.length), border_radius=6)
        
        # Ruedas Traseras (Rojas si patinan o si el freno de mano está puesto)
        rear_wheel_color = (220, 50, 50) if (car.rear_slip > 2.0 or car.handbrake) else (50, 50, 55)
        pygame.draw.rect(car_surf, rear_wheel_color, (2, 55, 8, 16), border_radius=2)
        pygame.draw.rect(car_surf, rear_wheel_color, (car.width - 10, 55, 8, 16), border_radius=2)
        
        # Ruedas Delanteras (Azules según fuerza ATTESA)
        front_wheel_color = (50, 120, 240) if car.front_torque_pct > 15 else (50, 50, 55)
        pygame.draw.rect(car_surf, front_wheel_color, (2, 10, 8, 16), border_radius=2)
        pygame.draw.rect(car_surf, front_wheel_color, (car.width - 10, 10, 8, 16), border_radius=2)

        # --- CÁLCULO DEL ÁNGULO VISUAL EXTRA POR FRENO DE MANO ---
        # Si tiramos del freno de mano y el volante está girado, añadimos una rotación visual agresiva
        visual_angle = car.angle
        if car.handbrake and car.speed > 0.5:
            # Si steering es negativo (izquierda), resta grados. Si es positivo (derecha), suma grados.
            drift_exaggeration = car.steering * 45.0
            visual_angle += drift_exaggeration

        # Rotar usando el ángulo visual calculado y pintar el coche
        rotated_surf = pygame.transform.rotate(car_surf, -visual_angle)
        new_rect = rotated_surf.get_rect(center=(car.x, car.y))
        surface.blit(rotated_surf, new_rect.topleft)