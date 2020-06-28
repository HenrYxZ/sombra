from datetime import datetime


DATETIME_FORMAT = "%H:%M:%S %d-%m-%Y"

def print_datetime(message):
    now = datetime.now()
    datetime_str = now.strftime(DATETIME_FORMAT)
    print("{}: {}".format(message, datetime_str))

def start_of_animation():
    message = "Started the animation at"
    print_datetime(message)

def end_of_animation():
    message = "Finished the animation at"
    print_datetime(message)

def start_of_raytracing():
    message = "Started Raytracing at"
    print_datetime(message)

def end_of_raytracing():
    message = "Finished Raytracing at"
    print_datetime(message)
