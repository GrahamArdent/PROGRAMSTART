"""Fail-closed gate for consequential capability conclusions."""
from enum import StrEnum
from pydantic import BaseModel, Field, model_validator

class CapabilityConclusion(StrEnum):
    HUMAN_REQUIRED="human_required"
    UNAVAILABLE="unavailable"
    AUTOMATION_GAP="automation_gap"
    NEW_CAPABILITY_REQUIRED="new_capability_required"
    PATH_SELECTED="path_selected"

ABSENCE_CONCLUSIONS={CapabilityConclusion.HUMAN_REQUIRED,CapabilityConclusion.UNAVAILABLE,CapabilityConclusion.AUTOMATION_GAP,CapabilityConclusion.NEW_CAPABILITY_REQUIRED}

class PathsDiscoveryEvidence(BaseModel):
    actor_ref:str=Field(min_length=1)
    effect_ref:str=Field(min_length=1)
    target_ref:str=Field(min_length=1)
    query_ref:str=Field(min_length=1)
    realization_ids:list[str]=Field(default_factory=list)
    widened_search_performed:bool=False
    owner_native_verification_refs:list[str]=Field(default_factory=list)
    @model_validator(mode="after")
    def normalized(self):
        if any(v!=v.strip() for v in (self.actor_ref,self.effect_ref,self.target_ref,self.query_ref)):
            raise ValueError("Paths discovery references must be normalized")
        if len(self.realization_ids)!=len(set(self.realization_ids)):
            raise ValueError("realization_ids must be unique")
        return self

class CapabilityDiscoveryDecision(BaseModel):
    conclusion:CapabilityConclusion
    discovery:PathsDiscoveryEvidence|None=None

def validate_capability_discovery(decision:CapabilityDiscoveryDecision)->None:
    if decision.discovery is None:
        raise ValueError("consequential capability conclusion requires deterministic Paths discovery evidence")
    e=decision.discovery
    if decision.conclusion in ABSENCE_CONCLUSIONS:
        if e.realization_ids:
            raise ValueError("capability-absence/escalation conclusion conflicts with discovered realization(s)")
        if not e.widened_search_performed:
            raise ValueError("capability-absence/escalation conclusion requires widened equivalent/composition search")
    if decision.conclusion==CapabilityConclusion.PATH_SELECTED and not e.realization_ids:
        raise ValueError("selected path conclusion requires at least one Paths realization")
    if e.realization_ids and not e.owner_native_verification_refs:
        raise ValueError("discovered realization requires owner-native JIT verification before consequential selection")
