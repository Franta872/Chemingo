# PYTHON imports
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Literal
import random

def random_question(
        elements: set[str], 
        compounds: dict[str, set], 
        question_types: dict[Literal["boolean", "choice", "typing"], bool]
        ) -> dict:
    from project import count_dictionary_list_items # accessing it locally because of circular import
    random_question: Literal["boolean", "choice", "typing"] = random.choice(tuple(x[0] for x in question_types.items() if x[1]))
    if random_question == "boolean":
        possible_types: list = []
        if count_dictionary_list_items(compounds) >= 2:
            possible_types.append("compound")
        if len(elements) >= 2:
            possible_types.append("element")
        type = random.choice(possible_types)
        appearance = random.sample(("name", "symbol"), k=2)
        correct_answer = random.choice((True, False))
        if correct_answer:
            item_1: str = random.choice(tuple(set().union(*compounds.values()))) if type == "compound" \
                        else random.choice(tuple(elements))
            item_2 = item_1
        else: # not correct_answer
            while True:
                item_1: str = random.choice(tuple(set().union(*compounds.values()))) if type == "compound" \
                            else random.choice(tuple(elements))
                item_2: str = random.choice(tuple(set().union(*compounds.values()))) if type == "compound" \
                            else random.choice(tuple(elements))
                if item_1 != item_2:
                    break
        return {
                "random_question": random_question,
                "1": {
                "type": type,
                "item": item_1,
                "appearance": appearance[0]
                },
                "2": {
                "type": type,
                "item": item_2,
                "appearance": appearance[1]
                },
                "answer": correct_answer
            }

    elif random_question == "choice":
        possible_types: list = []
        if count_dictionary_list_items(compounds) >= 4:
            possible_types.append("compound")
        if len(elements) >= 4:
            possible_types.append("element")
        type = random.choice(possible_types)
        appearance = random.sample(("name", "symbol"), k=2)
        items: dict = {}
        if type == "compound":
            for name, value in zip(("1", "2", "3", "4"), random.sample(tuple(set().union(*compounds.values())), k=4)):
                items.update({name: value})
        else: # type == "element"
            for name, value in zip(("1", "2", "3", "4"), random.sample(tuple(elements), k=4)):
                items.update({name: value})

        output: dict = {
                "random_question": random_question,
            }
        for x in ("1", "2", "3", "4", "asked"):
            output.update(
                {
                    x: {
                        "type": type,
                        "item": output[str(random.randint(1, 4))]["item"] if x == "asked" else items[x],
                        "appearance": appearance[0] if x != "asked" else appearance[1]
                    }
                }
            )
        return output

    elif random_question == "typing":
        possible_types: list = []
        if count_dictionary_list_items(compounds) >= 1:
            possible_types.append("compound")
        if len(elements) >= 1:
            possible_types.append("element")
        type = random.choice(possible_types)
        appearance = random.sample(("name", "symbol"), k=2)
        if type == "compound":
            item: str = random.choice(tuple(set().union(*compounds.values())))
        else: # type == "element"
            item = random.choice(tuple(elements))

        return {
                "random_question": random_question,
                "1": {
                    "type": type,
                    "item": item,
                    "appearance": appearance[0]
                },
                "answer": {
                    "type": type,
                    "item": item,
                    "appearance": appearance[1]
                }
            }