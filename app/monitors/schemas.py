from typing import List, Optional
from pydantic import BaseModel, Field

from uptime_kuma_api import MonitorType, AuthMethod


class Monitor(BaseModel):
    type: MonitorType
    name: str
    parent: Optional[int] = None
    description: Optional[str] = None
    conditions: List = Field(default_factory=list)
    interval: int = 60
    retryInterval: int = 60
    resendInterval: int = 0
    maxretries: int = 1
    upsideDown: bool = False
    notificationIDList: Optional[List] = None

    # HTTP KEYWORD
    url: Optional[str] = None
    expiryNotification: bool = False
    ignoreTls: bool = False
    maxredirects: int = 10
    accepted_statuscodes: Optional[List] = None
    proxyId: Optional[int] = None
    method: str = "GET"
    httpBodyEncoding: str = "json"
    body: Optional[str] = None
    headers: Optional[str] = None
    authMethod: AuthMethod = AuthMethod.NONE
    tlsCert: Optional[str] = None
    tlsKey: Optional[str] = None
    tlsCa: Optional[str] = None
    basic_auth_user: Optional[str] = None
    basic_auth_pass: Optional[str] = None
    authDomain: Optional[str] = None
    authWorkstation: Optional[str] = None

    # OAUTH
    oauth_auth_method: Optional[str] = "client_secret_basic"
    oauth_token_url: Optional[str] = None
    oauth_client_id: Optional[str] = None
    oauth_client_secret: Optional[str] = None
    oauth_scopes: Optional[str] = None

    # GRPC
    grpcUrl: Optional[str] = None
    grpcEnableTls: bool = False
    grpcServiceName: Optional[str] = None
    grpcMethod: Optional[str] = None
    grpcProtobuf: Optional[str] = None
    grpcBody: Optional[str] = None
    grpcMetadata: Optional[str] = None

    timeout: int = 48
    keyword: Optional[str] = None
    invertKeyword: bool = False
    hostname: Optional[str] = None
    packetSize: int = 56
    port: int = 53

    # DNS
    dns_resolve_server: str = "1.1.1.1"
    dns_resolve_type: str = "A"

    # MQTT
    mqttUsername: Optional[str] = None
    mqttPassword: Optional[str] = None
    mqttTopic: Optional[str] = None
    mqttSuccessMessage: Optional[str] = None
    mqttCheckType: str = "keyword"
    mqttWebsocketPath: Optional[str] = None

    # SQLSERVER POSTGRES
    databaseConnectionString: Optional[str] = None
    databaseQuery: Optional[str] = None

    # DOCKER
    docker_container: str = ""
    docker_host: Optional[int] = None

    # RADIUS
    radiusUsername: Optional[str] = None
    radiusPassword: Optional[str] = None
    radiusSecret: Optional[str] = None
    radiusCalledStationId: Optional[str] = None
    radiusCallingStationId: Optional[str] = None

    # GAME
    game: Optional[str] = None
    gamedigGivenPortOnly: bool = False

    jsonPath: Optional[str] = None
    jsonPathOperator: Optional[str] = None
    expectedValue: Optional[str] = None

    # KAFKA
    kafkaProducerBrokers: Optional[str] = None
    kafkaProducerTopic: Optional[str] = None
    kafkaProducerMessage: Optional[str] = None
    kafkaProducerSsl: bool = False
    kafkaProducerAllowAutoTopicCreation: bool = False
    kafkaProducerSaslOptions: Optional[dict] = None

    # 2.0+
    cacheBust: bool = False
    remote_browser: Optional[dict] = None
    snmpVersion: str = "2c"
    rabbitmqNodes: Optional[List] = None
    ipFamily: Optional[str] = None
    ping_numeric: bool = True
    ping_count: int = 3
    ping_per_request_timeout: int = 2
    rabbitmqUsername: Optional[str] = None
    rabbitmqPassword: Optional[str] = None

    class Config:
        use_enum_values = True


class MonitorUpdate(Monitor):
    type: Optional[MonitorType] = None
    name: Optional[str] = None
    conditions: Optional[List] = None


class MonitorTag(BaseModel):
    tag_id: int
    value: Optional[str] = ""
