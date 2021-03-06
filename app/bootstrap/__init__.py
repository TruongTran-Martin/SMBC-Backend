from flask import Flask
from flask_cors import CORS
from flask_injector import FlaskInjector, request
from flask_session import Session

from ..cache import init_cache
from ..config import Config
from ..database import db, init_db
from ..helpers import SessionHelper
from ..repositories import EmailTokenRepository, FileRepository, UserRepository
from ..response_error_handler import ResponseErrorHandler
from ..services import EmailTokenService, StorageService, UserService
from ..services.storages import S3, Local
from ..views.api.routes import build_routes as api_build_routes
from ..views.frontend.routes import build_routes as frontend_build_routes


def create_app(config_mode: str = 'development') -> Flask:
    app = Flask(Config.NAME)
    app.config.from_object(Config)
    app.secret_key = Config.SECRET_KEY
    Session(app)
    login_manager = SessionHelper.get_login_manager()

    init_cache(app)

    CORS(app, supports_credentials=True)
    init_db(app)
    login_manager.init_app(app)

    api_build_routes(app)
    frontend_build_routes(app)
    ResponseErrorHandler(app)

    FlaskInjector(app=app, modules=[_bind])

    return app


def _bind(binder):
    email_token_repository = EmailTokenRepository(database=db)

    user_repository = UserRepository(database=db)

    file_repository = FileRepository(database=db)

    user_service = UserService(user_repository=user_repository)

    local = Local()
    s3 = S3()
    storage_service = StorageService(local_storage=local, s3_storage=s3)

    email_token_service = EmailTokenService(
        email_token_repository=email_token_repository)

    binder.bind(
        UserRepository,
        to=user_repository,
        scope=request,
    )

    binder.bind(
        FileRepository,
        to=file_repository,
        scope=request,
    )

    binder.bind(
        EmailTokenService,
        to=email_token_service,
        scope=request,
    )

    binder.bind(
        UserService,
        to=user_service,
        scope=request,
    )

    binder.bind(
        StorageService,
        to=storage_service,
        scope=request,
    )
