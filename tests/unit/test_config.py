"""
Unit tests for configuration management
"""

import pytest
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

from config.settings import Settings, get_settings
from config.secrets import SecretManager, get_secret_manager


class TestSettings:
    """Test the Settings configuration class"""
    
    def test_settings_initialization(self):
        """Test that settings initialize correctly"""
        settings = Settings()
        
        assert settings.APP_NAME == "Personal Paraguay Fiber Comments Analysis"
        assert settings.APP_VERSION == "2.0.0"
        assert isinstance(settings.BASE_DIR, Path)
        assert settings.PRIMARY_LANGUAGE == "es"
    
    def test_directory_creation(self):
        """Test that necessary directories are created"""
        with patch('pathlib.Path.mkdir') as mock_mkdir:
            settings = Settings()
            
            # Check that mkdir was called for each directory
            assert mock_mkdir.call_count > 0
    
    def test_settings_validation(self):
        """Test settings validation"""
        with patch('config.settings.logger') as mock_logger:
            settings = Settings()
            settings._validate_settings()
            
            # Should warn about missing API key
            if not settings.OPENAI_API_KEY:
                mock_logger.warning.assert_called()
    
    def test_to_dict_conversion(self):
        """Test converting settings to dictionary"""
        settings = Settings()
        settings_dict = settings.to_dict()
        
        assert isinstance(settings_dict, dict)
        assert 'APP_NAME' in settings_dict
        assert 'OPENAI_API_KEY' in settings_dict
    
    def test_get_api_config(self):
        """Test getting API configuration"""
        settings = Settings()
        api_config = settings.get_api_config()
        
        assert isinstance(api_config, dict)
        assert 'openai_api_key' in api_config
        assert 'max_retries' in api_config
        assert api_config['max_retries'] == settings.MAX_RETRIES
    
    def test_get_analysis_config(self):
        """Test getting analysis configuration"""
        settings = Settings()
        analysis_config = settings.get_analysis_config()
        
        assert isinstance(analysis_config, dict)
        assert 'primary_language' in analysis_config
        assert 'batch_size' in analysis_config
        assert analysis_config['batch_size'] == settings.BATCH_SIZE
    
    def test_get_security_config(self):
        """Test getting security configuration"""
        settings = Settings()
        security_config = settings.get_security_config()
        
        assert isinstance(security_config, dict)
        assert 'rate_limit_enabled' in security_config
        assert 'max_file_size_mb' in security_config
    
    @patch.dict(os.environ, {'DEBUG': 'True', 'BATCH_SIZE': '200'})
    def test_environment_override(self):
        """Test that environment variables override defaults"""
        settings = Settings()
        
        assert settings.DEBUG is True
        assert settings.BATCH_SIZE == 200
    
    def test_get_settings_singleton(self):
        """Test that get_settings returns the same instance"""
        settings1 = get_settings()
        settings2 = get_settings()
        
        assert settings1 is settings2


class TestSecretManager:
    """Test the SecretManager class"""
    
    def test_secret_manager_initialization(self):
        """Test secret manager initialization"""
        manager = SecretManager()
        
        assert isinstance(manager._secrets, dict)
        assert isinstance(manager._last_rotation, dict)
    
    def test_set_and_get_secret(self):
        """Test setting and getting secrets"""
        manager = SecretManager()
        
        manager.set_secret('TEST_KEY', 'test_value')
        assert manager.get_secret('TEST_KEY') == 'test_value'
    
    def test_get_nonexistent_secret(self):
        """Test getting a non-existent secret"""
        manager = SecretManager()
        
        assert manager.get_secret('NONEXISTENT') is None
    
    def test_validate_api_key_openai(self):
        """Test OpenAI API key validation"""
        manager = SecretManager()
        
        assert manager.validate_api_key('sk-test123456789012345678', 'openai') is True
        assert manager.validate_api_key('invalid', 'openai') is False
        assert manager.validate_api_key('', 'openai') is False
    
    def test_validate_api_key_azure(self):
        """Test Azure API key validation"""
        manager = SecretManager()
        
        assert manager.validate_api_key('a' * 32, 'azure') is True
        assert manager.validate_api_key('short', 'azure') is False
    
    def test_hash_secret(self):
        """Test secret hashing for logging"""
        manager = SecretManager()
        
        hashed = manager.hash_secret('sk-test123456789012345678')
        assert 'sk-test1' in hashed
        assert '5678' in hashed
        assert 'hash:' in hashed
        assert 'test123456789012345678' not in hashed  # Full secret not exposed
    
    def test_encryption_decryption(self):
        """Test secret encryption and decryption"""
        from cryptography.fernet import Fernet
        
        key = Fernet.generate_key()
        manager = SecretManager(key)
        
        original = 'test_secret_value'
        encrypted = manager.encrypt_secret(original)
        decrypted = manager.decrypt_secret(encrypted)
        
        assert encrypted != original
        assert decrypted == original
    
    def test_rotation_status(self):
        """Test getting rotation status"""
        manager = SecretManager()
        manager.set_secret('TEST_KEY', 'test_value')
        
        status = manager.get_rotation_status()
        
        assert 'TEST_KEY' in status
        assert 'last_rotation' in status['TEST_KEY']
        assert 'age_days' in status['TEST_KEY']
        assert 'needs_rotation' in status['TEST_KEY']
    
    def test_get_secret_manager_singleton(self):
        """Test that get_secret_manager returns singleton"""
        manager1 = get_secret_manager()
        manager2 = get_secret_manager()
        
        assert manager1 is manager2
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'sk-test123'})
    def test_load_secrets_from_environment(self):
        """Test loading secrets from environment variables"""
        manager = SecretManager()
        
        secret = manager.get_secret('OPENAI_API_KEY')
        assert secret == 'sk-test123'