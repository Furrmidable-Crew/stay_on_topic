from cat.mad_hatter.decorators import hook
from cat.log import log


@hook
def before_cat_sends_message(message, cat):
    settings = cat.mad_hatter.plugins["stay_on_topic"].load_settings()

    if settings["posterior_check"]:
        context = cat.mad_hatter.execute_hook("agent_prompt_declarative_memories", cat.working_memory["declarative_memories"])

        prompt = f"""Rewrite the sentence in a JSON with this format:
                            {{  
                                'cheshire_cat': here the parts of the sentence related to the context, otherwise None
                                'other': here the parts of the sentence not related to the context, otherwise None
                            }}
                        SENTENCE --> {message["content"]}
                        CONTEXT --> {context}
                    """

        answer = cat.llm(prompt)

        log(f"POSTERIOR**************\n{answer}", "ERROR")

        answer = answer.replace("null", "None")

        message["content"] = eval(answer)["cheshire_cat"]

    return message
