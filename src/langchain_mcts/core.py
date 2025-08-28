"""Core MCTS functionality for LangChain integration."""

from typing import Any, Dict, List, Optional, Union
import math
import random
import re
import numpy as np
from langchain_core.language_models.base import BaseLanguageModel
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain.tools import tool


DEFAULT_SEED_ANSWERS = [
    "I don't know the answer",
    "I'm not sure", 
    "I can't say",
]

MAX_CHILDREN = 3


class MCTSNode:
    """Represents a node in the MCTS tree."""
    
    def __init__(self, question: str, answer: str, parent: Optional['MCTSNode'] = None):
        """
        Initialize MCTS Node.
        
        Args:
            question: The question being addressed
            answer: The answer for this node
            parent: Parent node
        """
        self.question = question
        self.answer = answer
        self.parent = parent
        self.children: List['MCTSNode'] = []
        self.visits = 0
        self.value = 0.0
        
    def is_fully_expanded(self) -> bool:
        """Check if node is fully expanded."""
        return len(self.children) >= MAX_CHILDREN
    
    def best_child(self, exploration_weight: float = 1.41) -> 'MCTSNode':
        """
        Select best child using UCB1 formula.
        
        Args:
            exploration_weight: Exploration parameter for UCB1
            
        Returns:
            Best child node
        """
        choices_weights = []
        for child in self.children:
            if child.visits == 0:
                weight = float('inf')
            else:
                exploitation = child.value / child.visits
                exploration = exploration_weight * math.sqrt((2 * math.log(self.visits) / child.visits))
                weight = exploitation + exploration
            choices_weights.append(weight)
        return self.children[np.argmax(choices_weights)]
    
    def most_visited_child(self) -> 'MCTSNode':
        """Return the most visited child node."""
        return max(self.children, key=lambda child: child.visits)
    
    def add_child(self, child_node: 'MCTSNode') -> None:
        """Add a child node."""
        self.children.append(child_node)


class MCTS:
    """Monte Carlo Tree Search implementation for LLM response improvement."""
    
    def __init__(self, question: str, llm: BaseLanguageModel, seed_answers: Optional[List[str]] = None, iterations: int = 2):
        """
        Initialize MCTS.
        
        Args:
            question: The question to search for answers
            llm: Language model to use
            seed_answers: Initial seed answers
            iterations: Number of MCTS iterations
        """
        self.question = question
        self.llm = llm
        self.seed_answers = seed_answers or DEFAULT_SEED_ANSWERS
        self.iterations = iterations
        self.root = MCTSNode(question, random.choice(self.seed_answers))
        
    def search(self) -> str:
        """
        Run MCTS search to find best answer.
        
        Returns:
            Best answer found
        """
        for i in range(self.iterations):
            print(f"\nIteration {i+1}/{self.iterations}")
            node = self.select(self.root)
            print(f"Selected Node: {node.answer}")
            
            if not node.is_fully_expanded():
                node = self.expand(node)
                print(f"Expanded Node: {node.answer}")
                
            reward = self.simulate(node)
            print(f"Simulated Reward: {reward}")
            self.backpropagate(node, reward)
            
        print(f"Visits to most visited child: {self.root.most_visited_child().visits}")
        return self.root.most_visited_child().answer
    
    def select(self, node: MCTSNode) -> MCTSNode:
        """Select a node for expansion using UCB1."""
        while node.is_fully_expanded() and node.children:
            node = node.best_child()
        return node
    
    def expand(self, node: MCTSNode) -> MCTSNode:
        """Expand a node by creating improved children."""
        for j in range(MAX_CHILDREN - len(node.children)):
            child_node = MCTSNode(self.question, node.answer, parent=node)
            node.add_child(child_node)
            
            critique = self.get_critique(self.question, child_node.answer)
            print(f"\n--Critique {j}--\n{critique}")
            
            improved_answer = self.improve_answer(self.question, child_node.answer, critique)
            print(f"\n--Improved answer: {j}--\n{improved_answer}")
            
            child_node.answer = improved_answer
            
        return random.choice(node.children)
    
    def simulate(self, node: MCTSNode) -> float:
        """Simulate from a node by rating the answer."""
        return self.rate_answer(self.question, node.answer)
    
    def backpropagate(self, node: MCTSNode, reward: float) -> None:
        """Backpropagate reward through the tree."""
        while node is not None:
            node.visits += 1
            node.value += reward
            node = node.parent
            
    def get_critique(self, question: str, draft_answer: str) -> str:
        """Get critique of a draft answer."""
        prompt = (
            f"Question: {question}\n"
            f"Draft Answer: {draft_answer}\n"
            "Please critique the draft answer. "
            "Do a careful assessment of whether the answer is correct or not, and why. "
            "Consider multiple ways of verifying the correctness of the answer. "
            "Do point out every flaw and hold the draft answer to a high standard. "
            "Do provide specific recommendations to improve the answer. "
            "Do think step by step. "
            "Do not provide a revised answer."
        )
        
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return response.content
    
    def improve_answer(self, question: str, draft_answer: str, critique: str) -> str:
        """Improve answer based on critique."""
        prompt = (
            f"Question: {question}\n"
            f"Draft Answer: {draft_answer}\n"
            f"Critique: {critique}\n\n"
            "Please improve the draft answer based on the critique. Follow this format:\n"
            "Reasoning Process: <step-by-step reasoning process>\n"
            "Verification: <verification of the facts>\n"
            "Final Answer: <the improved and verified answer>\n"
        )
        
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return response.content
    
    def rate_answer(self, question: str, answer: str) -> float:
        """Rate an answer on a scale of 0-1."""
        prompt = (
            f"Question: {question}\n"
            f"Answer: {answer}\n"
            "As an expert on this topic, please provide a detailed critique of the answer, pointing out every flaw. "
            "Provide only a critique, not a suggested answer. "
            "Then, rate the answer on a scale of 0 to 100. "
            "The response should be in the following format:\n"
            "Critique: <detailed critique>\n"
            "Rating: <rating>"
        )
        
        response = self.llm.invoke([HumanMessage(content=prompt)])
        rating_response = response.content
        
        try:
            match = re.search(r'Rating:\s*(\d+)', rating_response)
            if match:
                rating = int(match.group(1))
                if rating > 95:
                    rating = 95
                rating = float(rating) / 100
            else:
                raise ValueError("Rating not found in the response")
        except Exception as e:
            print(f"Error extracting rating: {e}")
            print(f"Rating response was: {rating_response}")
            rating = 0.0
            
        print(rating_response)
        return rating


