# from logging import getLogger
#
# from fastapi import FastAPI
# from starlette.requests import Request
# from x5_aios3_ext import create_s3_client
# from x5_aios3_ext.types import AioS3Client
#
# logger = getLogger(__name__)
#
# __all__ = ('create_s3', 's3')
#
#
# def create_s3(app: FastAPI, conn_settings):
#     @app.on_event('startup')
#     async def create():
#         app.s3 = await create_s3_client(**conn_settings)
#         logger.debug('S3 connection is established')
#
#         @app.on_event('shutdown')
#         async def close():
#             await close_s3_client(app.s3)
#             logger.debug('S3 connection is closed')
#
#
# async def s3(r: Request) -> AioS3Client:
#     return r.app.s3
