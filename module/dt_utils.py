from datetime import datetime, timedelta
#from zoneinfo import ZoneInfo
import pytz
import time
from django.utils.timezone import make_aware

# weekdays = ["Monday","Tuesday","Wednesday","Thursday","Friday","Satueday","Sunday"]
# slots = [('09:00', '12:00', 1), ('14:00', '18:00', 1), ('09:00', '12:00', 2), ('14:00', '18:00', 2), ('05:00', '10:00', 4), ('12:00', '23:00', 4)]

# tzoffset from tz
def get_utcoffset_minutes(tz):
    """  get offset of a timezone:
        tz: timezone
        """
    now = datetime.now(pytz.timezone(tz))
    utcoffset = int(now.utcoffset().total_seconds()/60)
    if "-" in str(utcoffset):
        return ('negative', int(str(utcoffset).replace("-", "")))
    else:
        return ('positive', int(utcoffset))


# get timezone difference
def tz_utcoffset_diff(base_tz, to_tz):
    """ get defference between two timezones in hours:
        base_tz: first timezone argument
        to_tz: second timezome argument for difference
        """
    dt = datetime.now()
    base_utcoff, to_utcoff = dt.astimezone(ZoneInfo(base_tz)).utcoffset(), dt.astimezone(ZoneInfo(to_tz)).utcoffset()
    diff = int((to_utcoff-base_utcoff).total_seconds()/60)
    if "-" in str(diff):
        return ('negative', int(str(diff).replace("-","")))
    else:
        return ('positive', int(diff))





# Convert weekdays into date attached timestamp/timeslot
def convert_wday_timestamp_slot(slot, offset_diff_minutes):
    """
    Convert weekdays into date attached timestamp/timeslot:
        slot: tuple(from_time, to_time),
        offset_diff_minnutes: offset difference in minutes
        """
    from_time, to_time, weekday = slot
    weekday_date  = 0
    counter = 0
    
    while 1:
        if weekday == (datetime.now() + timedelta(days=counter)).weekday():
            weekday_date = datetime.now() + timedelta(days=counter)
            break
        counter += 1
        
    from_dts = datetime.combine(weekday_date.date(), datetime.strptime(from_time,'%H:%M').time())
    to_dts = datetime.combine(weekday_date.date(), datetime.strptime(to_time,'%H:%M').time())

    if offset_diff_minutes[0] == "positive":
        from_dts = from_dts + timedelta(minutes = offset_diff_minutes[1])
        to_dts = to_dts + timedelta(minutes = offset_diff_minutes[1])

    if offset_diff_minutes[0] == "negative":
        from_dts = from_dts - timedelta(minutes = offset_diff_minutes[1])
        to_dts = to_dts - timedelta(minutes = offset_diff_minutes[1])

    if from_dts.date() == to_dts.date():
        return [(from_dts.strftime("%H:%M"), to_dts.strftime("%H:%M"), from_dts.weekday())]

    if from_dts.date() < to_dts.date():
        from_dts1 = datetime.combine(from_dts.date(), from_dts.time())
        to_dts1 = datetime.combine(from_dts.date(), datetime.strptime("00:00",'%H:%M').time())
        from_dts2 = datetime.combine(to_dts.date(), datetime.strptime("00:00",'%H:%M').time())
        to_dts2 = datetime.combine(to_dts.date(), to_dts.time())
        return [(from_dts1.strftime("%H:%M"), to_dts1.strftime("%H:%M"), from_dts1.weekday()),
                (from_dts2.strftime("%H:%M"), to_dts2.strftime("%H:%M"), to_dts2.weekday())]

    return None
    



