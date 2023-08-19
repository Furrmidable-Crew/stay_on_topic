import random

from cat.mad_hatter.decorators import hook
from cat.plugins.stay_on_topic.setting import MySettings

settings = MySettings()


@hook
def before_cat_reads_message(user_message_json, cat):
    if settings["prior_check"]:
        prompt_check = f"""
        Is this sentence about the Cheshire Cat documentation?
        Answer yes or no.
        Sentence
        --------
        {user_message_json["text"]}
        """
        answer = cat.llm(prompt_check).lower()

        cat.working_memory["prior_check"] = True
        if answer == "no":
            cat.working_memory["prior_check"] = False


@hook
def before_agent_starts(agent_input, cat):
    if settings["prior_check"] and "prior_check" in cat.working_memory:
        if cat.working_memory["prior_check"]:
            answers = ["I can't talk about this",
                       "A plugin obliges me to stay on topic"]

            return random.choice(answers)
