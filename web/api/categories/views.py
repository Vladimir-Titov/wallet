from fastapi import Depends
from fastapi_pagination import LimitOffsetPage, paginate

from app.models import Category
from app.models.common import base_fields
from app.services.wallet import WalletService
from fastapi_utils.views import view
from utils.pydantic_ext import partial, exclude
from web.api import depends

tags = ['Categories']


@view(tags=tags, summary='Create categories', methods=['POST'], response_model=Category)
async def create_category(
    payload: partial(exclude(*base_fields, model=Category)),
    wallet: WalletService = Depends(depends.wallet_service)
):
    return await wallet.clients_repo.create(**payload.dict())


@view(tags=tags, summary='Search categories', methods=['GET'], response_model=LimitOffsetPage[Category])
async def search_category(
    filters: partial(exclude(*base_fields, model=Category)),
    wallet: WalletService = Depends(depends.wallet_service)
):
    return paginate(await wallet.accounts_repo.search(**filters.dict(exclude_none=True)))
