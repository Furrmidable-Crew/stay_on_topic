from cat.mad_hatter.decorators import hook
from cat.plugins.stay_on_topic.setting import MySettings

settings = MySettings()


@hook
def before_cat_sends_message(message, cat):
    pass
