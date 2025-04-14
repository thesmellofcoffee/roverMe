import network
import urequests
from machine import UART, Pin, time_pulse_us
import time
import ujson

SSID = "YOUR_SSID_HERE"
PASSWORD = "YOUR_WIFI_PASSWORD_HERE"
BASE_FIREBASE_URL = "https://your-firebase-project.firebaseio.com/"

LOCATION_URL = BASE_FIREBASE_URL + "rover/location.json"
ISREADY_URL = BASE_FIREBASE_URL + "rover/isReady.json"
COMMAND_URL = BASE_FIREBASE_URL + "user/command/nextCheckpoint.json"

GPS_UART_NUM = 1
GPS_BAUD = 9600
GPS_RX_PIN = 5

ULTRASONIC_TRIG_PIN = 19
ULTRASONIC_ECHO_PIN = 21
DANGER_THRESHOLD = 17

front_left_motor = [Pin(11, Pin.OUT), Pin(10, Pin.OUT)]
rear_left_motor = [Pin(13, Pin.OUT), Pin(12, Pin.OUT)]
front_right_motor = [Pin(7, Pin.OUT), Pin(6, Pin.OUT)]
rear_right_motor = [Pin(3, Pin.OUT), Pin(2, Pin.OUT)]
left_motor_group = front_left_motor + rear_left_motor
right_motor_group = front_right_motor + rear_right_motor

def set_motor_direction(motor, forward, invert):
    if invert:
        if forward:
            motor[0].value(0)
            motor[1].value(1)
        else:
            motor[0].value(1)
            motor[1].value(0)
    else:
        if forward:
            motor[0].value(1)
            motor[1].value(0)
        else:
            motor[0].value(0)
            motor[1].value(1)

def stop_motor(motor):
    motor[0].value(0)
    motor[1].value(0)

def forward_motion(duration):
    set_motor_direction(front_left_motor, True, invert=True)
    set_motor_direction(rear_left_motor, True, invert=True)
    set_motor_direction(front_right_motor, True, invert=False)
    set_motor_direction(rear_right_motor, True, invert=False)
    print("Tüm motorlar ileri hareket ediyor.")
    time.sleep(duration)
    for m in [front_left_motor, rear_left_motor, front_right_motor, rear_right_motor]:
        stop_motor(m)

def backward_motion(duration):
    set_motor_direction(front_left_motor, False, invert=True)
    set_motor_direction(rear_left_motor, False, invert=True)
    set_motor_direction(front_right_motor, False, invert=False)
    set_motor_direction(rear_right_motor, False, invert=False)
    print("Tüm motorlar geri hareket ediyor.")
    time.sleep(duration)
    for m in [front_left_motor, rear_left_motor, front_right_motor, rear_right_motor]:
        stop_motor(m)

def tank_turn_cw(duration):
    set_motor_direction(front_left_motor, True, invert=True)
    set_motor_direction(rear_left_motor, True, invert=True)
    set_motor_direction(front_right_motor, False, invert=False)
    set_motor_direction(rear_right_motor, False, invert=False)
    print("Saat yönünde tank turn (CW) başlıyor.")
    time.sleep(duration)
    for m in [front_left_motor, rear_left_motor, front_right_motor, rear_right_motor]:
        stop_motor(m)
    print("Saat yönünde tank turn (CW) tamamlandı.")

def tank_turn_ccw(duration):
    set_motor_direction(front_left_motor, False, invert=True)
    set_motor_direction(rear_left_motor, False, invert=True)
    set_motor_direction(front_right_motor, True, invert=False)
    set_motor_direction(rear_right_motor, True, invert=False)
    print("Saat yönünün tersinde tank turn (CCW) başlıyor.")
    time.sleep(duration)
    for m in [front_left_motor, rear_left_motor, front_right_motor, rear_right_motor]:
        stop_motor(m)
    print("Saat yönünün tersinde tank turn (CCW) tamamlandı.")

def measure_distance():
    try:
        trig = Pin(ULTRASONIC_TRIG_PIN, Pin.OUT)
        echo = Pin(ULTRASONIC_ECHO_PIN, Pin.IN)
        trig.value(0)
        time.sleep_us(2)
        trig.value(1)
        time.sleep_us(10)
        trig.value(0)
        duration = time_pulse_us(echo, 1, 30000)
        distance = duration / 58.0
        return distance
    except Exception as e:
        print("Mesafe ölçüm hatası:", e)
        return None

def emergency_stop():
    print("ACİL DUR: Engel tespit edildi! Motorlar durduruluyor.")
    for m in [front_left_motor, rear_left_motor, front_right_motor, rear_right_motor]:
        stop_motor(m)
    time.sleep(1)

def check_obstacle():
    d = measure_distance()
    if d is not None and d <= DANGER_THRESHOLD:
        print("Engel tespit edildi: {} cm. Engel kalkana kadar bekleniyor.".format(d))
        emergency_stop()
        while True:
            d = measure_distance()
            if d is not None:
                print("Engel mesafesi: {} cm".format(d))
                if d > DANGER_THRESHOLD:
                    print("Engel kalktı, devam ediliyor.")
                    break
            time.sleep(0.1)

