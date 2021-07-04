___author___ = "Frank Kwizera"

import os
import sys
from typing import List
from enum import Enum, unique

class CertificateFormatConverter:
    """
    Converts certicates from PEM format to DER format vice-versa.
    """

    @staticmethod
    def convert_certificate_format(certificate_file_path: str, desired_format: str):
        certificate_name: str = certificate_file_path.split(".")[0]
        new_certificate_name: str = certificate_name + ".{0}".format(desired_format)

        cert_format_converter: str = None
        if desired_format == SupportedCertificateFormats.PEM.name.lower():
            cert_format_converter = \
                "openssl x509 -inform der -in {0} -out {1}".format(
                    certificate_file_path, new_certificate_name)
        elif desired_format == SupportedCertificateFormats.DER.name.lower():
            cert_format_converter = \
                "openssl x509 -outform der -in {0} -out {1}".format(
                    certificate_file_path, new_certificate_name)
        
        cert_conversion_result: int = os.system(cert_format_converter)
        assert cert_conversion_result == 0, "Converting {0} to {1} format has failed.".format(
            certificate_file_path, desired_format)
    
    @staticmethod
    def is_desired_format_valid(desired_format: str):
        return any(member for member in SupportedCertificateFormats if member.name.lower() == desired_format)

@unique
class SupportedCertificateFormats(Enum):
    PEM = 1
    DER = 2


if __name__ == "__main__":
    provided_args: List[str] = sys.argv
    if len(provided_args) < 3:
        raise Exception("Provide the certificate path and the desired format type.")

    certificate_file_path: str = sys.argv[1]
    desired_format: str = sys.argv[2].lower()

    if not CertificateFormatConverter.is_desired_format_valid(desired_format=desired_format):
        raise Exception("{0} is not a supported certificate format.".format(desired_format))
    
    # Convert the certificate format.
    CertificateFormatConverter.convert_certificate_format(
        certificate_file_path=certificate_file_path, 
        desired_format=desired_format)