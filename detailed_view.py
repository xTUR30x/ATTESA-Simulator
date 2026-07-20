import pygame
import math

class DetailedView:
    def __init__(self):
        self.font = pygame.font.SysFont("Arial", 16)
        self.font_bold = pygame.font.SysFont("Arial", 18, bold=True)
        self.font_large = pygame.font.SysFont("Arial", 26, bold=True)

    def draw(self, surface, car):
        section_title = self.font_large.render("ANÁLISIS DINÁMICO ESTÁTICO (ATTESA E-TS)", True, (240, 140, 40))
        surface.blit(section_title, (40, 75))


        pygame.draw.rect(surface, (50, 50, 55), (50, 130, 880, 600), border_radius=10)
        lbl_box1 = self.font_bold.render("VISTA SUPERIOR (Dirección y Derrape)", True, (255, 255, 255))
        surface.blit(lbl_box1, (80, 150))
        self._draw_top_down_static(surface, car, 490, 430)
        

        pygame.draw.rect(surface, (50, 50, 55), (990, 130, 880, 600), border_radius=10)
        lbl_box2 = self.font_bold.render("VISTA HORIZONTAL (Vectores de Tracción)", True, (255, 255, 255))
        surface.blit(lbl_box2, (1020, 150))
        self._draw_side_view(surface, car, 1430, 430)
        
        # Leyenda de vectores
        pygame.draw.line(surface, (220, 50, 50), (550, 420), (590, 420), 4)
        pygame.draw.line(surface, (50, 120, 240), (550, 460), (590, 460), 4)
        surface.blit(self.font.render("Torque Eje Trasero", True, (255, 255, 255)), (600, 412))
        surface.blit(self.font.render("Torque Eje Delantero", True, (255, 255, 255)), (600, 452))

    def _draw_top_down_static(self, surface, car, center_x, center_y):
        """Dibuja el coche desde arriba a gran escala con vectores de dirección."""
        car_w = 100
        car_l = 240
        
        # Crear superficie temporal para rotar el chasis según la dirección del volante
        car_surf = pygame.Surface((car_w, car_l), pygame.SRCALPHA)
        
        # Chasis principal
        pygame.draw.rect(car_surf, (80, 85, 90), (0, 0, car_w, car_l), border_radius=12)
        
        # Ruedas traseras fijas
        r_color = (220, 50, 50) if (car.rear_slip > 2.0 or car.handbrake) else (40, 40, 45)
        pygame.draw.rect(car_surf, r_color, (5, 180, 20, 40), border_radius=4)
        pygame.draw.rect(car_surf, r_color, (car_w - 25, 180, 20, 40), border_radius=4)
        
        # Ruedas delanteras que rotan con el volante
        f_color = (50, 120, 240) if car.front_torque_pct > 15 else (40, 40, 45)
        wheel_surf = pygame.Surface((20, 40), pygame.SRCALPHA)
        pygame.draw.rect(wheel_surf, f_color, (0, 0, 20, 40), border_radius=4)
        
        # Rotación de ruedas delanteras
        rot_wheel = pygame.transform.rotate(wheel_surf, -car.steering * 45)
        
        # Acoplar ruedas delanteras al chasis
        car_surf.blit(rot_wheel, rot_wheel.get_rect(center=(15, 40)))
        car_surf.blit(rot_wheel, rot_wheel.get_rect(center=(car_w - 15, 40)))
        
        # Dibujar chasis en la pantalla principal
        surface.blit(car_surf, car_surf.get_rect(center=(center_x, center_y)))
        
        # --- VECTOR DE INERCIA / DERRAPE TRASERO ---
        if car.rear_slip > 0.5:
            # Dibujamos una flecha roja gruesa que muestra hacia dónde desliza la cola
            slip_angle = car.steering * -60
            rad = math.radians(slip_angle)
            end_x = center_x + 120 * math.sin(rad)
            end_y = center_y + 100 + 120 * math.cos(rad) 
            
            pygame.draw.line(surface, (220, 50, 50), (center_x, center_y + 80), (end_x, end_y), 6)
            pygame.draw.circle(surface, (220, 50, 50), (int(end_x), int(end_y)), 8)

    def _draw_side_view(self, surface, car, center_x, center_y):
        """Dibuja el perfil del coche a gran escala mostrando el reparto de torque en tiempo real."""
        pygame.draw.line(surface, (100, 100, 105), (center_x - 400, center_y + 100), (center_x + 400, center_y + 100), 4)
        
        # Chasis lateral estilizado proporcional a la nueva pantalla (Largo 500, Alto 120)
        body_points = [
            (center_x - 250, center_y + 40),  # Parachoques trasero
            (center_x - 230, center_y - 20),  # Maletero
            (center_x - 100, center_y - 30),  # Luneta trasera
            (center_x - 40,  center_y - 70),  # Techo atrás
            (center_x + 80,  center_y - 70),  # Techo alante
            (center_x + 150, center_y - 20),  # Parabrisas
            (center_x + 240, center_y - 20),  # Capó
            (center_x + 260, center_y + 40),  # Parachoques delantero
            (center_x + 240, center_y + 70),  # Spoiler delantero
            (center_x - 240, center_y + 70)   # Faldón trasero
        ]
        pygame.draw.polygon(surface, (60, 65, 70), body_points)
        pygame.draw.polygon(surface, (200, 200, 205), body_points, 3) # Contorno
        
        # Pasos de rueda gigantes
        pygame.draw.circle(surface, (30, 30, 35), (center_x - 140, center_y + 70), 55)
        pygame.draw.circle(surface, (30, 30, 35), (center_x + 140, center_y + 70), 55)
        
        # Ruedas gigantes (Radio 45)
        pygame.draw.circle(surface, (20, 20, 25), (center_x - 140, center_y + 70), 45)
        pygame.draw.circle(surface, (20, 20, 25), (center_x + 140, center_y + 70), 45)
        # Llantas internas
        pygame.draw.circle(surface, (150, 150, 160), (center_x - 140, center_y + 70), 25, 4)
        pygame.draw.circle(surface, (150, 150, 160), (center_x + 140, center_y + 70), 25, 4)
        
        # --- VECTORES DINÁMICOS DE TRACCIÓN (FLECHAS GIGANTES) ---
        # Fuerza proporcional al torque y al acelerador
        force_factor = car.throttle * 2.5 
        
        # Eje Trasero (Rojo)
        rear_torque_len = car.rear_torque_pct * force_factor
        if rear_torque_len > 5:
            # Dibujar flecha hacia adelante desde la rueda trasera
            start_p = (center_x - 140, center_y + 70)
            end_p = (center_x - 140 + rear_torque_len, center_y + 70)
            pygame.draw.line(surface, (220, 50, 50), start_p, end_p, 8)
            pygame.draw.polygon(surface, (220, 50, 50), [
                (end_p[0], end_p[1] - 10), 
                (end_p[0], end_p[1] + 10), 
                (end_p[0] + 15, end_p[1])
            ])
            
        # Eje Delantero (Azul)
        front_torque_len = car.front_torque_pct * force_factor
        if front_torque_len > 5:
            # Dibujar flecha hacia adelante desde la rueda delantera
            start_p = (center_x + 140, center_y + 70)
            end_p = (center_x + 140 + front_torque_len, center_y + 70)
            pygame.draw.line(surface, (50, 120, 240), start_p, end_p, 8)
            pygame.draw.polygon(surface, (50, 120, 240), [
                (end_p[0], end_p[1] - 10), 
                (end_p[0], end_p[1] + 10), 
                (end_p[0] + 15, end_p[1])
            ])