gps = UART(GPS_UART_NUM, baudrate=GPS_BAUD, rx=Pin(GPS_RX_PIN))
buffer = b""
current_location = None

def parse_gprmc(sentence):
    try:
        parts = sentence.split(',')
        if parts[0] != "$GPRMC" or parts[2] != "A":
            return None
        raw_lat = parts[3]
        lat_dir = parts[4]
        raw_lon = parts[5]
        lon_dir = parts[6]
        lat_deg = float(raw_lat[:2])
        lat_min = float(raw_lat[2:])
        latitude = lat_deg + (lat_min / 60.0)
        if lat_dir.upper() == 'S':
            latitude = -latitude
        lon_deg = float(raw_lon[:3])
        lon_min = float(raw_lon[3:])
        longitude = lon_deg + (lon_min / 60.0)
        if lon_dir.upper() == 'W':
            longitude = -longitude
        return (latitude, longitude)
    except Exception as e:
        print("parse_gprmc hata:", e)
        return None

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    print("Wi-Fi’ye bağlanılıyor...")
    wlan.connect(SSID, PASSWORD)
    while not wlan.isconnected():
        time.sleep(0.5)
    print("Wi-Fi Bağlandı:", wlan.ifconfig())

def send_to_firebase(url, data):
    try:
        json_data = ujson.dumps(data)
        headers = {"Content-Type": "application/json"}
        response = urequests.put(url, data=json_data, headers=headers)
        print("Firebase yanıtı:", response.text)
        response.close()
    except Exception as e:
        print("Firebase hatası:", e)

def update_location(lat, lon):
    data = {"lat": str(lat), "lon": str(lon)}
    print("Firebase'e konum verisi gönderiliyor:", data)
    send_to_firebase(LOCATION_URL, data)

def update_isReady(status):
    send_to_firebase(ISREADY_URL, status)

def read_next_checkpoint():
    try:
        response = urequests.get(COMMAND_URL)
        data = response.json()
        response.close()
        if data:
            compass = data.get("compass")
            cp_lat = float(data.get("lat"))
            cp_lon = float(data.get("lon"))
            return compass, cp_lat, cp_lon
    except Exception as e:
        print("Checkpoint okuma hatası:", e)
    return None

def move_to_checkpoint(target_lat, target_lon, threshold=0.0001):
    global current_location
    print("Hedefe ilerleme başladı...")
    while True:
        if current_location is None:
            time.sleep(0.05)
            continue
        current_lat, current_lon = current_location
        if abs(current_lat - target_lat) < threshold and abs(current_lon - target_lon) < threshold:
            print("Hedef checkpoint'e ulaşıldı!")
            break
        forward_motion(1)
        check_obstacle()
        time.sleep(0.05)

current_heading = 0

def turn_to_heading(desired_heading):
    global current_heading
    diff = (desired_heading - current_heading + 180) % 360 - 180
    direction = "CW" if diff > 0 else "CCW"
    turn_angle = abs(diff)
    turn_duration = (turn_angle / 90.0) * 1.3
    print("Dönüş açısı: {}°, yön: {}, süresi: {:.2f} saniye".format(turn_angle, direction, turn_duration))
    if direction == "CW":
        tank_turn_cw(turn_duration)
    else:
        tank_turn_ccw(turn_duration)
    current_heading = desired_heading % 360
    print("Yeni heading:", current_heading)

def main():
    global buffer, current_location, current_heading
    connect_wifi()
    print("GPS başlatıldı, veri akışı bekleniyor...\n")
    while current_location is None:
        if gps.any():
            data = gps.read()
            if data:
                buffer += data
                while b'\n' in buffer:
                    line, buffer = buffer.split(b'\n', 1)
                    try:
                        sentence = line.decode("utf-8").strip()
                        print("Gelen satır:", sentence)
                        if sentence.startswith("$GPRMC"):
                            loc = parse_gprmc(sentence)
                            if loc is not None:
                                current_location = loc
                                print("Geçerli GPS konum alındı:", current_location)
                    except Exception as e:
                        print("Decode hatası:", e)
        time.sleep(0.05)
    lat, lon = current_location
    update_location(lat, lon)
    print("Firebase'e konum verisi gönderildi:", current_location)
    update_isReady(True)
    print("isReady true; nextCheckpoint verisi bekleniyor...")
    last_checkpoint = None
    first_checkpoint_processed = False
    while True:
        checkpoint = read_next_checkpoint()
        if checkpoint is not None:
            compass, cp_lat, cp_lon = checkpoint
            print("nextCheckpoint verisi alındı:", checkpoint)
            if not first_checkpoint_processed:
                if float(compass) != 0:
                    print("Sistem başlangıcında, başlangıç yönü kuzeyden farklı. İlk harekete başlamadan önce istenen yöne dönülüyor.")
                    turn_to_heading(float(compass))
                first_checkpoint_processed = True
            if last_checkpoint != checkpoint:
                last_checkpoint = checkpoint
                update_isReady(False)
                move_to_checkpoint(cp_lat, cp_lon)
                print("İstenen heading (compass):", compass)
                turn_to_heading(float(compass))
                update_isReady(True)
                print("İşlem tamamlandı; isReady true, yeni nextCheckpoint bekleniyor...")
        time.sleep(0.5)

if __name__ == "__main__":
    main()
