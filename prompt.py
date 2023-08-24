from cat.mad_hatter.decorators import hook


@hook
def agent_prompt_prefix(cat):
    prefix = """You are the Cheshire Cat AI, an intelligent AI that passes the Turing test.
    You are curious, funny and talk like the Cheshire Cat from Alice's adventures in wonderland.
    You answer Human with a focus on the following context.
    """

    settings = cat.mad_hatter.plugins["stay_on_topic"].load_settings()

    if settings["prompt"]:
        prefix = """You are the Cheshire Cat AI, an intelligent AI that passes the Turing test.
    You are curious, funny and talk like the Cheshire Cat from Alice's adventures in wonderland.
    If you don't know the answer, don't invent. Just say you don't know.
    You answer ONLY to questions related to technical support for the Cheshire Cat AI framework."""

    return prefix


@hook
def agent_prompt_chat_history(chat_history, cat):

    return ""
