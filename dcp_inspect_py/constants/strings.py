"""
String constants for DCP inspection
"""

class MStr:
    """String constants for media types"""
    Stereoscopic_pictures = "Stereoscopic pictures"
    Pictures = "Pictures"
    Mpeg2 = "MPEG-2"
    Audio = "Audio"
    Atmos = "ATMOS"
    Timed_text = "Timed text"


class FileExtensions:
    """File extension constants"""
    DCP_XML = {'.xml', '.cpl', '.pkl', '.am'}
    MXF = '.mxf'
    CERTIFICATE = {'.crt', '.cert'}
    JPEG2000 = '.jp2'
    SUBTITLES = {'.xml', '.ttml'}


class HashAlgorithms:
    """Hash algorithm constants"""
    SHA1 = 'sha1'
    SHA256 = 'sha256'
    MD5 = 'md5'


class EssenceTypes:
    """Essence type constants"""
    PICTURES = "Pictures"
    STEREOSCOPIC_PICTURES = "Stereoscopic pictures"
    AUDIO = "Audio"
    MPEG2 = "MPEG-2"
    ATMOS = "ATMOS"
    TIMED_TEXT = "Timed text"