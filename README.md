# SmartBin: Pemilah & Pemantau Sampah Berbasis IoT

## Deskripsi Singkat
SmartBin adalah sistem tempat sampah pintar berbasis IoT yang mampu memilah sampah basah dan kering secara otomatis serta memantau kapasitas masing-masing tempat sampah. Sistem ini menggunakan sensor kelembaban dan sensor ultrasonik yang terintegrasi dengan ESP32, serta menampilkan status melalui web.

## Tujuan
1. Meningkatkan efisiensi pengelolaan sampah melalui pemilahan otomatis antara sampah basah dan kering untuk mendukung sistem daur ulang yang lebih baik.

2. Mengurangi volume sampah yang tidak terkelola dengan baik, melalui pemantauan kepenuhan tempat sampah secara real-time dan pemberian notifikasi.

3. Mendorong penerapan teknologi inovatif dalam pengelolaan sampah, seperti penggunaan ESP32 dan sistem IoT.

## SDGs yang Disasar
- 🎯 SDG 11: Sustainable Cities and Communities  
  Mendukung kota dan permukiman yang inklusif, aman, tahan lama, dan berkelanjutan dengan pengelolaan sampah berbasis teknologi.

- 🎯 SDG 12: Responsible Consumption and Production  
  Mendorong pemilahan dan pengelolaan sampah yang bertanggung jawab untuk mengurangi limbah yang mencemari lingkungan.

## Skema Blok Sistem (Visual)

![Skema Blok Sistem]()

> Gambar di atas menggambarkan alur pemilahan dan pemantauan sampah mulai dari proses input oleh pengguna, pendeteksian jenis sampah, pengaturan servo, hingga deteksi penuh dan pengiriman status ke web.

## Daftar Komponen
| Komponen                     | Jumlah | Keterangan                                              |
|-----------------------------|--------|---------------------------------------------------------|
| ESP32                       | 1      | Mikrokontroler utama                                    |
| Sensor Kelembaban DHT-22    | 1      | Deteksi jenis sampah (basah atau kering)                |
| Sensor Ultrasonik HC-SR04   | 2      | Mengukur ketinggian sampah dalam dua tempat             |
| Servo Motor                 | 1      | Mengarahkan dan membuka tutup tempat sampah             |
| Tempat Sampah Fisik         | 2      | Untuk sampah basah dan kering                           |
| Breadboard & Kabel Jumper   | -      | Untuk penyambungan rangkaian                            |
| Power Supply                | 1      | Catu daya sistem                                        |
| Web Interface               | 1      | Menampilkan status tempat sampah secara real-time       |
