from typing import List
from config import logger as logging
from fastapi import APIRouter, Depends, Path
from auth.schemas import JWTSession
from auth.dependencies import get_jwt_session
from .schemas import (
    AddStatusPageRequest,
    AddStatusPageResponse,
    DeleteStatusPageResponse,
    PostIncidentRequest,
    PostIncidentResponse,
    SaveStatusPageRequest,
    SaveStatusPageResponse,
    StatusPage,
    UnpinIncidentResponse,
)
from uptime_kuma_api import IncidentStyle, UptimeKumaException
from utils.api import with_exceptions_handling
from response import success

router = APIRouter(redirect_slashes=True)


@router.get("", response_model=List[StatusPage], description="Get all status pages")
async def get_all_status_pages(s: JWTSession = Depends(get_jwt_session)):
    return await with_exceptions_handling(s.api.get_status_pages)


@router.get("/{slug}", response_model=StatusPage, description="Get a status page")
async def get_status_page(slug: str, s: JWTSession = Depends(get_jwt_session)):
    return await with_exceptions_handling(s.api.get_status_page, slug)


@router.post("", response_model=AddStatusPageResponse, description="Add a status page")
async def add_status_page(
        status_page_data: AddStatusPageRequest,
        s: JWTSession = Depends(get_jwt_session)
):
    return await with_exceptions_handling(
        s.api.add_status_page, status_page_data.slug, status_page_data.title
    )


@router.post(
    "/{slug}",
    response_model=SaveStatusPageResponse,
    description="Save a status page"
)
async def save_status_page(
        status_page_data: SaveStatusPageRequest,
        slug: str = Path(...),
        s: JWTSession = Depends(get_jwt_session),
):
    return await with_exceptions_handling(
        s.api.save_status_page,
        slug,
        title=status_page_data.title,
        description=status_page_data.description,
        theme=status_page_data.theme,
        published=status_page_data.published,
        showTags=status_page_data.showTags,
        domainNameList=status_page_data.domainNameList,
        googleAnalyticsId=status_page_data.googleAnalyticsId,
        customCSS=status_page_data.customCSS,
        footerText=status_page_data.footerText,
        showPoweredBy=status_page_data.showPoweredBy,
        showCertificateExpiry=status_page_data.showCertificateExpiry,
        icon=status_page_data.icon,
        publicGroupList=status_page_data.publicGroupList
    )


@router.delete(
    "/{slug}",
    response_model=DeleteStatusPageResponse,
    description="Delete a status page",
)
async def delete_status_page(
        slug: str = Path(...),
        s: JWTSession = Depends(get_jwt_session)
):
    def delete_status_page_api(slug):
        try:
            s.api.delete_status_page(slug)
            return success
        except UptimeKumaException as e:
            raise e
        # catch all other exceptions
        except Exception as e:
            # Exception: 'NoneType' object has no attribute 'values'
            if "NoneType" in str(e):
                logging.info(f"Exception: {e}")
                return success

    return await with_exceptions_handling(delete_status_page_api, slug)


@router.post(
    "/{slug}/incident",
    response_model=PostIncidentResponse,
    description="Post an incident to a status page",
)
async def post_incident(
        slug: str,
        incident_data: PostIncidentRequest,
        s: JWTSession = Depends(get_jwt_session),
):
    return await with_exceptions_handling(
        s.api.post_incident,
        slug,
        incident_data.title,
        incident_data.content,
        incident_data.style or IncidentStyle.PRIMARY,
    )


@router.delete(
    "/{slug}/incident/unpin",
    response_model=UnpinIncidentResponse,
    description="Unpin an incident from a status page",
)
async def unpin_incident(slug: str, s: JWTSession = Depends(get_jwt_session)):
    return await with_exceptions_handling(s.api.unpin_incident, slug)
