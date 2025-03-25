import unittest
from unittest.mock import patch, Mock
import requests
from url_resolver import URLResolver

class TestURLResolver(unittest.TestCase):
    
    def setUp(self):
        self.resolver = URLResolver()
    
    @patch('requests.head')
    def test_resolve_bitly(self, mock_head):
        # Setup mock
        mock_response = Mock()
        mock_response.url = 'https://example.com/gpg-key'
        mock_head.return_value = mock_response
        
        # Test function
        result = self.resolver.resolve_bitly('https://bit.ly/abc123')
        
        # Assertions
        self.assertEqual(result, 'https://example.com/gpg-key')
        mock_head.assert_called_once_with(
            'https://bit.ly/abc123', 
            allow_redirects=True, 
            timeout=10
        )
    
    @patch('requests.head')
    def test_resolve_bitly_error(self, mock_head):
        # Setup mock to raise exception
        mock_head.side_effect = requests.RequestException('Network error')
        
        # Test function raises exception
        with self.assertRaises(ValueError):
            self.resolver.resolve_bitly('https://bit.ly/abc123')
    
    @patch('requests.get')
    def test_fetch_content(self, mock_get):
        # Setup mock
        mock_response = Mock()
        mock_response.text = '-----BEGIN PGP PUBLIC KEY BLOCK-----\nkey data\n-----END PGP PUBLIC KEY BLOCK-----'
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        # Test function
        result = self.resolver.fetch_content('https://example.com/gpg-key')
        
        # Assertions
        self.assertIn('BEGIN PGP PUBLIC KEY BLOCK', result)
        mock_get.assert_called_once_with(
            'https://example.com/gpg-key', 
            timeout=10
        )
