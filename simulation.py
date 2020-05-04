import numpy as np
# Local Modules
from state import State, SystemState


class RigidBody:
    def __init__(self, obj):
        self.obj = obj

    def simulate_physics(self, state, delta_t, f):
        pass


class SphereBody(RigidBody):
    def __init__(self, sphere):
        RigidBody.__init__(self, sphere)
        self.r = sphere.radius

    def simulate_physics(self, state, delta_t, f):
        # This is for constant F and a
        d = state.v * delta_t
        pos = state.pos + d
        rot = state.rot + state.w * delta_t
        a = f / state.m
        v = state.v + a * delta_t
        vx, vy, vz = v[0], v[1], v[2]
        wz = -1 * ((vx + vy) / self.r)
        wx = (vz + vy) / self.r
        wy = 0
        w = np.array([wx, wy, wz])
        return State(pos, rot, v, w)


class Simulation:
    def __init__(self, initial_state, rigid_bodies, duration, time_step):
        # States and bodies will always have the same index on the list
        self.initial_state = initial_state
        self.rigid_bodies = rigid_bodies
        self.duration = duration
        self.time_step = time_step

    def run(self, f):
        current_state = self.initial_state
        simulation_states = [current_state]
        t = current_state.time
        while t < self.duration:
            # Update system state
            # Update time
            t += self.time_step
            new_system = SystemState(t)
            for body_index in range(len(self.rigid_bodies)):
                body_state = current_state.bodies_state[body_index]
                rigid_body = self.rigid_bodies[body_index]
                new_state = rigid_body.simulate_physics(
                    body_state, self.time_step, f
                )
                new_system.add(new_state)
            simulation_states.append(new_system)
            current_state = new_system
        return simulation_states
