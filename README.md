# ATTESA E-TS Digital Telemetry Simulator

Un simulador interactivo en 2D desarrollado en Python y Pygame enfocado en la recreación matemática y visual del legendario sistema de tracción integral inteligente **ATTESA E-TS** (Advanced Total Traction Engineering System for All-Terrain Electronic Torque Split) de Nissan.

El proyecto permite analizar en tiempo real cómo la computadora distribuye el par motor entre los ejes delantero y trasero en función de la pérdida de adherencia, inercias laterales y la intervención del freno de mano en distintas superficies.

## Características Principales

*   **Lógica Digital ATTESA E-TS:** Simulación activa de reparto de torque en tiempo real. El vehículo opera como tracción trasera (RWD) por defecto y acopla dinámicamente el eje delantero (hasta un 50%) al detectar deslizamiento o sobreviraje.
*   **Física Avanzada de Derrape:** Modelo dinámico que calcula fuerzas laterales, deslizamiento del eje posterior (`rear_slip`) e inercia por guiñada.
*   **Freno de Mano Dinámico:** Bloqueo simulado del eje trasero que genera desbalances proporcionales a la velocidad real del coche y fuerza la respuesta correctora del sistema de tracción.
*   **Panel de Telemetría Global:** HUD a alta resolución (1080p) con barras de progreso digitales que muestran el porcentaje exacto de torque en cada eje, niveles de agarre y lecturas del acelerador.
*   **Vista de Detalle Avanzada:** Módulo gráfico complementario que incluye:
    *   *Vista Cenital:* Renderizado a gran escala con vectores dinámicos de inercia y guiñada en las ruedas.
    *   *Vista Horizontal:* Silueta de perfil del chasis con vectores de tracción lineales en ambos ejes.
*   **Selector de Superficies:** Simulación física de coeficientes de fricción variables: Seco (100% agarre), Lluvia (50% agarre) e Hielo (15% agarre).

## Controles del Simulador

*   **`M` / Clic Pestaña 1:** Modo Libre Conducción.
*   **`N` / Clic Pestaña 2:** Modo Vista de Detalle (Telemetría extendida).
*   **`↑` / `↓`:** Acelerador y Reversa.
*   **`←` / `→`:** Dirección / Giro del volante.
*   **`ESPACIO`:** Freno de Mano (Bloqueo del eje trasero).
*   **`1`, `2`, `3`:** Cambiar superficie (Seco, Mojado, Hielo).

## Requisitos de Instalación

Asegúrate de tener instalado Python y la biblioteca Pygame:

```bash
pip install pygame