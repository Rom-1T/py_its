from datetime import datetime, timezone, timedelta
import time

DELTA_WITH_STACK = 70876


def calculate_tst_tai():
    # Define the TAI offset in seconds (as of the current offset, which may change)
    TAI_OFFSET = 37  # As of now, TAI is 37 seconds ahead of UTC

    # Define the epoch start time
    epoch_start_utc = datetime(2004, 1, 1, 0, 0, 0, 0, tzinfo=timezone.utc)

    # Get the current time in UTC
    current_time_utc = datetime.now(timezone.utc)

    # Convert current UTC time to TAI by adding the TAI offset
    current_time_tai = current_time_utc + timedelta(seconds=TAI_OFFSET)

    # Calculate TST as the number of milliseconds since the epoch start
    tst_milliseconds = int((current_time_tai - epoch_start_utc).total_seconds() * 1000)

    # Apply the modulo 2^32 operation
    tst_mod = tst_milliseconds % (2**32)

    return tst_milliseconds, tst_mod


def calculate_timestamp_its(current_time=None):
    # Define the epoch start time in UTC
    epoch_start = datetime(2004, 1, 1, 0, 0, 0, tzinfo=timezone.utc)

    # TAI offset in seconds (as of May 2023, TAI is 37 seconds ahead of UTC)
    TAI_OFFSET = 37

    # Get the current time in UTC if not provided
    if current_time is None:
        current_time = datetime.now(timezone.utc)

    # Convert current UTC time to TAI by adding the TAI offset
    current_time_tai = current_time + timedelta(seconds=TAI_OFFSET)

    # Calculate the total number of milliseconds since the epoch start
    total_milliseconds = int((current_time_tai - epoch_start).total_seconds() * 1000)

    return total_milliseconds - DELTA_WITH_STACK
