## Calendar Slot Booking
A Light wieght calendar slot booking python module to build real-time slot booking with timezone compatibility.

### Features
- **Offset based conversion**: Convert timestamp with offset
- **Flexible output**: Validation functions return output in tuple and lists which makes it really flexible to work with.
- **Timezone compatibility**: Validate slots across different timezones
- **Date Overrides**: Helps us to build easy date override functionality 
- **Function Doc**: Access the intitutive doc with .__doc__


<br>

## Usage

#### get_utcoffset_minutes()
Helps us to get offsets of a specific timezone.
##### `get_utcoffset_minutes(tz)`
<br>

#### tz_utcoffset_diff()
Gives us defference between two timezones in hours.
##### `tz_utcoffset_diff(tz1, tz2)`
<br>

#### convert_wday_timestamp_slot()
Convert weekdays into date attached timestamp/timeslot
##### `convert_wday_timestamp_slot(slot, offset_diff_minutes)`
<br>

#### convert_date_timestamp_slot()
Convert datetime stamp to difference timezone.
##### `convert_date_timestamp_slot(slots, to_timezone)`
<br>


#### validate_slots_for_a_date()
Slot validation
##### `validate_slots_for_a_date(date, booked_slots, available_slots)`
<br>




## Contributing

We love your contributions and do our best to provide you with mentorship and support.  
If nothing grabs your attention, check or come up with your feature. Just drop us a line or and we’ll work out how to handle it.


## Your feedback

Did you use Calendar Slot Boolikg module?
Share your feedback and help us grow. It will take just a minute, but mean a lot!

#### Crafted by [Wolves](https://wolfpackdigi.com/) 


