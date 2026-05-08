# Evaluasi Perbandingan nginx load balancer menggunakan Algoritma Round Robin dan Least Connection  

Proyek ini bertujuan untuk membandingkan performa algoritma load balancing menggunakan lingkungan virtual berbasis Docker.

Algoritma yang dibandingkan:
- Round Robin
- Least Connection

Pengujian dilakukan menggunakan beberapa skenario beban dan benchmark menggunakan Ubuntu.  

---

# Struktur Project

```text
project/
│
├── round-robin/
│   ├── docker-compose.yml
│   ├── nginx/
│   │   └── nginx.conf
│   ├── app1/
│   ├── app2/
│   └── app3/
│
└── least-connection/
    ├── docker-compose.yml
    ├── nginx/
    │   └── nginx.conf
    ├── app1/
    ├── app2/
    └── app3/
```

---

# Persiapan

## 1. Install Docker

Cek Docker:

```bash
docker --version
```

Cek container berjalan:

```bash
docker ps
```

---

## 2. Install ApacheBench (Ubuntu / WSL)

```bash
sudo apt update
sudo apt install apache2-utils
```

Cek ApacheBench:

```bash
ab -V
```

---

# Menjalankan Project

## Round Robin

```bash
cd round-robin
docker compose up --build
```

---

## Least Connection

```bash
cd least-connection
docker compose up --build
```

---

# Benchmark Dasar

```bash
ab -n 1000 -c 100 http://localhost:8080/
```

Keterangan:
- `-n 1000` = total request
- `-c 100` = concurrency level

---

# Cara Mengecek Parameter Benchmark

Setelah menjalankan benchmark, akan muncul output seperti:

```bash
Concurrency Level:      100
Time taken for tests:   2.177 seconds
Complete requests:      1000
Failed requests:        0
Requests per second:    459.40 [#/sec]
Time per request:       217.675 [ms]
Transfer rate:          79.13 [Kbytes/sec]
```

---

# Parameter yang Dicatat ke Paper

| Parameter | Keterangan |
|---|---|
| Concurrency Level | Jumlah request bersamaan |
| Requests per second | Jumlah request per detik |
| Time per request | Rata-rata response time |
| Failed requests | Jumlah request gagal |
| Transfer rate | Kecepatan transfer data |
| Time taken for tests | Total waktu benchmark |

---

# Mengecek Monitoring Docker

## 1. Melihat Container Aktif

```bash
docker ps
```

---

## 2. Melihat Penggunaan CPU dan RAM

```bash
docker stats
```

Parameter yang bisa dicatat:
- CPU usage
- Memory usage
- Network I/O

---

## 3. Melihat Log Container

```bash
docker compose logs -f
```

Digunakan untuk:
- melihat distribusi request
- mendeteksi error
- monitoring backend

---

# Skenario Pengujian

---

# Skenario 1 — Semua Server Normal

## Tujuan

Mengukur performa dasar ketika semua backend berjalan normal.

---

## Konfigurasi

Semua backend tanpa delay.

Contoh:

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "SERVER RESPONSE OK"

app.run(host='0.0.0.0', port=5000)
```

---

## Benchmark

```bash
ab -n 1000 -c 100 http://localhost:8080/
```

---

## Ekspektasi

- Performa kedua algoritma hampir sama
- Response stabil

---

# Skenario 2 — Delay 2 Detik

## Tujuan

Mensimulasikan server lambat ringan.

---

## Konfigurasi

### app1

```python
import time

