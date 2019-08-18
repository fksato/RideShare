
class Car:
    rider_dispatcher = None
    time_limit = None

    def __init__(self, dispatcher, limit):
        # Singleton static class vars:
        if not Car.rider_dispatcher:
            Car.rider_dispatcher = dispatcher
        if not Car.time_limit:
            Car.time_limit = limit

        self.pos = [0,0]
        self.time_step = 0
        self.in_operation = True

    def curTime(self):
        return self.time_step

    def inOperation(self):
        return self.in_operation

    def finish(self):
        self.in_operation = False

    def updatePosition(self, pos):
        self.pos = pos

    def updateTimeStep(self, time_step):
        self.time_step += time_step
        if self.time_step > Car.time_limit:
            self.in_operation = False

    def setTimeStep(self, time):
        self.time_step = time
        if self.time_step > Car.time_limit:
            self.in_operation = False
