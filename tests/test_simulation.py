import numpy as np
import unittest
# Local Modules
from simulation import SphereBody, Simulation
from state import State, SystemState


class SimulationTestCase(unittest.TestCase):
    def test_sphere_run(self):
        r = 1
        sphere_body = SphereBody(r)
        pos = np.zeros(3)
        rot = np.zeros(3)
        v = np.array([3, 0, 0], dtype=float)
        a = np.zeros(3)
        w = np.array([3.0/r, 0.0, 0.0])
        sphere_state = State(pos, rot, v, a, w)
        t = 0
        initial_state = SystemState(t)
        initial_state.add(sphere_state)
        rigid_bodies = [sphere_body]
        duration = 3
        time_step = 1
        simulation = Simulation(
            initial_state, rigid_bodies, duration, time_step
        )
        f = -1 * (v / duration)
        states = simulation.run(f)
        # Ensure v is calculated right
        self.assertEqual(states[1].bodies_state[0].v[0], 2)
        self.assertEqual(states[2].bodies_state[0].v[0], 1)
        self.assertEqual(states[3].bodies_state[0].v[0], 0)


if __name__ == '__main__':
    unittest.main()
