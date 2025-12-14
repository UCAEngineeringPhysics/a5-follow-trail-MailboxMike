from motor_driver import MotorDriver
from DualMotorDriver import DualMotorDriver_
from machine import Pin
from time import sleep, sleep_ms

"""
self, driver_ids: list | tuple, encoder_ids: list | tuple) -> None:
        super().__init__(*driver_ids)
"""

class TrailFollower_(DualMotorDriver_):
    def __init__(self, right_ids: tuple, left_ids:tuple, stby_id: int, encoder_ids: list | tuple):
        super().__init__(right_ids, left_ids, stby_id)
        
        # Pin configuration
        self.enc_a_pin = Pin(encoder_ids[0], Pin.IN)
        self.enc_b_pin = Pin(encoder_ids[1], Pin.IN)
        self.enc_a_pin.irq(
            trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self.update_counts_a
        )
        self.enc_b_pin.irq(
            trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self.update_counts_b
        )
        # Variables
        self.enc_a_val = self.enc_a_pin.value()
        self.enc_b_val = self.enc_b_pin.value()
        self.encoder_counts = 0
        self.prev_counts = 0
        self.meas_ang_vel = 0.0
        self.meas_lin_vel = 0.0

    def update_counts_a(self, pin):
        self.enc_a_val = pin.value()
        if self.enc_a_val == 1:
            if self.enc_b_val == 0:  # a=1, b=0
                self.encoder_counts += 1
            else:  # a=1, b=1
                self.encoder_counts -= 1
        else:
            if self.enc_b_val == 0:  # a=0, b=0
                self.encoder_counts -= 1
            else:  # a=0, b=1
                self.encoder_counts += 1

    def update_counts_b(self, pin):
        self.enc_b_val = pin.value()
        if self.enc_b_val == 1:
            if self.enc_a_val == 0:  # b=1, a=0
                self.encoder_counts -= 1
            else:  # b=1, a=1
                self.encoder_counts += 1
        else:
            if self.enc_a_val == 0:  # b=0, a=0
                self.encoder_counts += 1
            else:  # b=0, a=1
                self.encoder_counts -= 1

    def resetCount(self):
        sleep_ms(60)
        self.encoder_counts = 0
        sleep_ms(60)
    def forward(self, speed):
        self.left_motor.forward(speed)
        self.right_motor.forward(speed)    
    def backward(self, speed):
        self.left_motor.backward(speed)
        self.right_motor.backward(speed)
        
    def spinL(self, speed=0.):
        assert 0<=speed<=1
        self.right_motor.forward(speed)
        self.left_motor.backward(speed)

    def spinR(self, speed=0.):
        assert 0<=speed<=1
        self.right_motor.backward(speed)
        self.left_motor.forward(speed)
        
        
if __name__ =="__main__":
    tf = TrailFollower_(left_ids=(15,13,14), right_ids=(16,18,17), stby_id=12, encoder_ids=(10,11))
    tf.forward(.0)
    tf.backward(.0)
    sleep(2)

    STBY = Pin(12, Pin.OUT)
    STBY.off()
    # LOOP
    STBY.on()  # enable motor driver
    i=0
    tf.resetCount()

    while tf.encoder_counts<=16700:#8000,14850
        tf.forward(.5)
        print(f"f, dc: {i}%, enc_cnt: {tf.encoder_counts}")
        sleep_ms(20)  # 4 seconds to ramp up
    tf.forward(.0)
    tf.backward(.0)
    tf.resetCount()
    sleep(1)
    while tf.encoder_counts>=-1850:
        tf.spinL(.5)
        print(f"f, dc: {i}%, enc_cnt: {tf.encoder_counts}")
        sleep_ms(20)  # 4 seconds to ramp up
    tf.forward(.0)
    tf.backward(.0)
    tf.resetCount()
    sleep(1)
    while tf.encoder_counts<=11100:
        tf.forward(.5)
        print(f"f, dc: {i}%, enc_cnt: {tf.encoder_counts}")
        sleep_ms(20)  # 4 seconds to ramp up
    tf.forward(.0)
    tf.backward(.0)
    tf.resetCount()
    sleep(1)
    while tf.encoder_counts<=5900:
        tf.spinR(.5)
        print(f"f, dc: {i}%, enc_cnt: {tf.encoder_counts}")
        sleep_ms(20)  # 4 seconds to ramp up
    tf.forward(.0)
    tf.backward(.0)
    tf.resetCount()
    sleep(1)
    while tf.encoder_counts<=11000:
        tf.forward(.5)
        print(f"f, dc: {i}%, enc_cnt: {tf.encoder_counts}")
        sleep_ms(20)  # 4 seconds to ramp up
    tf.forward(.0)
    tf.backward(.0)
    tf.resetCount()
    sleep(1)
    while tf.encoder_counts>=-1000:
        tf.spinL(.5)
        print(f"f, dc: {i}%, enc_cnt: {tf.encoder_counts}")
        sleep_ms(20)  # 4 seconds to ramp up
    tf.forward(.0)
    tf.backward(.0)
    tf.resetCount()
    sleep(1)
    while tf.encoder_counts<=11000:
        tf.forward(.5)
        print(f"f, dc: {i}%, enc_cnt: {tf.encoder_counts}")
        sleep_ms(20)  # 4 seconds to ramp up
    tf.forward(.0)
    tf.backward(.0)
    tf.resetCount()
    sleep(1)
    tf.forward(.0)
    tf.backward(.0)

