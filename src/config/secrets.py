"""
Secure secret management for the application.
Handles API keys and sensitive configuration with proper validation and rotation support.
"""

import os
import hashlib
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from pathlib import Path
from cryptography.fernet import Fernet
import json

logger = logging.getLogger(__name__)


class SecretManager:
    """Manages application secrets securely"""
    
    def __init__(self, encryption_key: Optional[str] = None):
        """
        Initialize the secret manager.
        
        Args:
            encryption_key: Optional encryption key for secret storage
        """
        self._secrets: Dict[str, Any] = {}
        self._last_rotation: Dict[str, datetime] = {}
        self._rotation_interval = timedelta(days=90)  # Rotate secrets every 90 days
        
        # Initialize encryption if key provided
        self._cipher = None
        if encryption_key:
            self._cipher = Fernet(encryption_key.encode() if isinstance(encryption_key, str) else encryption_key)
        
        # Load secrets from environment
        self._load_secrets()
    
    def _load_secrets(self) -> None:
        """Load secrets from environment variables"""
        secret_keys = [
            'OPENAI_API_KEY',
            'AZURE_TEXT_ANALYTICS_KEY',
            'AZURE_TEXT_ANALYTICS_ENDPOINT',
            'GOOGLE_APPLICATION_CREDENTIALS'
        ]
        
        for key in secret_keys:
            value = os.getenv(key)
            if value:
                self._secrets[key] = value
                self._last_rotation[key] = datetime.now()
    
    def get_secret(self, key: str) -> Optional[str]:
        """
        Get a secret value by key.
        
        Args:
            key: The secret key
            
        Returns:
            The secret value or None if not found
        """
        if key not in self._secrets:
            logger.warning(f"Secret '{key}' not found")
            return None
        
        # Check if rotation is needed
        if self._should_rotate(key):
            logger.warning(f"Secret '{key}' should be rotated (age > {self._rotation_interval.days} days)")
        
        return self._secrets.get(key)
    
    def set_secret(self, key: str, value: str) -> None:
        """
        Set a secret value.
        
        Args:
            key: The secret key
            value: The secret value
        """
        if not value:
            logger.error(f"Cannot set empty value for secret '{key}'")
            return
        
        self._secrets[key] = value
        self._last_rotation[key] = datetime.now()
        logger.info(f"Secret '{key}' updated")
    
    def _should_rotate(self, key: str) -> bool:
        """
        Check if a secret should be rotated.
        
        Args:
            key: The secret key
            
        Returns:
            True if the secret should be rotated
        """
        if key not in self._last_rotation:
            return True
        
        age = datetime.now() - self._last_rotation[key]
        return age > self._rotation_interval
    
    def validate_api_key(self, key: str, provider: str = 'openai') -> bool:
        """
        Validate an API key format.
        
        Args:
            key: The API key to validate
            provider: The provider name
            
        Returns:
            True if the key format is valid
        """
        if not key:
            return False
        
        validations = {
            'openai': lambda k: k.startswith('sk-') and len(k) > 20,
            'azure': lambda k: len(k) == 32,
            'google': lambda k: k.endswith('.json') or len(k) > 30
        }
        
        validator = validations.get(provider, lambda k: len(k) > 10)
        return validator(key)
    
    def hash_secret(self, secret: str) -> str:
        """
        Create a hash of a secret for logging/comparison without exposing the value.
        
        Args:
            secret: The secret to hash
            
        Returns:
            A hash of the secret
        """
        if not secret:
            return ""
        
        # Use first 8 and last 4 characters for identification
        if len(secret) > 12:
            masked = f"{secret[:8]}...{secret[-4:]}"
        else:
            masked = "***"
        
        # Create hash for comparison
        hash_value = hashlib.sha256(secret.encode()).hexdigest()[:16]
        
        return f"{masked} (hash: {hash_value})"
    
    def encrypt_secret(self, secret: str) -> Optional[str]:
        """
        Encrypt a secret for storage.
        
        Args:
            secret: The secret to encrypt
            
        Returns:
            Encrypted secret or None if encryption not available
        """
        if not self._cipher:
            logger.warning("Encryption not available - cipher not initialized")
            return None
        
        try:
            encrypted = self._cipher.encrypt(secret.encode())
            return encrypted.decode()
        except Exception as e:
            logger.error(f"Failed to encrypt secret: {e}")
            return None
    
    def decrypt_secret(self, encrypted: str) -> Optional[str]:
        """
        Decrypt a secret from storage.
        
        Args:
            encrypted: The encrypted secret
            
        Returns:
            Decrypted secret or None if decryption fails
        """
        if not self._cipher:
            logger.warning("Decryption not available - cipher not initialized")
            return None
        
        try:
            decrypted = self._cipher.decrypt(encrypted.encode())
            return decrypted.decode()
        except Exception as e:
            logger.error(f"Failed to decrypt secret: {e}")
            return None
    
    def save_secrets(self, filepath: Path) -> bool:
        """
        Save encrypted secrets to a file.
        
        Args:
            filepath: Path to save the secrets
            
        Returns:
            True if successful
        """
        if not self._cipher:
            logger.error("Cannot save secrets - encryption not available")
            return False
        
        try:
            encrypted_secrets = {}
            for key, value in self._secrets.items():
                encrypted = self.encrypt_secret(value)
                if encrypted:
                    encrypted_secrets[key] = encrypted
            
            with open(filepath, 'w') as f:
                json.dump({
                    'secrets': encrypted_secrets,
                    'rotations': {k: v.isoformat() for k, v in self._last_rotation.items()}
                }, f)
            
            logger.info(f"Secrets saved to {filepath}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to save secrets: {e}")
            return False
    
    def load_secrets(self, filepath: Path) -> bool:
        """
        Load encrypted secrets from a file.
        
        Args:
            filepath: Path to load the secrets from
            
        Returns:
            True if successful
        """
        if not self._cipher:
            logger.error("Cannot load secrets - decryption not available")
            return False
        
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            for key, encrypted_value in data.get('secrets', {}).items():
                decrypted = self.decrypt_secret(encrypted_value)
                if decrypted:
                    self._secrets[key] = decrypted
            
            for key, iso_date in data.get('rotations', {}).items():
                self._last_rotation[key] = datetime.fromisoformat(iso_date)
            
            logger.info(f"Secrets loaded from {filepath}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to load secrets: {e}")
            return False
    
    def get_rotation_status(self) -> Dict[str, Dict[str, Any]]:
        """
        Get the rotation status of all secrets.
        
        Returns:
            Dictionary with rotation status for each secret
        """
        status = {}
        
        for key in self._secrets:
            if key in self._last_rotation:
                age = datetime.now() - self._last_rotation[key]
                status[key] = {
                    'last_rotation': self._last_rotation[key].isoformat(),
                    'age_days': age.days,
                    'needs_rotation': self._should_rotate(key),
                    'hash': self.hash_secret(self._secrets[key])
                }
            else:
                status[key] = {
                    'last_rotation': None,
                    'age_days': None,
                    'needs_rotation': True,
                    'hash': self.hash_secret(self._secrets[key])
                }
        
        return status


# Global instance
_secret_manager: Optional[SecretManager] = None


def get_secret_manager() -> SecretManager:
    """Get the global secret manager instance"""
    global _secret_manager
    if _secret_manager is None:
        # Try to load encryption key from environment
        encryption_key = os.getenv('SECRET_ENCRYPTION_KEY')
        if not encryption_key:
            # Generate a new key if not provided (for development only)
            if os.getenv('DEBUG', 'False').lower() == 'true':
                encryption_key = Fernet.generate_key()
                logger.warning("Generated temporary encryption key for development")
        
        _secret_manager = SecretManager(encryption_key)
    
    return _secret_manager