from pydantic import BaseModel, field_validator
from cat.mad_hatter.decorators import plugin


class MySettings(BaseModel):
    memory_filter: bool = True
    n_memories: int = 8
    threshold: float = 0.8
    posterior_check: bool = False
    topic_description: str = ""

    @field_validator("threshold")
    def validate_threshold(threshold: float):
        if threshold < 0 or threshold > 1:
            return ValueError("Threshold must be a value between 0 an 1.")
        
    @field_validator("n_memories")
    def validate_n_memories(n_memories: float):
        if n_memories < 0:
            return ValueError("n_memories must be a greater than 0.")
        

@plugin
def settings_model():
    return MySettings
