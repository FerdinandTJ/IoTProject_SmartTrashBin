from machine import Pin, time_pulse_us
from servo_lib import Servo
import utime
import network
import _thread
import socket
import json

WIFI_SSID = "hihihihi"
WIFI_PASSWORD = "123456789"

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard Tempat Sampah Pintar</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --danger-color: #dc3545;
            --success-color: #28a745;
            --warning-color: #ffc107;
        }
        body { font-family: 'Poppins', sans-serif; background-color: #eef2f7; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .container { background-color: #ffffff; padding: 35px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.08); text-align: center; width: 380px; }
        h1 { font-size: 28px; margin-bottom: 30px; }
        .chart-container { position: relative; width: 200px; height: 200px; margin: 0 auto 30px auto; }
        .chart-text { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); }
        #percentage { font-size: 40px; font-weight: 700; }
        .chart-label { font-size: 14px; color: #6c757d; margin-top: -15px; }
        svg { width: 100%; height: 100%; transform: rotate(-90deg); }
        .chart-background { fill: none; stroke: #e6e6e6; stroke-width: 15; }
        .chart-progress { fill: none; stroke: var(--success-color); stroke-width: 15; stroke-linecap: round; transition: all 0.5s ease-out; }
        .stats-container { display: flex; justify-content: space-around; margin-top: 20px; border-top: 1px solid #eee; padding-top: 20px; }
        .stat-block { display: flex; align-items: center; gap: 12px; }
        .stat-block .icon { width: 40px; height: 40px; background-color: #f8f9fa; border-radius: 50%; display: flex; align-items: center; justify-content: center; }
        .stat-block .icon svg { width: 20px; height: 20px; transform: none; fill: #6c757d; }
        .stat-info { text-align: left; }
        .stat-label { font-size: 14px; color: #6c757d; }
        .stat-value { font-size: 22px; font-weight: 600; }
        .modal-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(0, 0, 0, 0.6); display: flex; justify-content: center; align-items: center; z-index: 1000; opacity: 0; visibility: hidden; transition: opacity 0.3s ease, visibility 0.3s ease; }
        .modal-overlay.visible { opacity: 1; visibility: visible; }
        .modal-content { background-color: white; padding: 30px; border-radius: 15px; width: 90%; max-width: 350px; text-align: center; transform: scale(0.9); transition: transform 0.3s ease; }
        .modal-overlay.visible .modal-content { transform: scale(1); }
        .modal-content .icon { width: 60px; height: 60px; background-color: #fbe9e7; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 20px auto; }
        .modal-content .icon svg { width: 30px; height: 30px; fill: var(--danger-color); }
        .modal-content h2 { font-size: 24px; margin: 0 0 10px 0; color: #333; }
        .modal-content p { font-size: 16px; color: #6c757d; margin-bottom: 25px; }
        #modal-ok-btn { background-color: var(--danger-color); color: white; border: none; padding: 12px 30px; border-radius: 8px; font-size: 16px; font-weight: 600; cursor: pointer; width: 100%; transition: background-color 0.2s ease; }
        #modal-ok-btn:hover { background-color: #c82333; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Dashboard Sampah</h1>
        <div class="chart-container"><svg viewBox="0 0 120 120"><circle class="chart-background" cx="60" cy="60" r="50"></circle><circle class="chart-progress" cx="60" cy="60" r="50"></circle></svg><div class="chart-text"><span id="percentage">0</span>%<div class="chart-label">Kapasitas</div></div></div>
        <div class="stats-container"><div class="stat-block"><div class="icon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M15 2H9v2h6V2zM9 22h6v-2H9v2zm8-2h-2v-2h-2v2h-4v-2H9v2H7v-2H5v2H3v-4h18v4h-2v-2h-2v2zM5 4h14v12H5V4z"/></svg></div><div class="stat-info"><div class="stat-label">Total Buang</div><div class="stat-value" id="counter">0</div></div></div><div class="stat-block"><div class="icon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 15H9v-2h2v2zm0-4H9V7h2v6zm4-2h-2V7h2v6z"/></svg></div><div class="stat-info"><div class="stat-label">Status</div><div class="stat-value" id="status-text">Memuat...</div></div></div></div>
    </div>
    <div class="modal-overlay" id="modal-overlay"><div class="modal-content"><div class="icon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M1 21h22L12 2 1 21zm12-3h-2v-2h2v2zm0-4h-2v-4h2v4z"/></svg></div><h2>Peringatan</h2><p>Tempat sampah sudah penuh. Mohon segera dikosongkan!</p><button id="modal-ok-btn">OK</button></div></div>
    <script>
        document.addEventListener('DOMContentLoaded', function () {
            const progressCircle = document.querySelector('.chart-progress'); const radius = progressCircle.r.baseVal.value; const circumference = 2 * Math.PI * radius;
            progressCircle.style.strokeDasharray = `${circumference} ${circumference}`; progressCircle.style.strokeDashoffset = circumference;
            function setProgress(percent) { const offset = circumference - (percent / 100) * circumference; progressCircle.style.strokeDashoffset = offset; const percentageText = document.getElementById('percentage'); percentageText.innerText = Math.round(percent); if (percent > 85) { progressCircle.style.stroke = 'var(--danger-color)'; percentageText.style.color = 'var(--danger-color)'; } else if (percent > 60) { progressCircle.style.stroke = 'var(--warning-color)'; percentageText.style.color = 'var(--warning-color)'; } else { progressCircle.style.stroke = 'var(--success-color)'; percentageText.style.color = 'var(--success-color)'; } }
            let isPopupShown = false; const modalOverlay = document.getElementById('modal-overlay'); const modalOkBtn = document.getElementById('modal-ok-btn');
            function showPopup() { modalOverlay.classList.add('visible'); }
            function hidePopup() { modalOverlay.classList.remove('visible'); }
            modalOkBtn.addEventListener('click', hidePopup);
            function fetchData() {
                fetch('/data').then(response => response.json())
                .then(data => {
                    document.getElementById('counter').innerText = data.counter; const statusElement = document.getElementById('status-text'); const statusFromServer = data.status_text;
                    if (statusFromServer === 'Penuh' && !isPopupShown) { showPopup(); isPopupShown = true; } else if (statusFromServer !== 'Penuh') { isPopupShown = false; }
                    if (statusFromServer === 'Penuh') { statusElement.innerText = 'Penuh'; statusElement.style.color = 'var(--danger-color)'; } else { statusElement.innerText = 'Tidak Penuh'; statusElement.style.color = 'var(--success-color)'; }
                    setProgress(data.percentage);
                }).catch(error => console.error('Error fetching data:', error));
            }
            setProgress(0); setInterval(fetchData, 2000); fetchData();
        });
    </script>
</body>
</html>
"""

TRIG_PIN_1, ECHO_PIN_1 = 21, 19
TRIG_PIN_2, ECHO_PIN_2 = 5, 18
SERVO_PIN = 26
trig1 = Pin(TRIG_PIN_1, Pin.OUT)
echo1 = Pin(ECHO_PIN_1, Pin.IN)
trig2 = Pin(TRIG_PIN_2, Pin.OUT)
echo2 = Pin(ECHO_PIN_2, Pin.IN)
servo = Servo(SERVO_PIN)
SUDUT_BUKA, SUDUT_TUTUP = 90, 0
TINGGI_TEMPAT_SAMPAH_CM, AMBANG_BATAS_PENUH_CM = 10.7, 2.5

jumlah_pembuangan = 0
persentase_kepenuhan = 0
status_kepenuhan_text = "Inisialisasi..."
status_string_web = "Memuat..."

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print(f"Menghubungkan ke jaringan {WIFI_SSID}...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        while not wlan.isconnected():
            utime.sleep(1)
    ip_address = wlan.ifconfig()[0]
    print(f"Terhubung! Alamat IP: http://{ip_address}")
    return ip_address

def measure_distance(trig_pin, echo_pin):
    trig_pin.value(0)
    utime.sleep_us(2)
    trig_pin.value(1)
    utime.sleep_us(10)
    trig_pin.value(0)
    try:
        return (time_pulse_us(echo_pin, 1, 30000) / 2) / 29.1
    except OSError:
        return None

def cek_status_kepenuhan():
    global persentase_kepenuhan, status_kepenuhan_text, status_string_web
    jarak_sampah = measure_distance(trig2, echo2)
    if jarak_sampah is None:
        return False, "Status: Error Sensor"
    
    if jarak_sampah <= AMBANG_BATAS_PENUH_CM:
        is_full = True
        persentase_kepenuhan = 100
        status_string_web = "Penuh"
    else:
        is_full = False
        persentase = ((TINGGI_TEMPAT_SAMPAH_CM - jarak_sampah) / TINGGI_TEMPAT_SAMPAH_CM) * 100
        persentase_kepenuhan = round(max(0, min(100, persentase)))
        status_string_web = "Tidak Penuh"
        
    status_kepenuhan_text = f"Status: Terisi {persentase_kepenuhan}% (Jarak: {jarak_sampah:.1f} cm)"
    if is_full:
        status_kepenuhan_text = f"Status: PENUH (Jarak: {jarak_sampah:.1f} cm)"
    return is_full, status_kepenuhan_text

def run_web_server():
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(5)
    print('Web server berjalan di port 80')
    
    while True:
        try:
            conn, addr = s.accept()
            request = conn.recv(1024)
            request = str(request)
            
            if 'GET /data' in request:
                data = {'counter': jumlah_pembuangan, 'percentage': persentase_kepenuhan, 'status_text': status_string_web}
                response_body = json.dumps(data)
                conn.send('HTTP/1.0 200 OK\r\n')
                conn.send('Content-Type: application/json\r\n')
                conn.send('Connection: close\r\n\r\n')
                conn.sendall(response_body)
            elif 'GET / ' in request:
                conn.send('HTTP/1.0 200 OK\r\n')
                conn.send('Content-Type: text/html\r\n')
                conn.send('Connection: close\r\n\r\n')
                conn.sendall(HTML_CONTENT)
            else:
                conn.send('HTTP/1.0 404 Not Found\r\n')
                conn.send('Connection: close\r\n\r\n')
            
            conn.close()
        except OSError as e:
            conn.close()

def main_program():
    global jumlah_pembuangan
    servo.move_to_angle(SUDUT_TUTUP)
    print("Program utama (sensor & servo) berjalan.")
    
    while True:
        is_full, status_info = cek_status_kepenuhan()
        print(status_info, end=" | ")
        
        jarak_tangan = measure_distance(trig1, echo1)
        
        if jarak_tangan is not None:
            print(f"Jarak Tangan: {jarak_tangan:.1f} cm")
            
            if jarak_tangan < 20 and not is_full:
                print("Objek terdeteksi! Membuka servo...")
                servo.move_to_angle(SUDUT_BUKA)
                utime.sleep(10)
                servo.move_to_angle(SUDUT_TUTUP)
                print("Servo tertutup.")
                jumlah_pembuangan += 1
                
                print("Menunggu objek menjauh...")
                while True:
                    dist_check = measure_distance(trig1, echo1)
                    if dist_check is None or dist_check > 25:
                        break
                    utime.sleep(0.2)
                    
            elif jarak_tangan < 20 and is_full:
                print("GAGAL MEMBUKA: Tempat sampah sudah penuh!")
                utime.sleep(2)
        else:
            print("Jarak Tangan: -")
            
        utime.sleep(0.5)

try:
    connect_wifi()
    _thread.start_new_thread(run_web_server, ())
    main_program()
except KeyboardInterrupt:
    servo.deinit()
    print("\nProgram dihentikan oleh pengguna.")	