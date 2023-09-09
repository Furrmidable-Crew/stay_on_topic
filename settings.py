from pydantic import BaseModel
from cat.mad_hatter.decorators import hook


class MySettings(BaseModel):
    memory_filter: bool = True
    n_memories: int = 8
    threshold: float = 0.8
    posterior_check: bool = False
    topic_description: str = ""


@hook
def plugin_settings_schema():
    return MySettings.schema()
