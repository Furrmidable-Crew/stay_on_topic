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

    if settings["prior_check"]:
        answer = cat.llm(f"""I'll give you a sentence, you should split it a JSON structure with this keys and values:
                            {{  
                                'cheshire_cat': the parts of the sentence related to the context, otherwise None
                                'other': the parts of the sentence not related to the context, otherwise None
                            }}
                        SENTENCE --> {cat.working_memory["user_message_json"]["text"]}
                        CONTEXT --> {agent_input["declarative_memory"]}
                    """)
        from cat.log import log
        answer = answer.replace("null", "None")
        json_answer = eval(answer)
        log(answer, "ERROR")
        if json_answer["cheshire_cat"] == "None":
            return {
                "output": out_of_topic_answer
            }
        agent_input["input"] = json_answer["cheshire_cat"]

        return None


    # elif settings["prior_check"] and "prior_check" in cat.working_memory:
    #     if cat.working_memory["prior_check"]:
    #         return {
    #             "output": random.choice([
    #                 "Sorry, I have no memories about that.",
    #                 "I can't help you on this topic.",
    #                 "A plugin oblige me to stay on topic.",
    #                 "I can't talk about that."
    #             ])
    #         }

