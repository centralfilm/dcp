"""
XML utilities for DCP inspection
"""
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
import xmlschema
from pathlib import Path
from typing import Dict, List, Optional, Any


class XMLValidator:
    """Class for XML schema validation of DCP files"""
    
    def __init__(self, xsd_path: Optional[str] = None):
        """
        Initialize XML validator
        
        Args:
            xsd_path: Path to XSD schema directory
        """
        self.xsd_path = xsd_path
    
    def validate_xml(self, xml_file: str, schema_file: Optional[str] = None) -> Dict[str, Any]:
        """
        Validate XML file against schema
        
        Args:
            xml_file: Path to XML file to validate
            schema_file: Path to schema file (if None, try to determine automatically)
            
        Returns:
            Dictionary with validation results
        """
        result = {
            'valid': False,
            'errors': [],
            'warnings': []
        }
        
        try:
            # Parse XML
            tree = ET.parse(xml_file)
            root = tree.getroot()
            
            # If no schema provided, try to determine based on namespace
            if not schema_file and self.xsd_path:
                schema_file = self._get_schema_for_namespace(root)
            
            if schema_file:
                # Validate using xmlschema
                try:
                    xsd = xmlschema.XMLSchema(schema_file)
                    result['valid'] = xsd.is_valid(xml_file)
                    
                    if not result['valid']:
                        # Get validation errors
                        for error in xsd.iter_errors(xml_file):
                            result['errors'].append(str(error))
                except Exception as e:
                    result['errors'].append(f"Schema validation error: {str(e)}")
            else:
                # Just check if XML is well-formed
                result['valid'] = True
                
        except ET.ParseError as e:
            result['errors'].append(f"XML parsing error: {str(e)}")
            result['valid'] = False
        except Exception as e:
            result['errors'].append(f"Validation error: {str(e)}")
            result['valid'] = False
            
        return result
    
    def _get_schema_for_namespace(self, root: Element) -> Optional[str]:
        """
        Determine appropriate schema file based on XML namespace
        
        Args:
            root: Root element of XML document
            
        Returns:
            Path to schema file or None
        """
        if not self.xsd_path:
            return None
            
        # Common DCP namespaces and corresponding schema files
        namespace_to_schema = {
            'http://www.smpte-ra.org/schemas/429-7/2006/CPL': 'CPL.xsd',
            'http://www.digicine.com/PROTO-ASDCP-AM-20040311#': 'AM.xsd',
            'http://www.digicine.com/PROTO-ASDCP-PKL-20040311#': 'PKL.xsd',
            'http://www.smpte-ra.org/schemas/429-17/2006/DCST': 'DCSubtitle.xsd',
        }
        
        # Get namespace from root element
        if root.tag.startswith('{'):
            namespace = root.tag[1:root.tag.index('}')]
            schema_name = namespace_to_schema.get(namespace)
            if schema_name:
                schema_path = Path(self.xsd_path) / schema_name
                if schema_path.exists():
                    return str(schema_path)
        
        return None


def collect_namespaces(root: Element) -> Dict[str, List[Optional[str]]]:
    """
    Collect all namespaces in an XML document similar to the Ruby implementation
    
    Args:
        root: Root element of XML document
        
    Returns:
        Dictionary with namespace URIs as keys and prefixes as values
    """
    namespaces = {}
    
    # Function to recursively collect namespaces
    def collect_from_element(element: Element):
        # Get namespace from tag if it exists
        if element.tag.startswith('{'):
            ns_uri = element.tag[1:element.tag.index('}')].strip()
            prefix = None  # Default namespace
            if ns_uri not in namespaces:
                namespaces[ns_uri] = [prefix]
            elif prefix not in namespaces[ns_uri]:
                namespaces[ns_uri].append(prefix)
        
        # Process attributes for namespace declarations
        for attr, value in element.attrib.items():
            if attr.startswith('xmlns'):
                if ':' in attr:
                    prefix = attr.split(':')[1]
                    ns_uri = value
                else:
                    prefix = None  # Default namespace
                    ns_uri = value
                
                if ns_uri not in namespaces:
                    namespaces[ns_uri] = [prefix]
                elif prefix not in namespaces[ns_uri]:
                    namespaces[ns_uri].append(prefix)
        
        # Recursively process children
        for child in element:
            collect_from_element(child)
    
    collect_from_element(root)
    return namespaces