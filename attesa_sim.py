import pygame
import sys
from free_view import FreeDriveView
from detailed_view import DetailedView

# Inicialización
pygame.init()
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nissan Skyline GT-R R32 - ATTESA E-TS Modular Simulator")
clock = pygame.time.Clock()

# Modos del controlador
FREE_DRIVE = 0
DETAILED_VIEW = 1
current_mode = FREE_DRIVE

class CarData:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0.0
        self.speed = 0.0
        self.width = 40
        self.length = 80
        
        # Variables de estado físicas
        self.front_torque_pct = 0.0
        self.rear_torque_pct = 100.0
        self.rear_slip = 0.0
        self.surface_friction = 1.0
        self.throttle = 0.0
        self.steering = 0.0
        self.handbrake = False

    def update_physics(self, keys):
        # 1. Inputs del usuario (Acelerador y Dirección)
        self.hud_throttle = 1.0 if keys[pygame.K_UP] else -0.3 if keys[pygame.K_DOWN] else 0.0

        if keys[pygame.K_UP]:
            self.throttle = min(self.throttle + 0.01, 1.0)
        elif keys[pygame.K_DOWN]:
            self.throttle = max(self.throttle - 0.02, -0.3)
        else:
            self.throttle *= 0.85
            
        if keys[pygame.K_LEFT]:
            self.steering = max(self.steering - 0.12, -0.6)
        elif keys[pygame.K_RIGHT]:
            self.steering = min(self.steering + 0.12, 0.6)
        else:
            self.steering = 0.0

        # Activar freno de mano con ESPACIO
        self.handbrake = keys[pygame.K_SPACE]

        # Superficies (1: Seco, 2: Lluvia, 3: Hielo)
        if keys[pygame.K_1]: self.surface_friction = 1.0
        if keys[pygame.K_2]: self.surface_friction = 0.5
        if keys[pygame.K_3]: self.surface_friction = 0.15

        # 2. Física avanzada de Derrape por Inercia Lateral
        lateral_force = abs(self.steering) * self.speed
        grip_limit = 3.5 * self.surface_friction
        
        lateral_slip = 0.0
        if lateral_force > grip_limit:
            lateral_slip = (lateral_force - grip_limit) * 3.0

        # 3. Lógica matemática del ATTESA E-TS + FRENO DE MANO
        if self.handbrake:
            if self.speed > 0.5:
                # Al frenar y perder velocidad, el límite dinámico baja automáticamente.
                target_handbrake_slip = (12.0 * (self.speed / 10.0)) / (self.surface_friction + 0.1)
                
                self.rear_slip = min(self.rear_slip + 0.5, max(2.0, target_handbrake_slip))
                
                # Rotación física real suave
                self.angle += self.steering * self.speed * 0.8
            else:
                # Si el carro ya se detuvo casi por completo, el deslizamiento cae a cero
                self.rear_slip = max(0.0, self.rear_slip - 1.0)
        
        elif self.throttle > 0:
            longitudinal_slip = (self.throttle * 12.0) / (self.surface_friction + 0.1)
            self.rear_slip = max(0.0, longitudinal_slip + lateral_slip - self.speed * 0.3)
        else:
            self.rear_slip = max(0.0, lateral_slip - 1.5)

        # Computadora ATTESA
        if self.rear_slip > 0.5:
            self.front_torque_pct = min(50.0, self.rear_slip * 5.0)
        else:
            self.front_torque_pct = max(0.0, self.front_torque_pct - 3.0)
            
        self.rear_torque_pct = 100.0 - self.front_torque_pct

        # 4. Curvas de potencia y velocidad originales 
        if self.handbrake:
            engine_power = 0.0
            self.speed = max(0.0, self.speed - 0.08 * self.surface_friction)
        else:
            engine_power = self.throttle * 3.0 * self.surface_friction
            if self.front_torque_pct > 10:
                engine_power += (self.front_torque_pct / 50.0) * self.throttle * 1.5
                self.rear_slip *= (1.0 - (self.front_torque_pct / 100.0) * 0.15)
        
        self.speed += engine_power - (self.speed * 0.08)

