# codeskulptor http://www.codeskulptor.org/#user40_bHLVkmDBrqSNoxZ.py
# template for "Stopwatch: The Game"

import simplegui


# define global variables
timer = None
counter, total_stops, on_sec_stops = 0, 0, 0
already_stopped = True

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t_msec):
    m , remanider = int(t_msec) / 600, int(t_msec) % 600
    s, ms = str(remanider / 10), remanider % 10
    return "%s:%s.%s" % (m, s.rjust(2, '0'), ms)
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    global timer, already_stopped
    if already_stopped:
        timer.start()
        already_stopped = False
    
    
    
def stop(update_counters=True):
    global timer, counter, total_stops, on_sec_stops, already_stopped
    
    if already_stopped:
        # Got nothing else to do
        return
    
    timer.stop()
    already_stopped = True
    
    if update_counters:
        total_stops += 1
        if counter % 10 == 0:
            on_sec_stops += 1

            
def reset():
    # I personally think that reset should not stop the timer... 
    stop(False)
    global counter, total_stops, on_sec_stops, already_stopped
    counter, total_stops, on_sec_stops = 0, 0, 0



# define event handler for timer with 0.1 sec interval
def increment():
    global counter 
    counter += 1

    
# define draw handler
def draw(canvas):
    global counter, total_stops, on_sec_stops
    canvas.draw_text(format(counter), [68,102], 32, "Red")
    colour = "White"
    if on_sec_stops and on_sec_stops == total_stops:
        colour = "Green"
    canvas.draw_text("%s/%s" % (on_sec_stops, total_stops),
                     [6, 14], 18, colour)
    

# create frame
frame = simplegui.create_frame("StopWatch", 200, 200)

# register event handlers
frame.add_button("Start", start)
frame.add_button("Stop", stop)
frame.add_button("Reset", reset)
frame.set_draw_handler(draw)
timer = simplegui.create_timer(100, increment)

# start frame
frame.start()

# Please remember to review the grading rubric