time.sleep(2)
```

---

## Benchmark

```bash
ab -n 1000 -c 100 http://localhost:8080/
```

---

## Ekspektasi

### Round Robin
- Tetap membagi rata request

### Least Connection
- Lebih adaptif terhadap server lambat

---

# Skenario 3 — Delay 5 Detik

## Tujuan

Mensimulasikan bottleneck berat.

---

## Konfigurasi

### app1

```python
time.sleep(5)
```

---

## Ekspektasi

- Round Robin mengalami penurunan performa signifikan
- Least Connection lebih stabil

---

# Skenario 4 — Dua Server Lambat

## Konfigurasi

### app1

```python
time.sleep(2)
```

### app2

```python
time.sleep(2)
```

### app3

Normal.

---

## Tujuan

Mensimulasikan sebagian infrastruktur overload.

---

# Skenario 5 — Server Down

## Tujuan

Menguji fault tolerance.

---

## Menonaktifkan Container

```bash
docker stop round-robin-app1-1
```

atau

```bash
docker stop least-connection-app1-1
```

---

# Skenario 6 — High Concurrency

## Tujuan

Menguji skalabilitas.

---

## Benchmark

### Concurrency 10

```bash
ab -n 1000 -c 10 http://localhost:8080/
```

### Concurrency 50

```bash
ab -n 1000 -c 50 http://localhost:8080/
```

### Concurrency 100

```bash
ab -n 1000 -c 100 http://localhost:8080/
```

### Concurrency 500

```bash
ab -n 1000 -c 500 http://localhost:8080/
```

---

# Skenario 7 — CPU Stress

## Tujuan

Mensimulasikan overload CPU backend.

---

## Konfigurasi

### app1

```python
while True:
    pass
```

⚠ Warning:
Dapat menyebabkan penggunaan CPU tinggi.

---

# Tabel yang Bisa Dimasukkan ke Paper

---

# 1. Tabel Hasil Benchmark

| Algoritma | Skenario | Concurrency | Request/s | Response Time (ms) | Failed Request |
|---|---|---|---|---|---|
| Round Robin | Normal | 100 | 420 | 180 | 0 |
| Least Connection | Normal | 100 | 430 | 175 | 0 |

---

# 2. Tabel Perbandingan Stabilitas Algoritma

| Skenario | Round Robin | Least Connection |
|---|---|---|
| Semua Normal | Stabil | Stabil |
| Delay 2 Detik | Cukup Stabil | Stabil |
| Delay 5 Detik | Tidak Stabil | Stabil |
| Dua Server Lambat | Tidak Stabil | Cukup Stabil |
| Server Down | Cukup Stabil | Stabil |
| High Concurrency | Menurun | Lebih Stabil |
| CPU Stress | Overload | Lebih Adaptif |

---

# 3. Tabel Penggunaan Resource Docker

| Algoritma | CPU Usage | Memory Usage | Network I/O |
|---|---|---|---|
| Round Robin | 78% | 320 MB | 12 MB |
| Least Connection | 60% | 290 MB | 11 MB |

Data diambil dari:

```bash
docker stats
```

---

# 4. Tabel Distribusi Request Backend

| Backend | Round Robin | Least Connection |
|---|---|---|
| APP1 | 333 | 120 |
| APP2 | 333 | 440 |
| APP3 | 334 | 440 |

Tujuan:
- menunjukkan adaptivitas Least Connection

---

# 5. Tabel Persentase Keberhasilan Request

| Algoritma | Total Request | Failed Request | Success Rate |
|---|---|---|---|
| Round Robin | 1000 | 120 | 88% |
| Least Connection | 1000 | 10 | 99% |

---

# 6. Tabel Response Time Berdasarkan Concurrency

| Concurrency | Round Robin (ms) | Least Connection (ms) |
|---|---|---|
| 10 | 30 | 28 |
| 50 | 120 | 90 |
| 100 | 350 | 180 |
| 500 | Timeout | 400 |

---

# Data Penting untuk Overleaf / Paper

Minimal kumpulkan:
- screenshot benchmark
- hasil `ab`
- hasil `docker stats`
- log distribusi request
- grafik benchmark
- tabel response time
- tabel throughput
- tabel failed request

---

# Monitoring Tambahan yang Disarankan

## Cek CPU dan RAM Real-time

```bash
htop
```

Install:

```bash
sudo apt install htop
```

---

# Menghentikan Container

```bash
docker compose down
```

---

# Teknologi yang Digunakan

- Docker
- NGINX
- Python Flask
- ApacheBench(ab)

---

# Kesimpulan yang Diharapkan

- Round Robin cocok untuk beban merata
- Least Connection lebih adaptif pada kondisi server tidak seimbang
- Least Connection menghasilkan response time lebih stabil pada kondisi overload
