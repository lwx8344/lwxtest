import RPi.GPIO as GPIO
import time
Trig_Pin = 23  #超声波发送脚
Echo_Pin = 24  #超声波接收检测脚

GPIO.setmode(GPIO.BCM)
GPIO.setup(Trig_Pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Echo_Pin, GPIO.IN)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)
pwm = GPIO.PWM(18,10000)
pwm.start(97)
time.sleep(1)


temp=0;
class MyTimer():

   # 初始化构造函数
   def __init__(self):
       
       self.t = 0
       self.begin = 0
       self.end = 0

   # 开始计时
   def start(self):
       self.begin = time.time()
       print ("计时开始....")

   # 结束计时    
   def stop(self):
       self.end = time.time()
       self.calc()
       print ("计时结束...")

   # 计算运行时间   
   def calc(self):
       self.t = self.end-self.begin
       print(self.t)

def checkdist():
    GPIO.output(Trig_Pin, GPIO.HIGH)
    time.sleep(0.00015)
    GPIO.output(Trig_Pin, GPIO.LOW)
    while not GPIO.input(Echo_Pin):
        pass
    t1 = time.time()
    while GPIO.input(Echo_Pin):
        pass
    t2 = time.time()
    return (t2 - t1) * 340 * 100 / 2

my = MyTimer()   #实例化一个类对象
my.start() 
try:
    while True:
        print('距离:', checkdist(), 'cm')
        if(checkdist()<30) and temp==0:
            pwm.ChangeDutyCycle(0)
            my.stop() 
            temp=1;
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
