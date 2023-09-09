import random
from cat.mad_hatter.decorators import hook


@hook
def before_agent_starts(agent_input, cat):
    settings = cat.mad_hatter.plugins["stay_on_topic"].load_settings()

    num_declarative_memories = len(cat.working_memory["declarative_memories"])

    out_of_topic_answer = random.choice([
        "Sorry, I have no memories about that.",
        "I can't help you on this topic.",
        "A plugin oblige me to stay on topic.",
        "I can't talk about that."
    ])

    if settings["memory_filter"] and num_declarative_memories == 0:
        return {
            "output": out_of_topic_answer
        }


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
