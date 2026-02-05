from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path
from uptime_kuma_api import UptimeKumaException
from .schemas import Maintenance, MaintenanceUpdate, MonitorMaintenance, StatusPageMaintenance
from auth.schemas import JWTSession
from auth.dependencies import get_jwt_session
from config import logger as logging
from .raises import raise_maintenance_not_found

router = APIRouter(redirect_slashes=True)


@router.get("", description="Get all maintenances")
async def get_maintenances(s: JWTSession = Depends(get_jwt_session)):
    try:
        return s.api.get_maintenances()
    except Exception as e:
        logging.fatal(e)
        raise HTTPException(500, str(e))


@router.get("/{maintenance_id}", description="Get maintenances by ID")
async def get_maintenance(maintenance_id: int = Path(...), s: JWTSession = Depends(get_jwt_session)):
    try:
        return s.api.get_maintenance(maintenance_id)
    except UptimeKumaException as e:
        logging.info(e)
        raise_maintenance_not_found()
    except Exception as e:
        logging.fatal(e)
        raise HTTPException(500, str(e))


@router.post("", description="Create a maintenances")
async def create_maintenance(maintenance: Maintenance, s: JWTSession = Depends(get_jwt_session)):
    try:
        return s.api.add_maintenance(**maintenance.dict())
    except TypeError as e:
        logging.error(e)
        raise HTTPException(422, str(e))
    except Exception as e:
        logging.fatal(e)
        raise HTTPException(500, str(e))


@router.patch("/{maintenance_id}", description="Update a specific maintenances")
async def update_maintenance(
        maintenance: MaintenanceUpdate,
        maintenance_id: int = Path(...),
        s: JWTSession = Depends(get_jwt_session)
):
    try:
        return {
            **s.api.edit_maintenance(id_=maintenance_id, **maintenance.dict(exclude_unset=True)),
            "maintenances": maintenance.dict(exclude_unset=True)
        }
    except UptimeKumaException as e:
        logging.info(e)
        raise_maintenance_not_found()
    except TypeError as e:
        logging.error(e)
        raise HTTPException(422, str(e))
    except Exception as e:
        logging.fatal(e)
        raise HTTPException(500, str(e))


@router.delete("/{maintenance_id}", description="Delete a specific Maintenance")
async def delete_maintenance(maintenance_id: int = Path(...), s: JWTSession = Depends(get_jwt_session)):
    try:
        # kinda dumb the api doesnt check if th id exists he just sends an event
        return s.api.delete_maintenance(maintenance_id)
    except UptimeKumaException as e:
        logging.info(e)
        raise_maintenance_not_found()
    except Exception as e:
        logging.fatal(e)
        raise HTTPException(500, str(e))


@router.post("/{maintenance_id}/pause", description="Pause a specific maintenances")
async def pause_maintenance(maintenance_id: int = Path(...), s: JWTSession = Depends(get_jwt_session)):
    try:
        return s.api.pause_maintenance(maintenance_id)
    except UptimeKumaException as e:
        logging.info(e)
        raise_maintenance_not_found()
    except Exception as e:
        logging.fatal(e)
        raise HTTPException(500, str(e))


@router.post("/{maintenance_id}/resume", description="Resume a specific maintenances")
async def resume_maintenance(maintenance_id: int = Path(...), s: JWTSession = Depends(get_jwt_session)):
    try:
        return s.api.resume_maintenance(maintenance_id)
    except UptimeKumaException as e:
        logging.info(e)
        raise_maintenance_not_found()
    except Exception as e:
        logging.fatal(e)
        raise HTTPException(500, str(e))


@router.get("/{maintenance_id}/monitors", description="Get monitors to a maintenances")
async def add_monitor_maintenance(
        maintenance_id: int = Path(...),
        s: JWTSession = Depends(get_jwt_session)
) -> List[dict]:
    try:
        return s.api.get_monitor_maintenance(maintenance_id)
    except UptimeKumaException as e:
        logging.info(e)
        raise_maintenance_not_found()
    except Exception as e:
        logging.fatal(e)
        raise HTTPException(500, str(e))


@router.post("/{maintenance_id}/monitors", description="Adds monitors to a maintenances")
async def add_monitor_maintenance(
        monitors: List[MonitorMaintenance],
        maintenance_id: int = Path(...),
        s: JWTSession = Depends(get_jwt_session)
):
    try:
        mns = [m.dict() for m in monitors]
        return s.api.add_monitor_maintenance(maintenance_id, mns)
    except UptimeKumaException as e:
        logging.info(e)
        raise HTTPException(404, {"message": "Maintenance or monitors not found!"})
    except Exception as e:
        logging.fatal(e)
        raise HTTPException(500, str(e))


@router.get("/{maintenance_id}/status-pages", description="Get status pages to a maintenances")
async def get_status_page_maintenance(
        maintenance_id: int = Path(...),
        s: JWTSession = Depends(get_jwt_session)
) -> List[dict]:
    try:
        return s.api.get_status_page_maintenance(maintenance_id)
    except UptimeKumaException as e:
        logging.info(e)
        raise_maintenance_not_found()
    except Exception as e:
        logging.fatal(e)
        raise HTTPException(500, str(e))


@router.post("/{maintenance_id}/status-pages", description="Adds status pages to a maintenances")
async def add_status_page_maintenance(
        status_pages: List[StatusPageMaintenance],
        maintenance_id: int = Path(...),
        s: JWTSession = Depends(get_jwt_session)
):
    try:
        sps = [s.dict() for s in status_pages]
        return s.api.add_status_page_maintenance(maintenance_id, sps)
    except UptimeKumaException as e:
        logging.info(e)
        raise HTTPException(404, {"message": "Maintenance or status pages not found!"})
    except Exception as e:
        logging.fatal(e)
        raise HTTPException(500, str(e))
