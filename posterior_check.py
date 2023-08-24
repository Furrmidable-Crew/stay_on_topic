import random

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

        json_answer = eval(answer)

        message["content"] = json_answer["cheshire_cat"]

        if json_answer["cheshire_cat"] == "None":
            message["content"] = random.choice([
                "Sorry, I have no memories about that.",
                "I can't help you on this topic.",
                "A plugin oblige me to stay on topic.",
                "I can't talk about that."
            ])

    return message
