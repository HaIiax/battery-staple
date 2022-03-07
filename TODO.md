# TODO's

## ~~Rename security.py~~

- Seems to have special meaning to github

## ~~Create Helper Class~~

- Passed as first argument to run() function
- Holds initialized instances of
    - Storage
    - Security
    - LocationNormalizer
    - ... future helpers
- Create instance in groupme-bot.py, set instances of Storage, Security and LocationNormalizer
- Avoids having to modify the run() signature and callers each time a new helper is needed

## ~~Normalize Location Names~~

- Init with environment variable, comma delimited list of unique location names
- Remove spaces before processing to list of string
- Save list as class attribute
- Function normalize(candidate_name: str)
    - Find locations that start with the candidate_name, keep count
    - If count > 1 return None
    - Use lowercase with the comparisons
    - If found return the normalized name, else return None
- Use with .user command
    - person.location = normalizer.normalize(location)
    - if person.location is None, get list of valid locations from the normalizer and send back as message to user

## ~~Change Person time attribute to ordinal~~

- Add to event table pickup_time (hh:mm) and pickup_interval (minutes)
- Change person table time attribute to integer
- Compute display time in runschedulepublisher.py
    - Make sure sort by time compatible with numerics - format(%2.2d)
    - Convert pickup_time (hh:mm) to minutes -> pickup_time_minutes
    - Compute offset from pickup_time as (person.time - 1) * pickup_interval
    - Compute display time as pickup_time_minutes + pickup_offset converted back to hh:mm

## Editable Guests

- Extend generation of 'Guest' rides from the single placeholder to times computed from event guest_pickup_time, guest_pickup_interval and guest_rides
- Create a regenerated unique prefix for the guests G offset : index, where offset is the 1 based guest time offset, and index is the 1 based ordinal of the cars initial sort order
- Location set to the string 'Open'
- The guest prefix and information is stored in the event_ride user_id column. The join from er.user_id to person is already a left join. Change COALESCE(pr.name, 'Guests') to COALESCE(pr.name, er.user_id)
- The .guest command has 2 parameters - location, guest details. It will find the first Open location, store the new location and details, write the changes back to the event ride table, then republish.
- The .guestedit command
    - modify [n:o], location, details
    - remove [n:o]