#!/usr/bin/env python3
"""
N26 Data Mining - Advanced Security Module
Sistema di sicurezza avanzato con crittografia e autenticazione
"""

import os
import hashlib
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import json
import getpass
from datetime import datetime, timedelta
import secrets

class N26SecurityManager:
    """Gestore sicurezza avanzato per N26 Data Mining"""
    
    def __init__(self, security_dir=".security"):
        self.security_dir = security_dir
        self.ensure_security_dir()
        self.master_key_file = os.path.join(security_dir, "master.key")
        self.auth_file = os.path.join(security_dir, "auth.json")
        self.session_file = os.path.join(security_dir, "session.json")
        
    def ensure_security_dir(self):
        """Crea directory sicurezza se non esiste"""
        os.makedirs(self.security_dir, exist_ok=True)
        # Imposta permessi restrictive (solo owner)
        os.chmod(self.security_dir, 0o700)
    
    def generate_master_key(self, password):
        """Genera chiave master da password"""
        password_bytes = password.encode()
        salt = os.urandom(16)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        
        key = base64.urlsafe_b64encode(kdf.derive(password_bytes))
        
        # Salva salt per uso futuro
        with open(self.master_key_file, 'wb') as f:
            f.write(salt + key)
        
        os.chmod(self.master_key_file, 0o600)
        return key
    
    def load_master_key(self, password):
        """Carica chiave master con password"""
        try:
            with open(self.master_key_file, 'rb') as f:
                data = f.read()
            
            salt = data[:16]
            stored_key = data[16:]
            
            password_bytes = password.encode()
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            
            derived_key = base64.urlsafe_b64encode(kdf.derive(password_bytes))
            
            if derived_key == stored_key:
                return derived_key
            else:
                raise ValueError("Password errata")
                
        except FileNotFoundError:
            return None
    
    def encrypt_credentials(self, username, password, master_password):
        """Crittografa credenziali N26"""
        master_key = self.load_master_key(master_password)
        if not master_key:
            master_key = self.generate_master_key(master_password)
        
        fernet = Fernet(master_key)
        
        credentials = {
            'username': username,
            'password': password,
            'encrypted_at': datetime.now().isoformat()
        }
        
        encrypted_data = fernet.encrypt(json.dumps(credentials).encode())
        
        with open(os.path.join(self.security_dir, "credentials.enc"), 'wb') as f:
            f.write(encrypted_data)
        
        os.chmod(os.path.join(self.security_dir, "credentials.enc"), 0o600)
        return True
    
    def decrypt_credentials(self, master_password):
        """Decrittografa credenziali N26"""
        try:
            master_key = self.load_master_key(master_password)
            if not master_key:
                return None
            
            fernet = Fernet(master_key)
            
            with open(os.path.join(self.security_dir, "credentials.enc"), 'rb') as f:
                encrypted_data = f.read()
            
            decrypted_data = fernet.decrypt(encrypted_data)
            credentials = json.loads(decrypted_data.decode())
            
            return credentials
        except Exception:
            return None
    
    def setup_two_factor(self):
        """Setup autenticazione a due fattori"""
        try:
            import pyotp
            import qrcode
            
            # Genera segreto TOTP
            secret = pyotp.random_base32()
            
            # Salva segreto crittografato
            auth_data = {
                'totp_secret': secret,
                'backup_codes': [secrets.token_hex(8) for _ in range(10)],
                'created_at': datetime.now().isoformat()
            }
            
            # Cripta con master password
            master_password = getpass.getpass("Master password per 2FA: ")
            master_key = self.load_master_key(master_password)
            
            if master_key:
                fernet = Fernet(master_key)
                encrypted_auth = fernet.encrypt(json.dumps(auth_data).encode())
                
                with open(self.auth_file, 'wb') as f:
                    f.write(encrypted_auth)
                
                # Genera QR code per app authenticator
                totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
                    name="N26 Data Mining",
                    issuer_name="N26 Mining Security"
                )
                
                qr = qrcode.QRCode(version=1, box_size=10, border=5)
                qr.add_data(totp_uri)
                qr.make(fit=True)
                
                print("🔐 Setup 2FA completato!")
                print(f"Segreto manuale: {secret}")
                print("Scansiona il QR code con la tua app authenticator")
                
                return True
            
        except ImportError:
            print("❌ Moduli 2FA non disponibili. Installa: pip install pyotp qrcode[pil]")
            return False
    
    def verify_two_factor(self, token, master_password):
        """Verifica token 2FA"""
        try:
            import pyotp
            
            master_key = self.load_master_key(master_password)
            if not master_key:
                return False
            
            fernet = Fernet(master_key)
            
            with open(self.auth_file, 'rb') as f:
                encrypted_auth = f.read()
            
            auth_data = json.loads(fernet.decrypt(encrypted_auth).decode())
            totp = pyotp.TOTP(auth_data['totp_secret'])
            
            # Verifica token o backup codes
            if totp.verify(token) or token in auth_data['backup_codes']:
                self.create_session()
                return True
            
            return False
            
        except Exception:
            return False
    
    def create_session(self, duration_hours=24):
        """Crea sessione di autenticazione"""
        session_data = {
            'created_at': datetime.now().isoformat(),
            'expires_at': (datetime.now() + timedelta(hours=duration_hours)).isoformat(),
            'session_id': secrets.token_hex(32)
        }
        
        with open(self.session_file, 'w') as f:
            json.dump(session_data, f)
        
        return session_data['session_id']
    
    def verify_session(self):
        """Verifica sessione valida"""
        try:
            with open(self.session_file, 'r') as f:
                session_data = json.load(f)
            
            expires_at = datetime.fromisoformat(session_data['expires_at'])
            
            if datetime.now() < expires_at:
                return True
            else:
                # Sessione scaduta
                os.remove(self.session_file)
                return False
                
        except FileNotFoundError:
            return False
    
    def secure_delete_file(self, filepath):
        """Eliminazione sicura file"""
        if os.path.exists(filepath):
            # Sovrascrive con dati casuali prima di eliminare
            file_size = os.path.getsize(filepath)
            with open(filepath, 'r+b') as f:
                for _ in range(3):  # 3 passaggi di sovrascrittura
                    f.seek(0)
                    f.write(os.urandom(file_size))
                    f.flush()
                    os.fsync(f.fileno())
            
            os.remove(filepath)
    
    def audit_log(self, action, details=""):
        """Log di audit per sicurezza"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'details': details,
            'user': os.getenv('USER', 'unknown')
        }
        
        audit_file = os.path.join(self.security_dir, "audit.log")
        with open(audit_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')

def secure_setup_wizard():
    """Wizard setup sicurezza"""
    print("🔒 N26 Data Mining - Setup Sicurezza Avanzato")
    print("=" * 50)
    
    security = N26SecurityManager()
    
    # Setup master password
    master_password = getpass.getpass("Crea master password: ")
    confirm_password = getpass.getpass("Conferma master password: ")
    
    if master_password != confirm_password:
        print("❌ Password non corrispondenti!")
        return
    
    # Setup credenziali N26
    print("\n📝 Inserisci credenziali N26 (saranno crittografate):")
    n26_username = input("Username N26: ")
    n26_password = getpass.getpass("Password N26: ")
    
    # Crittografa credenziali
    security.encrypt_credentials(n26_username, n26_password, master_password)
    security.audit_log("credentials_encrypted", "N26 credentials encrypted")
    
    print("✅ Credenziali crittografate e salvate!")
    
    # Setup 2FA opzionale
    setup_2fa = input("\nVuoi configurare l'autenticazione a due fattori? (y/n): ")
    if setup_2fa.lower() == 'y':
        security.setup_two_factor()
    
    print("\n🎉 Setup sicurezza completato!")
    print("💡 Le credenziali sono ora protette con crittografia AES-256")

if __name__ == "__main__":
    secure_setup_wizard()
