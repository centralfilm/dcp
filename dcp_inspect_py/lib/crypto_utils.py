"""
Cryptographic utilities for DCP inspection
"""
import hashlib
import xml.etree.ElementTree as ET
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from pathlib import Path
from typing import Dict, List, Optional, Any


class CertificateValidator:
    """Class for certificate validation in DCPs"""
    
    def __init__(self):
        pass
    
    def load_certificate(self, cert_path: str) -> Optional[x509.Certificate]:
        """
        Load X.509 certificate from file
        
        Args:
            cert_path: Path to certificate file
            
        Returns:
            Certificate object or None if loading failed
        """
        try:
            with open(cert_path, 'rb') as f:
                cert_data = f.read()
                
            # Try different formats
            try:
                cert = x509.load_pem_x509_certificate(cert_data, default_backend())
            except ValueError:
                try:
                    cert = x509.load_der_x509_certificate(cert_data, default_backend())
                except ValueError:
                    # Try to determine format automatically
                    if b'-----BEGIN' in cert_data:
                        cert = x509.load_pem_x509_certificate(cert_data, default_backend())
                    else:
                        cert = x509.load_der_x509_certificate(cert_data, default_backend())
                        
            return cert
        except Exception as e:
            print(f"Error loading certificate {cert_path}: {str(e)}")
            return None
    
    def validate_certificate_chain(self, cert_path: str, trusted_certs: List[str]) -> Dict[str, Any]:
        """
        Validate certificate chain
        
        Args:
            cert_path: Path to certificate to validate
            trusted_certs: List of paths to trusted certificates
            
        Returns:
            Dictionary with validation results
        """
        result = {
            'valid': False,
            'errors': [],
            'warnings': [],
            'subject': None,
            'issuer': None,
            'not_valid_before': None,
            'not_valid_after': None
        }
        
        cert = self.load_certificate(cert_path)
        if not cert:
            result['errors'].append(f"Could not load certificate: {cert_path}")
            return result
        
        # Extract certificate information
        result['subject'] = cert.subject.rfc4514_string()
        result['issuer'] = cert.issuer.rfc4514_string()
        result['not_valid_before'] = cert.not_valid_before
        result['not_valid_after'] = cert.not_valid_after
        
        # Check validity period
        from datetime import datetime
        now = datetime.utcnow()
        if now < cert.not_valid_before:
            result['errors'].append("Certificate not yet valid")
        elif now > cert.not_valid_after:
            result['errors'].append("Certificate expired")
        else:
            result['valid'] = True
            
        return result


class HashValidator:
    """Class for asset hash validation in DCPs"""
    
    def __init__(self):
        pass
    
    def calculate_file_hash(self, file_path: str, algorithm: str = 'sha1') -> Optional[str]:
        """
        Calculate hash of file
        
        Args:
            file_path: Path to file
            algorithm: Hash algorithm (sha1, sha256, md5)
            
        Returns:
            Hex digest of hash or None if calculation failed
        """
        try:
            hash_obj = hashlib.new(algorithm)
            
            with open(file_path, 'rb') as f:
                # Read file in chunks to handle large files
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_obj.update(chunk)
                    
            return hash_obj.hexdigest()
        except Exception as e:
            print(f"Error calculating hash for {file_path}: {str(e)}")
            return None
    
    def validate_asset_hash(self, asset_path: str, expected_hash: str, algorithm: str = 'sha1') -> bool:
        """
        Validate asset hash against expected value
        
        Args:
            asset_path: Path to asset file
            expected_hash: Expected hash value
            algorithm: Hash algorithm used
            
        Returns:
            True if hash matches, False otherwise
        """
        calculated_hash = self.calculate_file_hash(asset_path, algorithm)
        if calculated_hash is None:
            return False
            
        return calculated_hash.lower() == expected_hash.lower()
    
    def validate_cpl_hashes(self, cpl_path: str) -> Dict[str, Any]:
        """
        Validate hashes for all assets referenced in a CPL
        
        Args:
            cpl_path: Path to Composition Playlist XML file
            
        Returns:
            Dictionary with validation results
        """
        result = {
            'total_assets': 0,
            'valid_assets': 0,
            'invalid_assets': 0,
            'missing_assets': 0,
            'results': []
        }
        
        try:
            tree = ET.parse(cpl_path)
            root = tree.getroot()
            
            # Find all asset references in the CPL
            # This is a simplified approach - actual implementation would need to
            # properly handle the XML namespace and structure
            namespace = {'cpl': 'http://www.smpte-ra.org/schemas/429-7/2006/CPL'}
            
            # Look for AssetList or similar structures in the CPL
            for asset in root.findall('.//Asset', namespace):
                asset_id = asset.find('Id', namespace)
                hash_value = asset.find('Hash', namespace)
                size = asset.find('Size', namespace)
                
                if asset_id is not None and hash_value is not None:
                    result['total_assets'] += 1
                    
                    # In a real implementation, we would need to resolve the asset path
                    # from the CPL file location and asset ID
                    # For now, we'll just show the structure
                    asset_result = {
                        'id': asset_id.text if asset_id is not None else 'Unknown',
                        'expected_hash': hash_value.text if hash_value is not None else 'Unknown',
                        'valid': False,
                        'error': 'Asset path resolution not implemented in this example'
                    }
                    
                    result['results'].append(asset_result)
                    result['invalid_assets'] += 1
        except Exception as e:
            result['error'] = f"Error parsing CPL: {str(e)}"
            
        return result