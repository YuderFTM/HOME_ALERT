from machine import Pin, I2C, PWM, ADC,SoftI2C
from utime import sleep, sleep_ms
import network, time, urequests
import ujson
import utime
from utelegram import Bot, urequests
from umqtt.simple import MQTTClient


TOKEN = "7495569084:AAFgWJaFP4LqjvTL7d1to84duh0M-VMWb5s"
CHAT_ID = '6736185646'

led = Pin (12, Pin.OUT) #luz led
zum = Pin (14, Pin.OUT)  #zumbador
ldr = ADC(Pin(33)) #servo_motor
sensorMq4 = ADC(Pin(32))  #sensor mq4
fan = Pin (35)#ventilador


#telegram

#chat_id = "Your user ID: 6736185646

#message = "hello from your telegram bot"
#url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
#print(requests.get(url).json()) # this sends the message

# Configura el pin del servomotor como salida PWM
servo_pin = PWM(Pin(4))
servo_freq = 50  # Frecuencia para el servomotor

# Define los valores mínimos y máximos del ciclo de trabajo del servomotor
servo_min_pulse = 30  # Normalmente alrededor de 2.5% del ciclo
servo_max_pulse = 105  # Normalmente alrededor de 12.5% del ciclo

# Configura la frecuencia del PWM
servo_pin.freq(servo_freq)

def map_value(value, in_min, in_max, out_min, out_max): 
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

#configurando sensor mq4
sensorMq4.width(ADC.WIDTH_10BIT)
sensorMq4.atten(ADC.ATTN_11DB)



#conexion a internet
wlan = network.WLAN(network.STA_IF) # create station interface
wlan.active(True)       # activate the interface
wifiList = wlan.scan()             # scan for access points

print('Redes disponibles-----------------------------------------------------------------')
for item in wifiList:
    print('Red:' + str(item[0]) + ' Canal :' + str(item[2]) + ' Señal: ' + str(item[3]) )
print('----------------------------------------------------------------------------------')

wlan.connect('Yaned','Kiara2501') # connect to an AP
while not wlan.isconnected():
        print('Conectando...')
        utime.sleep(1)
print('Conexión establecida!')
print(wlan.ifconfig() )

MQTT_CLIENT_ID = "clientPrrOcQ7RDiego"
MQTT_BROKER    = "broker.hivemq.com"
MQTT_USER      = ""
MQTT_PASSWORD  = ""
MQTT_TOPIC     = "andina/diplomado/python"

bot = Bot(TOKEN)#telegram
print("Conectando a MQTT server... ", MQTT_BROKER, "...", end="")
client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, user=MQTT_USER, password=MQTT_PASSWORD)
client.connect()

#.---------------------------------------------------------------------------------------

#conficuracion lcd
while True:

        lectura = int(sensorMq4.read())
       ## print (lectura)
        utime.sleep(1)
#conversion 
        ppm = 1200 /1023 #particulas por millon
        mt = ppm * lectura
        lectura= (int(mt))
        
        #co = 1001
        print("metano: ",mt , "ppm")
        utime.sleep_ms(1000)
        
        # Calcula el ángulo del servomotor en función del valor del potenciómetro
        servo_angle = int((ppm) * 180)

        # Calcula el ciclo de trabajo del servomotor en función del ángulo
        servo_pulse = int((servo_angle / 180) * (servo_max_pulse - servo_min_pulse) + servo_min_pulse)

        message = ujson.dumps({
            "Partes_por_millon": lectura,
            })

        print("Reportando a MQTT topic {}: {}".format(MQTT_TOPIC, message))
        client.publish(MQTT_TOPIC, message)

        sleep(1)


        #logica
        if mt >=1000:
            led.value(1)
            zum.value(1)
            fan.value(1)
            servo_pin.duty(servo_pulse)
            bot.send_message(CHAT_ID, "Se ha detectado una fuga de gas, se procede a cerrar el registro")

            #print(requests.get(url).json()) # this sends the message
            print("alarma")
            
            
          
        else:
            led.value(0)
            zum.value(0)
            print("no hay alarma")
   
else: 
    print ("Imposible conectar")
    miRed.active(False) 


     