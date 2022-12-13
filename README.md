## Bookit



### Description

Bookit is a calendar slot booking python module that helps developers building real-time slot booking easy with timezone compatibility.
Bookit provides functions to make it possible.



### Usage.

#### get_utcoffset_minutes()
Helps us to get offsets of a specific timezone.
##### `get_utcoffset_minutes(tz)`


#### tz_utcoffset_diff()
Gives us defference between two timezones in hours.
##### `tz_utcoffset_diff(tz1, tz2)`


#### convert_wday_timestamp_slot()
Convert weekdays into date attached timestamp/timeslot
##### `convert_wday_timestamp_slot(slot, offset_diff_minutes)`


#### convert_date_timestamp_slot()
Convert datetime stamp to difference timezone.
##### `convert_date_timestamp_slot(slots, to_timezone)`


#### validate_slots_for_a_date()
Slot validation
##### `validate_slots_for_a_date(date, booked_slots, available_slots)`

