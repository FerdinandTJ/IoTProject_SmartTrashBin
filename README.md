# IoTProject_SmartTrashBin
# SmartBin: Pemilah & Pemantau Sampah Berbasis IoT

SmartBin adalah sistem tempat sampah pintar berbasis IoT yang mampu memilah sampah basah dan kering secara otomatis menggunakan sensor kelembapan dan servo motor, serta memantau kapasitas tempat sampah secara real-time melalui tampilan web.

---

## 🔧 Fitur Utama
- Pemilahan otomatis sampah basah dan kering menggunakan sensor kelembapan (DHT-22).
- Dua tempat sampah fisik terpisah: basah & kering.
- Pemantauan kapasitas tempat sampah dengan dua sensor ultrasonik HC-SR04.
- Servo motor untuk mengarahkan dan membuka tutup tempat sampah secara otomatis.
- Tampilan web untuk memantau status dan notifikasi secara real-time.

---

## 🔩 Komponen yang Digunakan
| Komponen | Jumlah | Fungsi |
|----------|--------|--------|
| ESP32 | 1 | Mikrokontroler utama |
| DHT-22 | 1 | Sensor kelembapan untuk deteksi jenis sampah |
| HC-SR04 | 2 | Sensor ultrasonik untuk deteksi kapasitas tempat sampah |
| Servo Motor | 2 | Mengarahkan dan membuka tutup tempat sampah |
| Tempat Sampah Fisik | 2 | Sampah basah & kering |
| Web Interface | 1 | Monitoring data secara real-time |
