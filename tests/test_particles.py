import os
import sys
import unittest

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from assets.particles import EnhancedParticleSystem, Particle


class TestParticles(unittest.TestCase):
    def test_expired_particles_are_recycled(self):
        system = EnhancedParticleSystem()
        system.emit_burst(10, 20, (255, 0, 0), count=2, size_range=(3, 3), lifetime_range=(1, 1))

        original_ids = {id(p) for p in system.particles}
        self.assertEqual(len(system.particles), 2)

        system.update()

        self.assertEqual(len(system.particles), 0)
        self.assertEqual(len(system._particle_pool), 2)

        system.emit_burst(10, 20, (0, 255, 0), count=1, size_range=(3, 3), lifetime_range=(1, 1))

        self.assertEqual(len(system.particles), 1)
        self.assertIn(id(system.particles[0]), original_ids)

    def test_update_keeps_alive_particles(self):
        system = EnhancedParticleSystem()
        alive = Particle(0, 0, (0, 0, 255), 4, 10, velocity=(0, 0))
        dead = Particle(0, 0, (255, 0, 0), 4, 1, velocity=(0, 0))
        system.particles = [alive, dead]

        system.update()

        self.assertEqual(len(system.particles), 1)
        self.assertIs(system.particles[0], alive)
        self.assertGreaterEqual(len(system._particle_pool), 1)


if __name__ == '__main__':
    unittest.main()
