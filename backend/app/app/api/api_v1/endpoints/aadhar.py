from fastapi import APIRouter, HTTPException, status, Request, File, Form, UploadFile
from typing import Any
from zipfile import ZipFile
import xml.etree.ElementTree as ET
import os
from app.core.config import settings

router = APIRouter()


@router.post('/kyc', summary='Aadhar eKYC Offline (Paperless) Process', response_model=None)
async def ekyc_offline(request: Request, *, aadhar_file: UploadFile = File(...), code: str = Form(...)) -> Any:
    """

    :param request:
    :param code:
    :param aadhar_file:
    :return:
    """
    try:
        contents = await aadhar_file.read()
        kyc_file = "uploaded_kyc_offline.zip"
        with open(kyc_file, 'wb') as f:
            f.write(contents)

        try:
            with ZipFile(kyc_file, 'r') as zip_ref:
                zip_ref.setpassword(bytes(code, 'utf-8'))
                zip_ref.extractall( "extracted_kyc_offline")
        except RuntimeError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid code or corrupted KYC file.")

        extracted_files = os.listdir("extracted_kyc_offline")
        xml_files = [file for file in extracted_files if file.endswith(".xml")]
        if not xml_files:
            raise HTTPException(
                status_code=status.HTTP_404_NO_FOUND,
                detail="XML file not found in the extracted KYC folder."
            )

        kyc_xml = os.path.join("extracted_kyc_offline", xml_files[0])
        if not os.path.exists(kyc_xml):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid KYC XML file structure.")

        tree = ET.parse(kyc_xml)
        root = tree.getroot()

        address = root.find(".//Poa")
        user_details = {
            "name": root.find(".//Poi").attrib.get('name'),
            "dob": root.find(".//Poi").attrib.get('dob'),
            "gender": root.find(".//Poi").attrib.get('gender'),
            "address": {
                "care_of": address.attrib.get('co'),
                "house": address.attrib.get('house'),
                "street": address.attrib.get('street'),
                "landmark": address.attrib.get('lm'),
                "locality": address.attrib.get('loc'),
                "vtc": address.attrib.get('vtc'),
                "subdist": address.attrib.get('subdist'),
                "district": address.attrib.get('dist'),
                "state": address.attrib.get('state'),
                "pincode": address.attrib.get('pc')
            }
        }
        os.remove(kyc_file)
        for file in extracted_files:
            os.remove(os.path.join("extracted_kyc_offline", file))
        os.rmdir("extracted_kyc_offline")
        return {"message": "KYC verification successful!", "user_details": user_details}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
