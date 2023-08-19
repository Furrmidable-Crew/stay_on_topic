from cat.mad_hatter.decorators import hook
from cat.plugins.stay_on_topic.setting import MySettings

settings = MySettings()


@hook
def before_cat_recalls_episodic_memories(episodic_recall_config, cat):
    if settings["memory_filter"]:
        episodic_recall_config["k"] = 0

    return episodic_recall_config


@hook
def before_cat_recalls_declarative_memories(declarative_recall_config, cat):
    if settings["memory_filter"]:
        declarative_recall_config["k"] = 5
        declarative_recall_config["threshold"] = 0.8

    return declarative_recall_config


@hook
def before_cat_recalls_procedural_memories(procedural_recall_config, cat):
    if settings["memory_filter"]:
        procedural_recall_config["k"] = 0

    return procedural_recall_config
