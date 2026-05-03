from src.infrastructure.config import ConfigStatus
from src.infrastructure.db.models import Base, ResourceModel
from src.infrastructure.db.IDB import InfrastructureDB
from src.infrastructure.db.uow import SQLAlchemyUnitOfWork
from src.application.services import ResourceService
from src.domain.exceptions import ResourceNotFound
from src.application.dto import ResourceCreateDTO, ResourceReadDTO
from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from uuid import UUID
from typing import List


config = ConfigStatus.test
db = InfrastructureDB(config)

@asynccontextmanager
async def lifespan(app:FastAPI):
    db.init_db()
    yield

app = FastAPI(title='Resources API', lifespan=lifespan)

def get_uow():
    session = db.get_session()
    uow = SQLAlchemyUnitOfWork(session_factory=lambda: session)
    try:
        yield uow
    finally:
        session.close()

def get_resource_service(uow = Depends(get_uow)):
    return ResourceService(uow)

@app.exception_handler(ResourceNotFound)
def resource_not_found_handler(request: Request, exception: ResourceNotFound):
    return JSONResponse(
        status_code=404,
        content={
            'error': 'Resource not found',
            'status': 404,
            'message': str(exception),
            'path': request.url.path,
        }
    )

@app.post('/resources', response_model=ResourceReadDTO)
def post_resources(payload: ResourceCreateDTO, service: ResourceService = Depends(get_resource_service)):
    resource = service.create_resource(name=payload.name, metadata=payload.metadata)
    return resource

@app.get('/resources/{resource_id}', response_model=ResourceReadDTO)
def get_resource(resource_id: UUID, service: ResourceService = Depends(get_resource_service)):
    resource = service.get_resource(resource_id=resource_id)
    return resource

@app.patch('/resources/{resource_id}/activate')
def activate_resource(resource_id: UUID, service: ResourceService = Depends(get_resource_service)):
    service.activate_resource(resource_id=resource_id)
    return {'message': 'Resource activated successfully'}

@app.get('/resources', response_model=List[ResourceReadDTO])
def get_list_resources(service: ResourceService = Depends(get_resource_service)):
    list_resource = service.list_all_resources()
    return list_resource
