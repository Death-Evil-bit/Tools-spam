# evasion.py
# Teknik menghindari deteksi

class EvasionTechniques:
    @staticmethod
    def random_delay(min_ms=500, max_ms=3000):
        """Delay random dalam milidetik"""
        delay = random.randint(min_ms, max_ms) / 1000
        time.sleep(delay)
        
    @staticmethod
    def rotate_user_agent():
        """Rotasi User-Agent tiap request"""
        agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)',
            'Mozilla/5.0 (Linux; Android 11; SM-G998B)',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        ]
        return random.choice(agents)
        
    @staticmethod
    def add_cookies(session):
        """Tambah cookies random biar keliatan legit"""
        cookies = {
            '_ga': 'GA1.2.' + ''.join([str(random.randint(0,9)) for _ in range(9)]),
            '_gid': 'GA1.2.' + ''.join([str(random.randint(0,9)) for _ in range(9)]),
            'session_id': hashlib.md5(str(time.time()).encode()).hexdigest()
        }
        session.cookies.update(cookies)
        return session