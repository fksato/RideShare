from Car import Car
from Rider import Rider

class RiderDispatcher:

    def __init__(self, rider_data, num_cars, time_limit, total_rides, bonus_points):
        self.__global_rider_dict = {}
        self.completed_rider_dict = {}
        self.car = None
        self.fleet = []
        self.total_rides = total_rides

        for rider in rider_data:
            new_rider = Rider( rider, bonus_points )
            rider_id = ''
            self.__global_rider_dict[new_rider.getRiderID()] = new_rider

        for i in range(num_cars):
            self.fleet.append(Car(self, time_limit))

        self.run()

    def setCar(self, car):
        self.car = car

    def getAvailableRiders(self):
        available_riders = []
        for rider_id, rider in self.__global_rider_dict.items():
            if rider_id in self.completed_rider_dict:
                continue
            if self.canCompleteRide(rider):
                available_riders.append( rider )
        return available_riders

    def updateCompletedRides(self, rider):
        self.completed_rider_dict[rider.getRiderID()] = rider

    def weights(self, rider):
        if isinstance( rider, Rider ):
            # points / total time
            return ( 1.0*rider.totalPoints() ) / ( rider.travel_time + self.distance(self.car.pos, rider.pos) )
        return 0

    def retrieveOptimalRider(self, candidates_list):
        if candidates_list:
            max_rider = candidates_list[0]
            max_wait_time = self.waitForBonus(max_rider)
            for rider in candidates_list:
                rider_wait_time = self.waitForBonus(rider)
                if self.weights(rider) > self.weights(max_rider) or rider_wait_time > max_wait_time:
                    max_rider = rider
                    max_wait_time = rider_wait_time
            return max_rider

    def distance(self, start_position, end_position):
        return abs(start_position[0]-end_position[0]) + abs(start_position[1]-end_position[1])

    def createPath(self):
        self.carPath = []
        self.recursion = 0

    def addToPath(self, rider, pick_up_time):
        self.carPath.insert( 0, [rider, pick_up_time] )

    def getPath(self):
        return self.carPath

    def canCompleteRide(self, rider):
        if isinstance( rider, Rider ):
            wait_time = self.waitForBonus(rider)
            return rider.end_time - (self.distance(self.car.pos, rider.pos) + rider.travel_time + wait_time + self.car.curTime()) >= 0
        return False

    def waitForBonus(self, rider):
        wait_time = rider.start_time - self.car.curTime()
        if wait_time >= 0:
            if wait_time == 0:
                if self.distance(self.car.pos, rider.pos) == 0:
                    rider.getBonus()
            else:
                rider.getBonus()
            return wait_time

        rider.removeBonus()
        return 0

    def pickupRider(self, rider, pickup_time):
        wait_time = self.waitForBonus(rider)
        dist_to_rider = self.distance(self.car.pos, rider.pos)

        if pickup_time == -1:
            pickup_time = dist_to_rider

        self.car.setTimeStep(pickup_time + rider.travel_time)

        if self.car.curTime() > rider.end_time:
            raise AssertionError("ERROR: invalid car time step and rider time")

        if self.car.inOperation:
            rider.pickupRider(pickup_time)
            self.updateCompletedRides(rider)

        self.car.updatePosition(rider.end_pos)

    def retrieveCandidate(self, candidates_list):
        index = 0
        i = 0
        max_rider = candidates_list[0]
        max_wait_time = self.waitForBonus(max_rider)
        for rider in candidates_list:
            rider_wait_time = self.waitForBonus(rider)
            if self.weights(rider) > self.weights(max_rider) or rider_wait_time > max_wait_time:
                index = i
                max_rider = rider
                max_wait_time = rider_wait_time
            i += 1
        return max_rider, index


    def maximalStrategy(self, max_rider, timer, intermediate_list):
        candidate_list = []
        pickup_times = []
        # check if max_rider is bonus:
        bonus_available = max_rider.isBonus()
        # if bonus, what is the wait time?
        if bonus_available:
            wait_time = self.waitForBonus(max_rider)
            if wait_time == 0:
                return
            bonus_start = max_rider.start_time
            for intermediate_rider in intermediate_list:
                temp = timer
                dist_to_bonus = self.distance(intermediate_rider.end_pos, max_rider.pos)
                car_dist_to_intermediate = self.distance(intermediate_rider.pos, self.car.pos)
                temp -=  (intermediate_rider.travel_time + car_dist_to_intermediate + dist_to_bonus)
                intermediate_start = (bonus_start - dist_to_bonus - car_dist_to_intermediate - intermediate_rider.travel_time)
                intermediate_end =  (bonus_start - dist_to_bonus)
                # check if ride fits within bonus window:
                if temp >= 0 and intermediate_start >= intermediate_rider.start_time and intermediate_end <= intermediate_rider.end_time:
                    candidate_list.append( intermediate_rider )
                    pickup_times.append( intermediate_start )
        else:
            #find points nearby with bonuses available:
            for intermediate_rider in intermediate_list:
                #max time start:
                max_time_start = timer
                dist_to_rider = self.distance(intermediate_rider.end_pos, max_rider.pos)
                car_dist_to_intermediate = self.distance(intermediate_rider.pos, self.car.pos)
                total_travel_time = intermediate_rider.travel_time + car_dist_to_intermediate + dist_to_rider
                max_time_start -=  total_travel_time
                intermediate_end = max_time_start + intermediate_rider.travel_time
                if max_time_start >= 0 and max_time_start>= intermediate_rider.start_time and intermediate_end <= intermediate_rider.end_time:
                    candidate_list.append( intermediate_rider )
                    #pickup_times.append( max_time_start )
                    pickup_times.append( -1 )

        #add max_rider @ pickup_time: bonus_start or 
        if not candidate_list or len(candidate_list) != len(pickup_times):
            return

        previous_rider, index = self.retrieveCandidate(candidate_list)
        self.addToPath(previous_rider, pickup_times[index])
        intermediate_list.remove(previous_rider)
        timer -=  previous_rider.travel_time + self.distance(self.car.pos, previous_rider.pos) + self.distance(previous_rider.end_pos, max_rider.pos)

        #if self.recursion < 900:
        self.recursion += 1
        self.maximalStrategy(previous_rider, timer, intermediate_list)
        #else:
        #   return

    def run(self):
        for car in self.fleet:
            rider_list = []
            self.setCar(car)
            while(car.inOperation()):
                # create an intermidiate bonus chain check path:
                self.createPath()
                rider_max = None
                rider_list = self.getAvailableRiders()

                if not rider_list:
                    car.finish()
                    continue

                rider_max = self.retrieveOptimalRider(rider_list)

                timer = 0
                if rider_max.isBonus():
                    timer = self.waitForBonus(rider_max)
                    pickup_time = rider_max.start_time
                else:
                    timer = rider_max.end_time - rider_max.travel_time
                    pickup_time = -1

                self.addToPath(rider_max, pickup_time)
                rider_list.remove(rider_max)

                self.maximalStrategy(rider_max, timer, rider_list)

                for path_rider in self.getPath():
                    self.pickupRider(path_rider[0], path_rider[1])
        # compute statistics:
        self.computeStats()

    def computeStats(self):
        rides_completed = 0
        total_points = 0
        number_of_bonuses = 0
        for rider in self.completed_rider_dict.values():
            rides_completed += 1
            total_points += rider.totalPoints()
            if rider.isBonus():
                number_of_bonuses += 1

        print('TOTAL RIDES: %s\nrides completed: %s\ntotal points: %s\nnumber of bonuses: %s\n' % 
                (self.total_rides, rides_completed, total_points, number_of_bonuses))

