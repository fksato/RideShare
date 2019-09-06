# RideShare

## Usage
python main_driver.py <scenario.in>

## provided scenario files by Google Hashcode team
a_example.in

b_should_be_easy.in

c_no_hurry.in

d_metroplis.in

e_high_bonus.in

## main_driver.py:
- environment initialization

## RiderDispatcher.py
- Simulates time
- Scheduler for cars
- Maximizes bonus points and number of fares

## Rider.py
- Rider object
- properties:

	__pos__: position of rider
	__end_pos: fare destination
	__start_time__: earliest time for pick-up
	__end_time__: latest time for pick-up
	__travel_time__: time required to go from rider position to destination
	__pickedUp__: flag to distinguish if rider has been picked up by car
	__bonus__: flag if bonus has been collected for the rider
	__b_point__: value of bonus
	__rider_id__: identification for rider

- methods:

	__getRiderID__: getter for rider ID
	__isBonus__: getter for whether fare was within time bonus
	__pickupRider__: setter for pickedUp. 
	__getBonus__: setter for bonus flag
	__removeBonus__: setter for bonus flag
	__totalPoints__: calculates potential fare points on fare completion


## Car.py
- Car object:
- properties:

	__rider_dispatcher__: connection to ride scheduler
	__time_limit__: time limit of trial

	__pos__: current position of car
	__time_step__: current time position
	__in_operation__: availability of car given time constraint

- methods:

	__curTime__: getter for car time
	__inOpertaion__: getter for in_operation
	__finish__: seeter for in_opertaion
	__updatePosition__: update car posiiton
	__updateTimeStep__: increment car time by time_step
	__setTimeStep__: set car time to time
