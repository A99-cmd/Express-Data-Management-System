#OpenMV Cam使用镜头校正检测二维码
import sensor, display, pyb, time
from pyb import UART

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA2)
sensor.skip_frames(time=2000)
sensor.set_auto_gain(False)  # must turn this off to prevent image washout...

lcd = display.SPIDisplay()
p5 = pyb.Pin("P5", pyb.Pin.IN, pyb.Pin.PULL_UP)
red_led = pyb.LED(1)
red_led.off()
uart = UART(3, 19200, timeout_char=200)

while True:
    img = sensor.snapshot()
    img.lens_corr(1.8)  # strength of 1.8 is good for the 2.8mm lens.
    for code in img.find_qrcodes():
        img.draw_rectangle(code.rect(), color=(255, 0, 0))
    lcd.write(img)
    while (p5.value()):
        time.sleep_ms(200)
        if (p5.value() == 0):
            red_led.on()
            uart.write(code[4])
        else:
            break