import os
from dotenv import load_dotenv
from typing import List, Optional

# Load environment variables from .env file
load_dotenv()


class EnvironmentConfig:
    """Environment configuration similar to Node.js style"""
    
    def __init__(self):
        # Support both PORT and APP_PORT for flexibility
        self.PORT: int = int(os.getenv('APP_PORT')  or '8080')
        self.HOST: str = os.getenv('APP_HOST', 'localhost')
        self.DEBUG: bool = os.getenv('DEBUG', 'False').lower() == 'true'
        
        # CORS Origins - split by comma and trim whitespace (support both CORS_ORIGINS and CORS_ORIGIN)
        cors_origins = os.getenv('CORS_ORIGINS') or os.getenv('CORS_ORIGIN') or '*'
        self.CORS_ORIGINS: List[str] = (
            [origin.strip() for origin in cors_origins.split(',')]
            if cors_origins else ['*']
        )
        
        # Database (optional)
        self.MONGODB_URI: Optional[str] = os.getenv('MONGODB_URI')
        
        # API Configuration
        self.PREFIX_API: str = os.getenv('PREFIX_API', '/api')
        self.APP_NAME: str = os.getenv('APP_NAME', 'AI Agent API')
        
        # Gemini API Key
        self.GEMINI_API_KEY: str = self._get_required_env('GEMINI_API_KEY')
    
    def _get_required_env(self, key: str) -> str:
        """Get required environment variable or raise error"""
        value = os.getenv(key)
        if not value:
            raise ValueError(
                f"Environment variable '{key}' is required but not found. "
                f"Please set it in your .env file."
            )
        return value
    
    def to_dict(self) -> dict:
        """Convert config to dictionary"""
        return {
            'port': self.PORT,
            'host': self.HOST,
            'debug': self.DEBUG,
            'cors_origins': self.CORS_ORIGINS,
            'mongodb_uri': self.MONGODB_URI,
            'prefix_api': self.PREFIX_API,
            'app_name': self.APP_NAME,
            'gemini_api_key': '***' + self.GEMINI_API_KEY[-4:] if self.GEMINI_API_KEY else None
        }


# Create singleton instance
env = EnvironmentConfig()


# Legacy functions for backward compatibility
def get_env_variable(key: str, default: str = None) -> str:
    """
    Get environment variable with optional default value
    
    Args:
        key: Environment variable key
        default: Default value if key not found
        
    Returns:
        Environment variable value
    """
    value = os.getenv(key, default)
    if value is None:
        raise ValueError(f"Environment variable {key} not found")
    return value


def get_gemini_api_key() -> str:
    """Get Gemini API key from environment"""
    return env.GEMINI_API_KEY


def get_app_config() -> dict:
    """Get application configuration from environment"""
    return {
        'host': env.HOST,
        'port': env.PORT,
        'debug': env.DEBUG,
        'cors_origins': env.CORS_ORIGINS
    }