# Convert datetime stamp to difference timezone
def convert_date_timestamp_slot(slots, to_timezone):
    """Convert datetime stamp to difference timezones
        slots: list of tuples -> [(from_time, to_time),(from_time, to_time),(from_time, to_time)],
        to_timezone: target timezone name -> example: "utc" or "Asia/Kolkata"
    """
    new_slots = {}
    for i in slots:
        ft = make_aware(datetime.combine(datetime.strptime(i[2],"%Y-%m-%d").date(),datetime.strptime(i[0],"%H:%M").time()), timezone=pytz.timezone(i[3]))
        tt = make_aware(datetime.combine(datetime.strptime(i[2],"%Y-%m-%d").date(),datetime.strptime(i[1],"%H:%M").time()), timezone=pytz.timezone(i[3]))
        new_ft = ft.astimezone(pytz.timezone(to_timezone))
        new_tt = tt.astimezone(pytz.timezone(to_timezone))


        if new_ft.date() == new_tt.date():
            
            if new_ft.strftime("%Y-%m-%d") in new_slots.keys():
                new_slots[new_ft.strftime("%Y-%m-%d")].append({"from_time":new_ft.strftime("%H:%M"), "to_time":new_tt.strftime("%H:%M")})
            else:
                new_slots[new_ft.strftime("%Y-%m-%d")] = [{"from_time":new_ft.strftime("%H:%M"), "to_time":new_tt.strftime("%H:%M")}]

        if new_ft.date() < new_tt.date():
            new_ft1 = datetime.combine(new_ft.date(), new_ft.time())
            new_tt1 = datetime.combine(new_tt.date(), datetime.strptime("00:00",'%H:%M').time())
            new_ft2 = datetime.combine(new_tt.date(), datetime.strptime("00:00",'%H:%M').time())
            new_tt2 = datetime.combine(new_tt.date(), new_tt.time())
            
            if new_ft1.strftime("%Y-%m-%d") in new_slots.keys():
                new_slots[new_ft1.strftime("%Y-%m-%d")].append({"from_time":new_ft1.strftime("%H:%M"), "to_time":new_tt1.strftime("%H:%M")})
            else:
                new_slots[new_ft1.strftime("%Y-%m-%d")] = [{"from_time":new_ft1.strftime("%H:%M"), "to_time":new_tt1.strftime("%H:%M")}]

            if new_ft2.strftime("%Y-%m-%d") in new_slots.keys():
                new_slots[new_ft2.strftime("%Y-%m-%d")].append({"from_time":new_ft2.strftime("%H:%M"), "to_time":new_tt2.strftime("%H:%M")})
            else:
                new_slots[new_ft2.strftime("%Y-%m-%d")] = [{"from_time":new_ft2.strftime("%H:%M"), "to_time":new_tt2.strftime("%H:%M")}]

    return {"timezone": to_timezone, "slots": new_slots}



# Slot validation
def validate_slots_for_a_date(date, booked_slots, available_slots):
    """
    Function to validate slots
    date: date object,
    booked_slots: booked slots for specific date -> [(from_time, to_time),(from_time, to_time),(from_time, to_time),(from_time, to_time)]
    available_slots: available slots for validation -> [(from_time, to_time),(from_time, to_time),(from_time, to_time),(from_time, to_time)]
    """
    bs_list = []
    as_list = []
    rs_list = []
    for i in booked_slots:
        bft = datetime.combine(datetime.strptime(date, "%Y-%m-%d").date(), datetime.strptime(i["from_time"],"%H:%M").time())
        btt = datetime.combine(datetime.strptime(date, "%Y-%m-%d").date(), datetime.strptime(i["to_time"],"%H:%M").time())
        if i["to_time"] == "00:00":
            btt = btt+timedelta(days=1)
        bs_list.append((bft, btt))

    for i in available_slots:
        aft = datetime.combine(datetime.strptime(date, "%Y-%m-%d").date(), datetime.strptime(i["from_time"],"%H:%M").time())
        att = datetime.combine(datetime.strptime(date, "%Y-%m-%d").date(), datetime.strptime(i["to_time"],"%H:%M").time())
        if i["to_time"] == "00:00":
            att = att+timedelta(days=1)
        as_list.append((aft, att))

    if len(bs_list) == 0:
        return sorted(as_list)

    
    for i in as_list:
        vls = []
        for j in bs_list:
            break_flag = False
            if (j[0]<=i[0]) and (j[1]>=i[1]):
                break_flag = True
                break
            if (j[0]<i[0])    and   (j[1]<i[1] and j[1]>i[0]):
                if not j in vls:
                    vls.append(j)
            if (j[0]>i[0] and j[0]<i[1])   and    (j[1]>i[1]):
                if not j in vls:
                    vls.append(j)
            if (j[0]>i[0])    and   (j[1]<=i[1]):
                if not j in vls:
                    vls.append(j)
            if (j[0]>=i[0])   and   (j[1]<i[1]):
                if not j in vls:
                    vls.append(j)

        vls = sorted(vls)
        if len(vls) > 0:
            
            av_slots = ([(i[0],i[0])] + vls + [(i[1],i[1])])
            if (vls[0][0] < i[0]) and (vls[-1][1] <= i[1]):
                av_slots = ([(vls[0][1],vls[0][1])] + vls[1:] + [(i[1],i[1])])
            if (vls[0][0] >= i[0]) and (vls[-1][1] > i[1]):
                av_slots = ([(i[0],i[0])] + vls[:-1] + [(vls[-1][0],vls[-1][0])])
            if (vls[0][0] < i[0]) and (vls[-1][1] > i[1]):
                av_slots = ([(vls[0][1],vls[0][1])] + vls[1:-1] + [(vls[-1][0],vls[-1][0])])

            for start, end in ((av_slots[i][1], av_slots[i+1][0]) for i in range(len(av_slots)-1)):
                if not start == end:
                    rs_list.append((start, end))
        else:
            if len(bs_list)>0 and break_flag == False:
                rs_list.append(i)

    return sorted(rs_list)





        













