from pydantic import BaseModel, Field

class SimulationRequest(BaseModel):
    decision: str = Field(min_length=8, max_length=1200)
    category: str = Field(default="General", max_length=100)
    context: str = Field(default="", max_length=2000)
    time_horizon: str = Field(default="6 months", max_length=100)
    constraints: str = Field(default="", max_length=1200)

class AgentInsight(BaseModel):
    agent: str
    summary: str
    benefits: list[str]
    concerns: list[str]
    assumptions: list[str]

class Scenario(BaseModel):
    name: str
    likelihood_label: str
    description: str
    impacts: list[str]
    risks: list[str]
    opportunities: list[str]

class SimulationResponse(BaseModel):
    id: str | None = None
    saved_to_db: bool | None = False
    category: str | None = "General"
    mode: str
    disclaimer: str
    decision: str
    agent_insights: list[AgentInsight]
    scenarios: list[Scenario]
    recommendations: list[str]
    key_assumptions: list[str]
    confidence: str
