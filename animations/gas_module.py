"""
Gas Module - Reusable gas visualization for Manim animations

This module provides a Gas class that creates animated gas particles
within a container, with visual properties based on temperature.

Usage:
    from animations.gas_module import Gas

    gas = Gas(width=2.5, height=3.5, temperature=300, num_particles=20)
    self.add(gas)

    # Change temperature
    self.play(gas.animate_temperature(500, run_time=2))
"""

from manim import *
import numpy as np


class Gas(VGroup):
    """
    Rappresentazione animata di un gas con particelle che si muovono casualmente.

    Caratteristiche:
    - Dimensioni variabili (larghezza e altezza)
    - Colore basato sulla temperatura
    - Velocità di movimento proporzionale alla temperatura
    - Particelle che si muovono casualmente all'interno del contenitore

    Parameters:
    -----------
    width : float
        Larghezza del contenitore (default: 2.5)
    height : float
        Altezza del contenitore (default: 3.5)
    temperature : float
        Temperatura in Kelvin (default: 300, influisce su colore e velocità)
    num_particles : int
        Numero di particelle da visualizzare (default: 20)
    particle_radius : float
        Raggio base delle particelle (default: 0.06)
    particle_scale : float
        Scala visuale delle particelle, moltiplicatore per il raggio (default: 1.0)
        Usa valori > 1.0 per particelle più grandi e più visibili
    center : np.ndarray
        Centro del contenitore (default: ORIGIN)
    """

    def __init__(
        self,
        width=2.5,
        height=3.5,
        temperature=300,
        num_particles=20,
        particle_radius=0.06,
        particle_scale=1.0,
        center=ORIGIN,
        **kwargs
    ):
        super().__init__(**kwargs)

        # Use _container_width/_container_height to avoid conflict with VGroup.width/height
        self._container_width = width
        self._container_height = height
        self.temperature = temperature
        self.num_particles = num_particles
        self.particle_radius = particle_radius
        self.particle_scale = particle_scale
        self._container_center = center

        # Create particles
        self.particles = VGroup()
        self._create_particles()

        # Add particles to this VGroup
        self.add(self.particles)

        # Initialize velocities for ideal gas (magnitude proportional to sqrt(T))
        speed = self._get_wiggle_speed()
        self.velocities = []
        for _ in range(num_particles):
            # Random direction, magnitude based on temperature
            angle = np.random.uniform(0, 2 * np.pi)
            velocity = speed * np.array([np.cos(angle), np.sin(angle), 0])
            self.velocities.append(velocity)

        # Add updater for ideal gas motion
        self.add_updater(self._wiggle_updater)

    def _create_particles(self):
        """Create particles distributed within the container bounds."""
        color = self._temperature_to_color()

        # Calculate scaled particle radius
        scaled_radius = self.particle_radius * self.particle_scale

        # Calculate bounds relative to center (with scaled radius)
        left_bound = self._container_center[0] - self._container_width / 2 + scaled_radius
        right_bound = self._container_center[0] + self._container_width / 2 - scaled_radius
        bottom_bound = self._container_center[1] - self._container_height / 2 + scaled_radius
        top_bound = self._container_center[1] + self._container_height / 2 - scaled_radius

        # Create particles at random positions within bounds
        for i in range(self.num_particles):
            x = np.random.uniform(left_bound, right_bound)
            y = np.random.uniform(bottom_bound, top_bound)

            particle = Dot(
                point=[x, y, 0],
                color=color,
                radius=scaled_radius
            )
            self.particles.add(particle)

    def _temperature_to_color(self):
        """
        Mappa la temperatura a un colore:
        - Bassa temperatura (< 300K): blu scuro (BLUE_D)
        - Media temperatura (300-500K): blu/verde
        - Alta temperatura (> 500K): rosso scuro (RED_D)
        """
        if self.temperature < 250:
            return BLUE_E
        elif self.temperature < 300:
            return BLUE_D
        elif self.temperature < 400:
            return interpolate_color(BLUE_D, GREEN_D, (self.temperature - 300) / 100)
        elif self.temperature < 500:
            return interpolate_color(GREEN_D, ORANGE, (self.temperature - 400) / 100)
        else:
            return interpolate_color(ORANGE, RED_D, min((self.temperature - 500) / 300, 1))

    def _get_wiggle_speed(self):
        """
        Calcola la velocità di movimento basata sulla temperatura.
        Velocità direttamente proporzionale alla temperatura (v ∝ T) per chiarezza visiva.
        """
        # Base speed at 300K (room temperature)
        base_speed = 0.15
        # Speed scales linearly with temperature: v(600K) = 2 × v(300K)
        speed_factor = self.temperature / 300
        return base_speed * speed_factor

    def _wiggle_updater(self, mob, dt):
        """
        Updater per gas perfetto: moto rettilineo uniforme con collisioni elastiche.
        Le particelle si muovono a velocità costante e rimbalzano elasticamente sui bordi.
        """
        # Calculate scaled particle radius
        scaled_radius = self.particle_radius * self.particle_scale

        # Calculate container bounds relative to center (with scaled radius)
        left_bound = self._container_center[0] - self._container_width / 2 + scaled_radius
        right_bound = self._container_center[0] + self._container_width / 2 - scaled_radius
        bottom_bound = self._container_center[1] - self._container_height / 2 + scaled_radius
        top_bound = self._container_center[1] + self._container_height / 2 - scaled_radius

        for i, particle in enumerate(self.particles):
            # Ideal gas: constant velocity, no acceleration, no damping
            # Update position with constant velocity
            new_pos = particle.get_center() + self.velocities[i] * dt * 10  # Scale dt for visible motion

            # Elastic collisions with walls (perfect reflection)
            if new_pos[0] < left_bound or new_pos[0] > right_bound:
                # Reflect x-velocity (elastic collision)
                self.velocities[i][0] *= -1.0
                # Clamp position to boundary
                new_pos[0] = max(left_bound, min(new_pos[0], right_bound))

            if new_pos[1] < bottom_bound or new_pos[1] > top_bound:
                # Reflect y-velocity (elastic collision)
                self.velocities[i][1] *= -1.0
                # Clamp position to boundary
                new_pos[1] = max(bottom_bound, min(new_pos[1], top_bound))

            particle.move_to(new_pos)

    def set_temperature(self, new_temperature):
        """
        Imposta una nuova temperatura (cambia colore e velocità).

        Parameters:
        -----------
        new_temperature : float
            Nuova temperatura in Kelvin
        """
        self.temperature = new_temperature
        new_color = self._temperature_to_color()

        for particle in self.particles:
            particle.set_color(new_color)

        return self

    def animate_temperature(self, new_temperature, run_time=2):
        """
        Anima il cambiamento di temperatura (colore e velocità cambiano gradualmente).
        La velocità è proporzionale alla temperatura (v ∝ T).

        Parameters:
        -----------
        new_temperature : float
            Nuova temperatura target in Kelvin
        run_time : float
            Durata dell'animazione in secondi

        Returns:
        --------
        Animation
            AnimationGroup per il cambio di temperatura
        """
        old_temperature = self.temperature

        # Store initial velocities to maintain directions during rescaling
        initial_velocities = [v.copy() for v in self.velocities]

        # Create a temporary tracker to interpolate temperature
        def update_temp(mob, alpha):
            interp_temp = interpolate(old_temperature, new_temperature, alpha)
            mob.temperature = interp_temp

            # Update particle colors
            interp_color = mob._temperature_to_color()
            for particle in mob.particles:
                particle.set_color(interp_color)

            # Rescale velocities based on temperature ratio (v ∝ T)
            # Use initial velocities to preserve direction from start of animation
            velocity_scale = interp_temp / old_temperature
            for i in range(len(mob.velocities)):
                # Scale the initial velocity (preserves original direction)
                mob.velocities[i] = initial_velocities[i] * velocity_scale

        return UpdateFromAlphaFunc(self, update_temp, run_time=run_time)

    def resize(self, new_width, new_height):
        """
        Ridimensiona il contenitore del gas.
        Le particelle vengono ridistribuite proporzionalmente.

        Parameters:
        -----------
        new_width : float
            Nuova larghezza
        new_height : float
            Nuova altezza
        """
        # Calculate scale factors
        width_scale = new_width / self._container_width
        height_scale = new_height / self._container_height

        # Update dimensions
        self._container_width = new_width
        self._container_height = new_height

        # Rescale particle positions relative to center
        for particle in self.particles:
            rel_pos = particle.get_center() - self._container_center
            rel_pos[0] *= width_scale
            rel_pos[1] *= height_scale
            particle.move_to(self._container_center + rel_pos)

        return self

    def get_bounds(self):
        """
        Restituisce i limiti del contenitore.

        Returns:
        --------
        dict
            Dizionario con 'left', 'right', 'bottom', 'top'
        """
        return {
            'left': self._container_center[0] - self._container_width / 2,
            'right': self._container_center[0] + self._container_width / 2,
            'bottom': self._container_center[1] - self._container_height / 2,
            'top': self._container_center[1] + self._container_height / 2
        }
