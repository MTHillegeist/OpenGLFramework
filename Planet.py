class Planet():
    def __init__(self):
        self.distance = 0.0
        self.orbit_angle = 0.0
        self.speed = 0.0

        self.relative_angle = 0.0
        self.axis = None
        self.rotation_speed = 0.0

        self.size = 1.0
        self.shape = None

    def update(self, delta_t):
        self.orbit_angle += delta_t * self.speed
        self.relative_angle += delta_t * self.rotation_speed
