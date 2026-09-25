from pydantic import BaseModel


class Finding(BaseModel):
    title: str
    vulnerability_type: str
    severity: str
    endpoint: str
    description: str
    evidence: str
    recommendation: str