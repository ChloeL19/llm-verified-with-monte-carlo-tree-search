from montecarlo.node import Node
from montecarlo.montecarlo import MonteCarlo

from lang import can_be_solution
from lang import score_func_whole as uncached_score_func #NOTE: score_func_whole is generalized score_func

from common_cache import create_cached_func
score_func, cache_stats, reset_cache = create_cached_func(uncached_score_func)
from common_interactive import diffprompt

from prompts import prompt, expansion_count, min_lines, check_func
from common import limit_depth, max_completion_depth
from common_stats import stats

import llm

import tiktoken

def num_tokens_from_string(string: str, encoding_name: str = "cl100k_base") -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def generate_complete(text, montecarlo, current_completion_depth=1):
    if current_completion_depth >= max_completion_depth:
        return None
    prev = text
    texts = llm.generate(text, 1)
    print(f"------number of tokens being sent to the LLM: {num_tokens_from_string(text)}")
    print(f"------texts from the llm in generate_complete: {texts}")
    text = texts[0]
    print(f"------number of tokens from the LLM: {num_tokens_from_string(text)}")
    score = score_func(text)
    print(f"MC OBSERVED SCORE: {score}")
    #print(diffprompt(prev, texts))
    if score is not None:
        if score < 0:
            return None
        else:
            if can_be_solution(text, min_lines, check_func):
                montecarlo.solution = text
            return text
    else:
        print(f"-----text variable when score none before next recursive completion call: {text}")
        return generate_complete(text, montecarlo, current_completion_depth + 1)


def child_finder(node, montecarlo):
    if limit_depth(node):
        return
    
    print(f"!!!!!!Now generating another completion with max completion depth: {max_completion_depth} and limit depth: {limit_depth}")
    #print(f"!!!!!!The state of the current node is: {node.state}")
    text = generate_complete(node.state, montecarlo)
    if text is None:
        node.update_win_value(-1)
    else:
        child = Node(text)
        node.add_child(child)
        child.update_win_value(1)
        child.update_policy_value(1)

        child = Node(node.state)
        node.add_child(child)
        child.update_policy_value(0.2)

def main(mins_timeout = None, prompt = prompt):
    montecarlo = MonteCarlo(Node(prompt), mins_timeout)
    montecarlo.child_finder = child_finder

    montecarlo.simulate(expansion_count)

    print("CHOSEN SOLUTION")
    print(montecarlo.solution)

    stats(montecarlo)
    print('cache stats', cache_stats)
    #with open("graph.dot", "w") as f:
    #    montecarlo.print_tree(f)

    return cache_stats

if __name__ == "__main__":
    main()
