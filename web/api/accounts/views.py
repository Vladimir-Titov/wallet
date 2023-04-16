from fastapi import Depends
from fastapi_pagination import LimitOffsetPage, paginate

from app.models.account import Account
from app.models.common import base_fields
from app.services.wallet import WalletService
from fastapi_utils.views import view
from utils.pydantic_ext import partial, exclude
from web.api import depends
from . import schemas

tags = ['Account']


@view(tags=tags, summary='Create account', methods=['POST'], response_model=Account)
async def create_account(
    payload: partial(exclude(*base_fields, model=Account)),
    wallet: WalletService = Depends(depends.wallet_service)
):
    return await wallet.accounts_repo.create(**payload.dict())


@view(tags=tags, summary='Search users', methods=['GET'], response_model=LimitOffsetPage[Account])
async def search_account(
    filters: schemas.SearchAccounts = Depends(),
    wallet: WalletService = Depends(depends.wallet_service)
):
    return paginate(await wallet.accounts_repo.search(**filters.dict(exclude_none=True)))
