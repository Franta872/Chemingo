# PYTHON imports
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Literal
import random

def random_question(
        elements: set[str], 
        compounds: dict[str, set], 
        question_types: dict[Literal["boolean", "choice", "typing"], bool]
        ):
    from project import count_dictionary_list_items # accessing it locally because of circular import
    random_question: str = "boolean" #random.choice(tuple(x[0] for x in question_types.items() if x[1]))
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
            item_1: str = random.choice(tuple(compounds[random.choice(tuple(compounds.keys()))])) if type == "compound" \
                        else random.choice(tuple(elements))
            item_2 = item_1
        else: # not correct_answer
            while True:
                item_1: str = random.choice(tuple(compounds[random.choice(tuple(compounds.keys()))])) if type == "compound" \
                            else random.choice(tuple(elements))
                item_2: str = random.choice(tuple(compounds[random.choice(tuple(compounds.keys()))])) if type == "compound" \
                            else random.choice(tuple(elements))
                if item_1 != item_2:
                    break
        return (
            random_question,
                {
                "type_1": type,
                "item_1": item_1,
                "appearance_1": appearance[0],
                "type_2": type,
                "item_2": item_2,
                "appearance_2": appearance[1],
                "answer": correct_answer
            }
        )