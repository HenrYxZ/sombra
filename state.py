class State:
    def __init__(self, pos, rot, v, w, m=1, scale=1):
        self.pos = pos
        self.rot = rot
        self.v = v
        self.w = w
        self.m = m
        self.scale = scale

    def __str__(self):
        return (
            'pos= {}, rot= {}, v= {}, w= {}, m= {}'
        ).format(self.pos, self.rot, self.v, self.w, self.m)

    def __repr__(self):
        return (
            'pos= {}, rot= {}, v= {}, w= {}, m= {}'
        ).format(self.pos, self.rot, self.v, self.w, self.m)


class SystemState:
    def __init__(self, time):
        self.time = time
        self.bodies_state = []

    def __str__(self):
        return 't: {}\nbodies: {}'.format(self.time, self.bodies_state)

    def __repr__(self):
        return 't: {}\nbodies: {}'.format(self.time, self.bodies_state)

    def add(self, state):
        self.bodies_state.append(state)
