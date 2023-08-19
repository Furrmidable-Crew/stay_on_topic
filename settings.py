from pydantic import BaseModel
from cat.mad_hatter.decorators import hook


class MySettings(BaseModel):
    prompt: bool
    prior_check: bool
    memory_filter: bool
    posterior_check: bool


@hook
def plugin_settings_schema():
    return MySettings.schema()
