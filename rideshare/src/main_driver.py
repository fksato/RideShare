import os
import sys
from RiderDispatcher import RiderDispatcher

class MainDriver:

    def __init__(self, file_name):
        self.parseData(os.getcwd()+ '\\' + file_name)

    def parseData(self, file_name):
        f=open(file_name)
        data = f.readline().split()
        num_cars = int(data[2])
        bonus_points = int(data[4])
        time_limit = int(data[5])
        total_rides = int(data[3])
        sys.setrecursionlimit(total_rides)

        rider_data = []
        for line in f:
            rider_data.append([int(k) for k in line.split()])
        
        self.riderDispatcher = RiderDispatcher(rider_data, num_cars, time_limit, total_rides, bonus_points)

if __name__ == '__main__':
    app = MainDriver(sys.argv[1])
