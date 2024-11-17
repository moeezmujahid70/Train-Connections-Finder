from datetime import datetime, timedelta


def calculate_time_differenc(from_time, to_time):
    '''calculate the time diffrence between two given time inputs'''
    from_time = datetime.strptime(
        from_time.strip("'"), "%H:%M:%S")
    to_time = datetime.strptime(
        to_time.strip("'"), "%H:%M:%S")

    # Handle overnight travel where arrival time is on the next day
    if to_time < from_time:
        to_time += timedelta(days=1)

    return (to_time - from_time)


def add_seconds_to_time(arrival_time: str, seconds: int) -> str:
    """
    Adds seconds to the given arrival time and returns the result in dd:hh:mm:ss format.

    Parameters:
        arrival_time (str): The arrival time in "HH:MM:SS" format.
        seconds (int): The number of seconds to add.

    Returns:
        str: The resulting time in "dd:hh:mm:ss" format.
    """
    # Parse the arrival time
    base_time = datetime.strptime(arrival_time, "%H:%M:%S")

    # Add the seconds to the base time
    updated_time = base_time + timedelta(seconds=seconds)

    # Calculate total days, hours, minutes, and seconds
    total_seconds = (updated_time - base_time.replace(hour=0,
                     minute=0, second=0)).total_seconds()
    days, remainder = divmod(total_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    # Format and return the result
    return f"{int(days):02}:{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
