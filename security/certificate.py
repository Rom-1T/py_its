import requests
import tempfile
from encoder.encoding import security_foo, certificate_foo

def fake_certificate():
    return {
        'version': 3,
        'type': 'explicit',
        'issuer': (
            'sha256AndDigest', bytearray.fromhex('80b063a068107b88')
        ),
        'toBeSigned': {
            'id': ('none', None),
            'cracaId': bytearray.fromhex('000000'),
            'crlSeries': 0,
            'validityPeriod': {
                'start': 1425,
                'duration': ('seconds', 60)
            },
            'verifyKeyIndicator': (
                'reconstructionValue',(
                        'compressed-y-1',
                        bytearray.fromhex('2b6a5512a84c92d0d7d742511b02674da2c4abcfae33e9bf4cf58b3fb697e436')
                )
            )
        },
        'signature': (
            'ecdsaNistP256Signature', {
                'rSig': (
                    'x-only', bytearray.fromhex('6cd317b74641cfd49585647b9ac115c3e00b9b2bc6a4e380fb919fd7f7aeca38')
                ),
                'sSig': bytearray.fromhex('e4a44ff4cf0a7c595aa4eb4f4ddf9f396637cf9cb0710ee7f98af7a9a31b397a')
            }
        )
    }
def certificate_to_file(url_pki):
    try:
        # Effectuer une requête GET au serveur PKI pour récupérer le certificat
        reponse = requests.get(url_pki)
        reponse.raise_for_status()  # Vérifier si la requête a réussi
        certificat = reponse.content

        # Créer un fichier temporaire pour stocker le certificat
        with tempfile.NamedTemporaryFile(delete=False) as fichier_temp:
            fichier_temp.write(certificat)

        chemin_fichier_temp = fichier_temp.name
        return chemin_fichier_temp

    except requests.exceptions.RequestException as e:
        print("Erreur lors de la récupération du certificat depuis le PKI:", e)
        return None

def get_certificate(url_pki) :
    try:
        # Effectuer une requête GET au serveur PKI pour récupérer le certificat
        reponse = requests.get(url_pki)
        reponse.raise_for_status()  # Vérifier si la requête a réussi
        certificat = reponse.content

        return certificat

    except requests.exceptions.RequestException as e:
        print("Erreur lors de la récupération du certificat depuis le PKI:", e)
        return None

def open_certifcate(file_path) :
    # Opening the binary file in binary mode as rb(read binary)
    f = open(file_path, mode="rb")

    # Reading file data with read() method
    data = f.read()

    # Closing the opened file
    f.close()

    return data

def decode_certificat(encoded_cert) :
    return security_foo.decode('ExplicitCertificate', encoded_cert)
