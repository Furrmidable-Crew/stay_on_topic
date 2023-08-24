from pydantic import BaseModel
from cat.mad_hatter.decorators import hook


class MySettings(BaseModel):
    prompt: bool = True
    prior_check: bool = False
    memory_filter: bool = False
    posterior_check: bool = False
    n_memories: int = 8
    threshold: float = 0.8


@hook
def plugin_settings_schema():
    return MySettings.schema()
