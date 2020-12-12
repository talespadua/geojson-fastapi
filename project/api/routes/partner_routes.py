from fastapi import APIRouter, HTTPException
from pymongo.errors import DuplicateKeyError

from project.dal.mongo_connection import MongoConnection
from project.dal.partner_dal import PartnerDAL
from project.domain.partner.model import PartnerModel
from project.config import settings


router = APIRouter(prefix="/items", tags=["Partners"])

mongo_connection = MongoConnection(
    db_connection=settings.DB_CONNECTION_STRING, db_name=settings.DB_NAME
)

partner_dal = PartnerDAL(mongo_connection)


@router.get("/{partner_id}/", response_model=PartnerModel)
def get_partner_by_id(partner_id: str) -> PartnerModel:
    partner = partner_dal.get_partner_by_id(partner_id)
    if not partner:
        raise HTTPException(status_code=404, detail="No partner found")
    return partner


@router.post("/", status_code=201)
def insert_partner(partner: PartnerModel) -> str:
    try:
        response = partner_dal.insert_partner(partner)
    except DuplicateKeyError:
        raise HTTPException(status_code=409, detail="duplicate entry")
    return str(response.inserted_id)
