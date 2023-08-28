import random

from langchain.chains import LLMChain
from langchain.prompts.prompt import PromptTemplate
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser

from cat.mad_hatter.decorators import hook
from cat.log import log


@hook
def before_cat_sends_message(message, cat):
    settings = cat.mad_hatter.plugins["stay_on_topic"].load_settings()

    if settings["posterior_check"]:

        context = cat.mad_hatter.execute_hook("agent_prompt_declarative_memories",
                                              cat.working_memory["declarative_memories"])

        ccat_schema = ResponseSchema(name="support",
                                     description="here the parts of the sentence related to the context, otherwise None")
        other_schema = ResponseSchema(name="other",
                                      description="here the parts of the sentence not related to the context, otherwise None")
        schema = [ccat_schema, other_schema]
        output_parser = StructuredOutputParser.from_response_schemas(schema)

        template = f"""
        Support: a sentence related to asking for technical support about the Cheshire Cat AI framework. E.g. hooks, tools, the Rabbit Hole, The Mad Hatter, plugins and many other topics.
        Other: a sentence that is asking something general, different from the previous topics.
        
        Given this context --> {{context}}
        Rewrite this sentence --> {{text}}

        {{format_instructions}}"""

        prompt = PromptTemplate(
            template=template,
            input_variables=["context", "text"],
            output_parser=output_parser,
            partial_variables={"format_instructions": output_parser.get_format_instructions()}
        )

        chain = LLMChain(
            llm=cat._llm,
            prompt=prompt,
            verbose=True
        )

        answer = chain.run({"context": context,
                            "text": message["content"]})
        log(answer, "CRITICAL")
        output_dict = output_parser.parse(answer)
        log(output_dict, "CRITICAL")

        # prompt = f"""Rewrite the sentence in a JSON with this format:
        #                     {{
        #                         'cheshire_cat': here the parts of the sentence related to the context, otherwise None
        #                         'other': here the parts of the sentence not related to the context, otherwise None
        #                     }}
        #                 SENTENCE --> {message["content"]}
        #                 CONTEXT --> {context}
        #             """
        #
        # answer = cat.llm(prompt)
        #
        # log(f"POSTERIOR**************\n{answer}", "ERROR")
        #
        # answer = answer.replace("null", "None")
        #
        # json_answer = eval(answer)
        #
        message["content"] = output_dict["support"]

        if output_dict["support"] is None:
            message["content"] = random.choice([
                "Sorry, I have no memories about that.",
                "I can't help you on this topic.",
                "A plugin oblige me to stay on topic.",
                "I can't talk about that."
            ])

    return message
