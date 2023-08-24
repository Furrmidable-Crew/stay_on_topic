from cat.mad_hatter.decorators import hook


@hook
def before_cat_recalls_episodic_memories(episodic_recall_config, cat):
    settings = cat.mad_hatter.plugins["stay_on_topic"].load_settings()
    if settings["memory_filter"]:
        episodic_recall_config["k"] = 0

    return episodic_recall_config


@hook
def before_cat_recalls_declarative_memories(declarative_recall_config, cat):
    settings = cat.mad_hatter.plugins["stay_on_topic"].load_settings()
    if settings["memory_filter"]:
        declarative_recall_config["k"] = settings["n_memories"]
        declarative_recall_config["threshold"] = settings["threshold"]

    return declarative_recall_config


@hook
def before_cat_recalls_procedural_memories(procedural_recall_config, cat):
    settings = cat.mad_hatter.plugins["stay_on_topic"].load_settings()
    if settings["memory_filter"]:
        procedural_recall_config["k"] = 0

    return procedural_recall_config
