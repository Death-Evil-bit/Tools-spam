# proxy_rotator.py
# Tambahkan ini ke tools utama

class ProxyRotator:
    def __init__(self):
        self.proxies = []
        self.current_index = 0
        
    def load_proxies(self, proxy_file='proxies.txt'):
        """Load proxy dari file"""
        with open(proxy_file, 'r') as f:
            self.proxies = [line.strip() for line in f if line.strip()]
        print(f"[✓] {len(self.proxies)} proxy dimuat")
        
    def get_proxy(self):
        """Dapatkan proxy secara round-robin"""
        if not self.proxies:
            return None
            
        proxy = self.proxies[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.proxies)
        return {'http': f'http://{proxy}', 'https': f'http://{proxy}'}
        
    def fetch_free_proxies(self):
        """Ambil proxy gratis dari internet"""
        import requests
        from bs4 import BeautifulSoup
        
        url = 'https://free-proxy-list.net/'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        table = soup.find('table')
        for row in table.find_all('tr')[1:]:
            cols = row.find_all('td')
            if len(cols) > 1:
                ip = cols[0].text
                port = cols[1].text
                self.proxies.append(f"{ip}:{port}")
                
        print(f"[✓] {len(self.proxies)} proxy gratis diambil")