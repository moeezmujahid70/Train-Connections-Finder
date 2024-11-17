from datetime import datetime, timedelta


def calculate_time_differenc(from_time, to_time):
    from_time = datetime.strptime(
        from_time.strip("'"), "%H:%M:%S")
    to_time = datetime.strptime(
        to_time.strip("'"), "%H:%M:%S")

    # Handle overnight travel where arrival time is on the next day
    if to_time < from_time:
        to_time += timedelta(days=1)

    return (to_time - from_time)