class MCTSAgent:
    """Monte Carlo Tree Search Agent for LangChain integration."""
    
    def __init__(self, model: Optional[BaseLanguageModel] = None, **kwargs):
        """
        Initialize MCTS Agent.
        
        Args:
            model: Language model to use with MCTS
            **kwargs: Additional configuration parameters
        """
        self.model = model
        self.config = kwargs
        
    def search(self, query: str, iterations: int = 2, seed_answers: Optional[List[str]] = None) -> str:
        """
        Perform MCTS search for the given query.
        
        Args:
            query: Input query to search
            iterations: Number of MCTS iterations
            seed_answers: Initial seed answers
            
        Returns:
            Best answer found
        """
        if not self.model:
            raise ValueError("Language model must be provided to perform search")
            
        mcts = MCTS(query, self.model, seed_answers, iterations)
        return mcts.search()


def mcts_search(query: str, model: BaseLanguageModel, iterations: int = 2, seed_answers: Optional[List[str]] = None, **kwargs) -> str:
    """
    Convenience function for MCTS search.
    
    Args:
        query: Query to search
        model: Language model to use
        iterations: Number of iterations
        seed_answers: Initial seed answers
        **kwargs: Additional parameters
        
    Returns:
        Best answer found
    """
    agent = MCTSAgent(model=model, **kwargs)
    return agent.search(query, iterations, seed_answers)


def create_mcts_chain(model: BaseLanguageModel, **kwargs) -> MCTSAgent:
    """
    Create an MCTS chain for LangChain integration.
    
    Args:
        model: Language model to use
        **kwargs: Additional configuration
        
    Returns:
        Configured MCTS Agent
    """
    return MCTSAgent(model=model, **kwargs)


@tool
def monte_carlo_search_tool(question: str, model: BaseLanguageModel, iterations: int = 5) -> str:
    """
    Runs the Monte Carlo Tree Search algorithm to find the best answer for a given question.
    
    Args:
        question: The question to find the best answer for
        model: Language model to use for search
        iterations: Number of MCTS iterations
        
    Returns:
        The best answer found by Monte Carlo Tree Search
    """
    try:
        mcts = MCTS(question, model, DEFAULT_SEED_ANSWERS, iterations)
        best_answer = mcts.search()
        return best_answer
    except Exception as e:
        return f"Error during MCTS search: {str(e)}"