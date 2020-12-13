from typing import Optional

from fastapi import APIRouter, HTTPException
from pymongo.errors import DuplicateKeyError

from project.dal.partner_repository import PartnerRepository
from project.domain.partner.model import PartnerModel
from project.dal import mongo_connection
from project.domain.partner.partner_service import PartnerService

router = APIRouter(prefix="/partners", tags=["Partners"])

partner_repository = PartnerRepository(mongo_connection)
partner_service = PartnerService(partner_repository)


@router.get("/search")
def get_nearest_partner(long: float, lat: float) -> Optional[PartnerModel]:
    nearest_partner = partner_service.get_nearest_partner_covering_point(long, lat)
    if not nearest_partner:
        raise HTTPException(status_code=404, detail="No partner cover this area")
    return nearest_partner


@router.get("/{partner_id}/", response_model=PartnerModel)
def get_partner_by_id(partner_id: str) -> PartnerModel:
    partner = partner_service.get_partner_by_id(partner_id)
    if not partner:
        raise HTTPException(status_code=404, detail="No partner found")
    return partner


@router.post(
    "/",
    status_code=201,
    responses={
        409: {
            "description": "there is a partner with the provided document"
        }
    }
)
def insert_partner(partner: PartnerModel) -> str:
    try:
        partner_id = partner_service.insert_partner(partner)
    except DuplicateKeyError:
        raise HTTPException(status_code=409, detail="duplicate entry")
    return partner_id
