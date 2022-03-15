# User Commands

## .help

Shows the help message.

## .user

Users are automatically added the first time they send a group message, with their name taken from GroupMe. Before users can be scheduled they need to set a time slot and location using this command.

- .user time slot (1-9), location

## .car

Offer your car to be used for driving using the add command, or remove the car. Removing a car after rides have been scheduled for the current event requires generating the schedule again.

- .car add, seats , model , parking_location
- .car remove

## .usecar

Offers your car for use in the current event. A .car command needs to be invoked first before the .usecar command is issued.

## .notusecar

Removes your car for use in the current event. Removing a car after rides have been scheduled for the current event requires generating the schedule again.

## .notgoing

Opt out of the current event. Opting out of the current event after the rides have been scheduled requires generating the schedule again.

## .going

Opt in to the current event, after having previously opted out with the .notgoing command. Opting in to the current event after the rides have been scheduled requires generating the schedule again.

## .driving

Opt in to driving for the current event. Opting in as a driver for the current event after the rides have been scheduled requires generating the schedule again.

## .notdriving

Opt out of driving the current event. Opting out as a driver for the current event after the rides have been scheduled requires generating the schedule again.

## .getlink

Get the link to the current ride schedule.

# Administative Commands

## .event

Maintains events. The add command will also edit an existing event. Changing any of the pickup and interval settings requires a generation.

- .event add, event_date, name, pickup time, pickup interval, guest_time, guest_interval, guest_rides
- .event remove, event_date

## .generate

Creates or recreates the ride schedule given the event current drivers (set by .driving) and event opt outs (set by .notgoing). One a rider or guest has been scheduled for a given pickup time and car, they stay scheduled with that pickup time and car, unless a driver opts out (set by .notdriving) and another driver is not assigned.

## .guest

Maintains the guest rides. Adding a guest automatically picks the next available car and driver. Once a guest is scheduled they stay assigned to the same time, car and driver.

- .guest add, location, description
- .guest edit, n:m, location, description
- .guest remove, n:m