# Instanciación del Modelo y las Vistas
self = CarData(WIDTH // 2, HEIGHT // 2)
free_view = FreeDriveView()
detailed_view = DetailedView()

# Fuentes para el HUD global
font = pygame.font.SysFont("Arial", 16)
font_bold = pygame.font.SysFont("Arial", 18, bold=True)

running = True
while running:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic izquierdo
                    mouse_x, mouse_y = event.pos
                    if 12 <= mouse_y <= 47:
                        if 20 <= mouse_x <= 260:
                            current_mode = FREE_DRIVE
                        elif 280 <= mouse_x <= 520:
                            current_mode = DETAILED_VIEW

            # Cambiar de pantalla con el teclado
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    current_mode = FREE_DRIVE
                elif event.key == pygame.K_n:
                    current_mode = DETAILED_VIEW

            # Cerrar Simulador
            if event.type == pygame.QUIT:
                running = False


    keys = pygame.key.get_pressed()
    
    self.update_physics(keys)

    if current_mode == FREE_DRIVE:
        screen.fill((25, 25, 30))
        free_view.update_movement(self)
        free_view.draw(screen, self)
    else:
        screen.fill((20, 20, 25))
        detailed_view.draw(screen, self)

    # --- PINTAR MENÚ DE PESTAÑAS GLOBAL ---
    pygame.draw.rect(screen, (15, 15, 20), (0, 0, WIDTH, 60))
    
    btn1_color = (240, 140, 40) if current_mode == FREE_DRIVE else (90, 90, 95)
    pygame.draw.rect(screen, btn1_color, (20, 12, 240, 35), border_radius=5)
    screen.blit(font_bold.render("[ M ] Libre Conducción", True, (255, 255, 255)), (42, 20))
    
    btn2_color = (240, 140, 40) if current_mode == DETAILED_VIEW else (90, 90, 95)
    pygame.draw.rect(screen, btn2_color, (280, 12, 240, 35), border_radius=5)
    screen.blit(font_bold.render("[ N ] Vista de Detalle", True, (255, 255, 255)), (305, 20))
    
    # --- PINTAR PANEL DE TELEMETRÍA GLOBAL ---
    pygame.draw.rect(screen, (15, 15, 20), (40, 780, 1840, 240), border_radius=10)
    screen.blit(font_bold.render("TELEMETRÍA ATTESA E-TS", True, (255, 255, 255)), (70, 800))
    
    surface_str = "Seco (100% Agarre)" if self.surface_friction == 1.0 else "Mojado (50% Agarre)" if self.surface_friction == 0.5 else "Hielo (15% Agarre)"
    screen.blit(font.render(f"Superficie [Teclas 1, 2, 3]:  {surface_str}", True, (50, 200, 100)), (70, 840))
    screen.blit(font.render(f"Acelerador / Freno:  {self.throttle*100:.0f}%", True, (255, 255, 255)), (70, 870))
    screen.blit(font.render(f"Deslizamiento Eje Trasero:  {self.rear_slip:.2f}", True, (220, 50, 50) if self.rear_slip > 1 else (255, 255, 255)), (70, 900))
    
    # --- REPARTO DE TRACCIÓN DIGITAL ---
    screen.blit(font_bold.render("REPARTO DE TRACCIÓN DIGITAL", True, (255, 255, 255)), (860, 800))
    dist_str = f"EJE DELANTERO: {self.front_torque_pct:.1f}%   |   EJE TRASERO: {self.rear_torque_pct:.1f}%"
    screen.blit(font_bold.render(dist_str, True, (50, 120, 240) if self.front_torque_pct > 0 else (255, 255, 255)), (860, 835))
    
    # Barras de Progreso
    pygame.draw.rect(screen, (50, 50, 55), (860, 880, 350, 22), border_radius=3)
    pygame.draw.rect(screen, (220, 50, 50), (860, 880, int(self.rear_torque_pct * 3.5), 22), border_radius=3)
    pygame.draw.rect(screen, (50, 50, 55), (860, 920, 350, 22), border_radius=3)
    pygame.draw.rect(screen, (50, 120, 240), (860, 920, int(self.front_torque_pct * 3.5), 22), border_radius=3)

    # --- GUÍA DE CONTROLES DEL SIMULADOR ---
    screen.blit(font_bold.render("CONTROLES", True, (255, 255, 255)), (1380, 800))
    pygame.draw.line(screen, (60, 60, 70), (1380, 825), (1800, 825), 2)
    
    # Leyenda de acciones y teclas
    screen.blit(font.render("Acelerar / Reversa:", True, (180, 180, 185)), (1380, 840))
    screen.blit(font_bold.render("[ ↑ ]  /  [ ↓ ]", True, (240, 140, 40)), (1580, 840))
    
    screen.blit(font.render("Dirección (Giro):", True, (180, 180, 185)), (1380, 870))
    screen.blit(font_bold.render("[ ← ]  /  [ → ]", True, (240, 140, 40)), (1580, 870))
    
    screen.blit(font.render("Freno de Mano:", True, (180, 180, 185)), (1380, 900))
    screen.blit(font_bold.render("[ ESPACIO ]", True, (220, 50, 50) if self.handbrake else (200, 200, 200)), (1580, 900))


    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()