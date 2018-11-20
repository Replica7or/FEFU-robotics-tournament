import pyb,time
from colorSensor import TCS34725

#srv1 = pyb.Servo(1)
#tc = TCS34725()
from pyb import Pin, Timer, ADC, Servo
from utime import sleep_ms

T = time.time()+8
Stage = 1
serv_left = Servo(3)
serv_right = Servo(4)


p_light_left = Pin('X20', Pin.IN, Pin.PULL_UP)    #blackwhite sensors. Digital mode
p_light_right = Pin('X21', Pin.IN, Pin.PULL_UP)

Face_sensor = ADC(Pin('X12'))    #collision avoid sensors. Analog mode
Left_sensor = ADC(Pin('X19'))
Right_sensor = ADC(Pin('X11'))

p_out_left_forward = Pin('X7', Pin.OUT_PP)    #Forward-backward direction left motor
p_out_left_backward = Pin('X8', Pin.OUT_PP)

p_out_right_forward = Pin('X5', Pin.OUT_PP)    #Forward-backward direction right motor
p_out_right_backward = Pin('X6', Pin.OUT_PP)

p_left = Pin('X1')    #PWM left motor
p_right = Pin('X2')    #PWM right motor

tim = Timer(2, freq=1000)    #set timer & frequency

ch_left = tim.channel(1, Timer.PWM, pin=p_left)    #set pwm channel
ch_right = tim.channel(2,Timer.PWM, pin=p_right)

p_out_left_forward.high()    #activate
p_out_right_forward.high()
p_out_left_backward.low()    #deactivate
p_out_right_backward.low()

serv_left.angle(40)
serv_right.angle(50)

ch_left.pulse_width_percent(40)    #set pwn power
ch_right.pulse_width_percent(40)

while True:
    print(Left_sensor.read(), Face_sensor.read(), Right_sensor.read())

    Light_left = p_light_left.value()
    Light_right = p_light_right.value()

    Light_left = p_light_left.value()
    Light_right = p_light_right.value()
    #r, g, b, c = tc.get_raw_data()
    #print(r, g, b, c)


    if Stage==1:            #переписать весь кусок
        if time.time() > T:
            Stage += 1
        if (Light_left==0 and Light_right==0) or (Light_left==1 and Light_right==1):
            p_out_left_backward.low()
            p_out_right_backward.low()
            p_out_left_forward.high()
            p_out_right_forward.high()
            ch_left.pulse_width_percent(40)
            ch_right.pulse_width_percent(40)
        elif Light_left==1:
            p_out_left_forward.low()
            p_out_left_backward.high()
            ch_left.pulse_width_percent(40)
            ch_right.pulse_width_percent(40)
        else:
            p_out_right_forward.low()
            p_out_right_backward.high()
            ch_right.pulse_width_percent(50)
            ch_left.pulse_width_percent(50)
    elif Stage==2:
        p_out_left_backward.low()
        p_out_right_backward.low()
        p_out_left_forward.high()
        p_out_right_forward.high()
        ch_left.pulse_width_percent(60)
        ch_right.pulse_width_percent(60)
        time.sleep(2)
        Stage+=1
    elif Stage==3:
        ch_left.pulse_width_percent(20)
        ch_right.pulse_width_percent(20)
        while True:
            if Face_sensor.read()>3700:
                p_out_right_backward.low()
                p_out_right_forward.high()
                p_out_left_backward.low()
                p_out_left_forward.high()

            elif Left_sensor.read()>3700:
                #p_out_right_forward.low()
                #p_out_left_forward.low()
                #p_out_right_backward.high()
                #p_out_left_backward.high()
                #ch_left.pulse_width_percent(10)
                #ch_right.pulse_width_percent(10)
                #time.sleep(0.5)
                p_out_right_backward.low()
                p_out_right_forward.high()
                p_out_left_forward.low()
                p_out_left_backward.high()
                ch_left.pulse_width_percent(20)
                ch_right.pulse_width_percent(20)
                time.sleep(1)

            elif Right_sensor.read()>3700:
                p_out_right_forward.low()
                p_out_right_backward.high()
                p_out_left_backward.low()
                p_out_left_forward.high()
                ch_left.pulse_width_percent(20)
                ch_right.pulse_width_percent(20)
                time.sleep(1)
            else:
                p_out_right_forward.low()
                p_out_left_forward.low()
                p_out_right_backward.high()
                p_out_left_backward.high()
                ch_left.pulse_width_percent(40)
                ch_right.pulse_width_percent(40)
                time.sleep(2)
    #print(p_light_left.value(),p_light_right.value())
    #print(value)

#while True:
#    r, g, b, c = tc.get_raw_data()
#    print(r, g, b, c)