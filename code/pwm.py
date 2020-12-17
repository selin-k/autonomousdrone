import RPi.GPIO as IO     
import time               

IO.setmode(IO.BOARD)    # set to pin numbering by choosing board
IO.setup(12, IO.OUT)    # set GPIO 12 as output
pwm = IO.PWM(12, 100)   # set PWM on pin 12 to 100Hz frequency

duty_cycle = 0                       # set duty cycle to 0%
pwm.start(duty_cycle)              # start PWM with duty cycle 0%

try:
  while True:                      # this loops the program until KeyboardInterrupt (Ctrl + C)
    for duty_cycle in range(0, 101, 5):    # loop from 0 to a 100 with step 5
      pwm.ChangeDutyCycle(duty_cycle)
      time.sleep(0.05)             # this sleeps 0.05s at the current duty_cycle, provides specific LED brightness to indicate 
      print(duty_cycle)
    for duty_cycle in range(95, 0, -5):    # loops 95 to 5, step -5, hence is just a loop down to decrease duty cycle, LED brightness decreases here
      pwm.ChangeDutyCycle(duty_cycle)
      time.sleep(0.05)             
      print(duty_cycle)
except KeyboardInterrupt:
pwm.stop()                         
IO.cleanup()                     # cleans up and resets GPIO ports
