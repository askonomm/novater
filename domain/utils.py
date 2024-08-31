from datetime import datetime
import pytz


def get_current_time_in_tz(timezone_str, timezone_type):
    current_time = datetime.now()

    # Z / UTC
    if timezone_str == 'Z':
        return current_time.astimezone(pytz.UTC)

    # +0200
    if timezone_type == 1:
        offset_hrs = int(timezone_str[:3])
        offset_mins = int(timezone_str[0] + timezone_str[3:])
        fixed_offset = pytz.FixedOffset(offset_hrs * 60 + offset_mins)

        return current_time.astimezone(fixed_offset)

    # EET / Europe/Tallinn
    if timezone_type == 2 or timezone_type == 3:
        return current_time.astimezone(pytz.timezone(timezone_str))

    # UTC if nothing matches
    return current_time.astimezone(pytz.UTC)
