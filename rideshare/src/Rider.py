
class Rider:
    def __init__(self, rider, b_point):
        self.pos = [rider[0], rider[1]]
        self.end_pos = [rider[2], rider[3]]
        self.start_time = rider[4]
        self.end_time = rider[5]
        self.travel_time = abs(self.pos[0]-self.end_pos[0]) + abs(self.pos[1]-self.end_pos[1])
        self.pickedUp = False
        self.bonus = False
        self.b_point = b_point
        self.rider_id = ''
        # create rider_id:
        for i in range(6):
            self.rider_id += bin(rider[i])

    def getRiderID(self):
        return self.rider_id

    def isBonus(self):
        return self.bonus

    def pickupRider(self, pickup_time):
        if pickup_time == self.start_time:
            self.getBonus()
        else:
            self.removeBonus()
        self.pickedUp = True

    def getBonus(self):
        self.bonus = True

    def removeBonus(self):
        self.bonus = False

    def totalPoints(self):
        return self.travel_time + self.b_point if self.bonus else self.travel_time
