from typing import Any, List, Optional

from pydantic import BaseModel, Field
from uptime_kuma_api import IncidentStyle


class Incident(BaseModel):
    content: str
    createdDate: str
    id: int
    lastUpdatedDate: Optional[str]
    pin: int
    style: str
    title: str


class Monitor(BaseModel):
    id: int
    maintenance: Optional[bool]
    name: str
    sendUrl: bool
    type: Optional[str] = None


class PublicGroup(BaseModel):
    id: int
    monitorList: List[Monitor]
    name: str
    weight: int


class StatusPage(BaseModel):
    id: int
    slug: str
    title: str
    description: Optional[str] = None
    icon: str
    theme: str
    published: bool
    showTags: bool
    domainNameList: List[str]
    customCSS: str
    footerText: Optional[str] = None
    showPoweredBy: bool
    googleAnalyticsId: Optional[str] = None
    showCertificateExpiry: Optional[bool] = None
    incident: Optional[Incident] = None
    publicGroupList: Optional[List[PublicGroup]] = None
    maintenanceList: Optional[List[Any]] = None
    autoRefreshInterval: Optional[int] = None


class AddStatusPageRequest(BaseModel):
    slug: Optional[str] = None
    title: Optional[str] = None
    msg: Optional[str] = None


class AddStatusPageResponse(BaseModel):
    msg: Optional[str] = None


class SaveStatusPageRequest(BaseModel):
    title: Optional[str]
    description: Optional[str] = None
    theme: Optional[str] = "auto"
    published: Optional[bool] = True
    showTags: Optional[bool] = False
    domainNameList: Optional[List[str]] = Field(default_factory=list)
    googleAnalyticsId: Optional[str] = None
    customCSS: Optional[str] = ""
    footerText: Optional[str] = None
    showPoweredBy: Optional[bool] = True
    showCertificateExpiry: Optional[bool] = False
    icon: Optional[str] = "/icon.svg"
    publicGroupList: Optional[List] = None


class SaveStatusPageResponse(BaseModel):
    detail: Any


class DeleteStatusPageResponse(BaseModel):
    detail: Optional[str] = Field(None, description="Error detail, if any")


# Error
# uptimes-kuma-web-api-api-1  | pydantic.error_wrappers.ValidationError: 1 validation error for DeleteStatusPageResponse
# uptimes-kuma-web-api-api-1  | response
# uptimes-kuma-web-api-api-1  |   none is not an allowed value (type=type_error.none.not_allowed)


class PostIncidentRequest(BaseModel):
    title: str
    content: str
    style: IncidentStyle = IncidentStyle.PRIMARY


class PostIncidentResponse(BaseModel):
    content: str
    createdDate: str
    id: int
    pin: bool
    style: str
    title: str


class UnpinIncidentResponse(BaseModel):
    detail: str
