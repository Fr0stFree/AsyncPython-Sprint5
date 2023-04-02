from pydantic import BaseModel


class ServiceStatus(BaseModel):
    name: str
    status: str
    ping: float | None
    
    @classmethod
    def build(cls, name: str, ping: float | None) -> 'ServiceStatus':
        status = 'NOT AVAILABLE' if ping is None else 'ACTIVE'
        return cls(name=name, status=status, ping=ping)
