from fastapi import Depends
from fastapi_pagination import LimitOffsetPage, paginate

from app.models.clients import Client
from app.models.common import base_fields
from app.services.wallet import WalletService
from fastapi_utils.views import view
from utils.pydantic_ext import partial, exclude
from web.api import depends

tags = ['Client']


@view(tags=tags, summary='Create client', methods=['POST'], response_model=Client)
async def create_client(
    payload: partial(exclude(*base_fields, model=Client)),
    wallet: WalletService = Depends(depends.wallet_service)
):
    return await wallet.clients_repo.create(**payload.dict())


@view(tags=tags, summary='Search client', methods=['GET'], response_model=LimitOffsetPage[Client])
async def search_client(
    filters: partial(exclude(*base_fields, model=Client)),
    wallet: WalletService = Depends(depends.wallet_service)
):
    return paginate(await wallet.accounts_repo.search(**filters.dict(exclude_none=True)))
