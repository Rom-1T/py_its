import os
import asn1tools

# Path to the ASN files using root directory
src_dir = os.path.realpath(os.path.join(os.path.dirname(__file__), ''))
itspdupath = os.path.join(src_dir, 'ASN1', 'ITS', 'ITS-Container.asn')
campath = os.path.join(src_dir, 'ASN1', 'ITS', 'CAM-PDU-Descriptions.asn')
denmpath = os.path.join(src_dir, 'ASN1', 'ITS', 'DENM-PDU-Descriptions.asn')
spat = os.path.join(src_dir, 'ASN1', 'ITS', 'SPATEM-PDU-Descriptions.asn')
ssem_path = os.path.join(src_dir, 'ASN1', 'ITS', 'SSEM-PDU-Descriptions.asn')
srem_path = os.path.join(src_dir, 'ASN1', 'ITS', 'SREM-PDU-Descriptions.asn')
iso19091 = os.path.join(src_dir, 'ASN1', 'ITS', 'ISO-TS-19091-addgrp-C-2018.asn')
iso19321 = os.path.join(src_dir, 'ASN1', 'ITS', 'ISO19321IVIv2.asn')
iso17419 = os.path.join(src_dir, 'ASN1', 'ITS', 'ISO_TS_17419.asn')
dsrc = os.path.join(src_dir, 'ASN1', 'ITS', 'DSRC.asn')
iso14816 = os.path.join(src_dir, 'ASN1', 'ITS', 'ISO14816.asn')
iso14823 = os.path.join(src_dir, 'ASN1', 'ITS', 'ISO14823-missing.asn')
iso24534 = os.path.join(src_dir, 'ASN1', 'ITS',
                        'ISO24534-3_ElectronicRegistrationIdentificationVehicleDataModule-patched.asn')
mcmpath = os.path.join(src_dir, 'ASN1', 'ITS','MCM.asn')
ivimpath = os.path.join(src_dir, 'ASN1', 'ITS','IVIM-PDU-Descriptions.asn')

efcdsrcapplication = os.path.join(src_dir, 'ASN1', 'ITS','ISO14906(2018)EfcDsrcApplicationv6-patched.asn')
efcdsrcgeneric = os.path.join(src_dir, 'ASN1', 'ITS','ISO14906(2018)EfcDsrcGenericv7-patched.asn')


ieee1609Dot2 = os.path.join(src_dir, 'ASN1', 'Security', 'Ieee1609Dot2.asn')
ieee1609Dot2BaseType = os.path.join(src_dir, 'ASN1', 'Security', 'Ieee1609Dot2BaseTypes.asn')
etsiTs103097 = os.path.join(src_dir, 'ASN1', 'Security', 'EtsiTs103097Module.asn')
etsiTs103097Extension = os.path.join(src_dir, 'ASN1', 'Security', 'EtsiTs103097ExtensionModule.asn')
etsiTs103097BaseTypes = os.path.join(src_dir, 'ASN1', 'Security', 'EtsiTs102941BaseTypes.asn')

etsi102941_BT = os.path.join(src_dir, 'ASN1', 'Security', 'EtsiTs102941BaseTypes.asn')
etsi102941_CA = os.path.join(src_dir, 'ASN1', 'Security', 'EtsiTs102941MessagesCa.asn')
etsi102941_ITS = os.path.join(src_dir, 'ASN1', 'Security', 'EtsiTs102941MessagesItss.asn')
etsi102941_OP = os.path.join(src_dir, 'ASN1', 'Security', 'EtsiTs102941MessagesItss-OptionalPrivacy.asn')
etsi102941_TL = os.path.join(src_dir, 'ASN1', 'Security', 'EtsiTs102941TrustLists.asn')
etsi102941_TA = os.path.join(src_dir, 'ASN1', 'Security', 'EtsiTs102941TypesAuthorization.asn')
etsi102941_TA_VA = os.path.join(src_dir, 'ASN1', 'Security', 'EtsiTs102941TypesAuthorizationValidation.asn')
etsi102941_CA_MA = os.path.join(src_dir, 'ASN1', 'Security', 'EtsiTs102941TypesCaManagement.asn')
etsi102941_EN = os.path.join(src_dir, 'ASN1', 'Security', 'EtsiTs102941TypesEnrolment.asn')
etsi102941_link = os.path.join(src_dir, 'ASN1', 'Security', 'EtsiTs102941TypesLinkCertificate(1).asn')

geoNet = os.path.join(src_dir, 'ASN1', 'GEONET.asn')

ssem_foo = asn1tools.compile_files([ssem_path, iso19091, iso24534, itspdupath], 'uper')
mcm_foo = asn1tools.compile_files([mcmpath, iso19091, iso24534, itspdupath, campath], 'uper')
srem_foo = asn1tools.compile_files([srem_path, iso19091, iso24534, itspdupath], 'uper')
spat_foo = asn1tools.compile_files([spat, iso24534, iso19091, itspdupath], 'uper')
cam_foo = asn1tools.compile_files([campath, itspdupath], 'uper')
geonet_foo = asn1tools.compile_files([geoNet], 'uper')
denm_foo = asn1tools.compile_files([denmpath, itspdupath], 'uper')
ivim_foo = asn1tools.compile_files([ivimpath, itspdupath, iso19321, efcdsrcapplication, efcdsrcgeneric, iso14816, iso24534, iso14823, dsrc, iso17419], 'uper')

security_foo = asn1tools.compile_files(
    [etsiTs103097, ieee1609Dot2, ieee1609Dot2BaseType, etsiTs103097BaseTypes], 'oer')
certificate_foo = asn1tools.compile_files(
    [etsiTs103097, ieee1609Dot2,ieee1609Dot2BaseType,etsiTs103097BaseTypes,etsi102941_EN,
     etsi102941_TA, etsi102941_TL, etsi102941_TA_VA, etsi102941_CA_MA, etsi102941_CA], 'oer')
