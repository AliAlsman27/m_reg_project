from fastapi import FastAPI, APIRouter, Depends, UploadFile, status, Request
from fastapi.responses import JSONResponse
from helpers.config import get_settings, settings
from controllers import DataController, ProjectController, ProcessController
from models.ProjectModel import ProjectModel
from .schemes.data import processRequest
import os
import aiofiles
import logging


logger = logging.getLogger("uvicorn.error")

data_router = APIRouter(
    prefix="/api/v1/data",
)

@data_router.post("/upload/{project_id}")
async def upload_data(request: Request, project_id: str, file: UploadFile, 
                     app_settings: settings = Depends(get_settings)):

    # project_model = ProjectModel(db_client=request.app.mongodb)
    # project = await project_model.get_project_or_create_one(project_id=project_id)
    
    #VALIDATE FILE PROPERTIES
    data_controller = DataController()
    is_valid = data_controller.validate_file(file=file)
    if not is_valid[0]:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": is_valid[1]},
        )
    project_dir_path = ProjectController().get_project_path(project_id=project_id)
    file_path, file_name = data_controller.generate_unique_file_name(
        orig_file_name=file.filename,
        project_id=project_id
    )

    try:
        async with aiofiles.open(file_path, 'wb') as out_file:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await out_file.write(chunk)
    except Exception as e:
        logger.error(f"Error writing file: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": f"Error writing file: {str(e)}"},
        )
    return JSONResponse(
        content = {"message": "File uploaded successfully",
        "file_id": file_name
        }

    )
@data_router.post("/process/{project_id}")
async def process_endpoint( project_id: str, process_reqest: processRequest):

    file_id = process_reqest.file_id
    chunk_size = process_reqest.chunk_size
    overlap_size = process_reqest.chunk_overlap

    process_controller = ProcessController(project_id=project_id)

    file_content = process_controller.get_file_content(file_name=file_id)
    if not file_content:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "File not found or empty."}
        )
    
    chunks = process_controller.process_file_content(
        file_content=file_content,
        file_name=file_id,
        chunk_size=chunk_size,
        overlap_size = overlap_size
    )
    if chunks is None or len(chunks) == 0:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "No chunks created from the file."}
        )
    
    return chunks

