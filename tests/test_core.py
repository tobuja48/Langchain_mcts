"""Tests for core MCTS functionality."""

import pytest
from unittest.mock import Mock, MagicMock
from langchain_mcts import MCTSAgent, mcts_search, create_mcts_chain, MCTS, MCTSNode, monte_carlo_search_tool
from langchain_core.language_models.base import BaseLanguageModel
from langchain_core.messages import AIMessage


class TestMCTSNode:
    """Test cases for MCTSNode class."""
    
    def test_node_initialization(self):
        """Test MCTSNode initialization."""
        node = MCTSNode("What is 2+2?", "4")
        assert node.question == "What is 2+2?"
        assert node.answer == "4"
        assert node.parent is None
        assert node.children == []
        assert node.visits == 0
        assert node.value == 0.0
    
    def test_node_with_parent(self):
        """Test MCTSNode initialization with parent."""
        parent = MCTSNode("What is 2+2?", "I don't know")
        child = MCTSNode("What is 2+2?", "4", parent=parent)
        assert child.parent == parent
    
    def test_is_fully_expanded(self):
        """Test is_fully_expanded method."""
        node = MCTSNode("test", "answer")
        assert not node.is_fully_expanded()
        
        for i in range(3):
            child = MCTSNode("test", f"child{i}", parent=node)
            node.add_child(child)
            
        assert node.is_fully_expanded()
    
    def test_add_child(self):
        """Test adding child node."""
        parent = MCTSNode("test", "parent_answer")
        child = MCTSNode("test", "child_answer", parent=parent)
        parent.add_child(child)
        
        assert len(parent.children) == 1
        assert parent.children[0] == child
        assert child.parent == parent


class TestMCTSAgent:
    """Test cases for MCTSAgent class."""
    
    def test_agent_initialization(self):
        """Test that MCTSAgent can be initialized."""
        agent = MCTSAgent()
        assert agent is not None
        assert agent.model is None
        assert agent.config == {}
    
    def test_agent_initialization_with_model(self):
        """Test MCTSAgent initialization with model."""
        mock_model = Mock(spec=BaseLanguageModel)
        agent = MCTSAgent(model=mock_model)
        assert agent.model == mock_model
    
    def test_search_requires_model(self):
        """Test that search raises error without model."""
        agent = MCTSAgent()
        with pytest.raises(ValueError, match="Language model must be provided"):
            agent.search("test query")


class TestMCTS:
    """Test cases for MCTS class."""
    
    def test_mcts_initialization(self):
        """Test MCTS initialization."""
        mock_llm = Mock(spec=BaseLanguageModel)
        mcts = MCTS("What is 2+2?", mock_llm)
        
        assert mcts.question == "What is 2+2?"
        assert mcts.llm == mock_llm
        assert mcts.iterations == 2
        assert mcts.root.question == "What is 2+2?"
    
    def test_mcts_with_custom_seed_answers(self):
        """Test MCTS with custom seed answers."""
        mock_llm = Mock(spec=BaseLanguageModel)
        custom_seeds = ["Custom seed 1", "Custom seed 2"]
        mcts = MCTS("test question", mock_llm, seed_answers=custom_seeds)
        
        assert mcts.seed_answers == custom_seeds


class TestMCTSFunctions:
    """Test cases for module-level functions."""
    
    def test_mcts_search_with_mock_model(self):
        """Test mcts_search function with mock model."""
        mock_llm = Mock(spec=BaseLanguageModel)
        mock_llm.invoke.return_value = AIMessage(content="Test response with Rating: 85")
        
        result = mcts_search("test query", mock_llm, iterations=1)
        assert isinstance(result, str)
        mock_llm.invoke.assert_called()
    
    def test_create_mcts_chain_returns_agent(self):
        """Test that create_mcts_chain returns MCTSAgent instance."""
        mock_model = Mock(spec=BaseLanguageModel)
        result = create_mcts_chain(model=mock_model, config="test")
        
        assert isinstance(result, MCTSAgent)
        assert result.model == mock_model
        assert result.config == {"config": "test"}


class TestMonteCarloSearchTool:
    """Test cases for monte_carlo_search_tool."""
    
    def test_tool_with_mock_model(self):
        """Test the tool function with mock model."""
        mock_llm = Mock(spec=BaseLanguageModel)
        mock_llm.invoke.return_value = AIMessage(content="Improved answer with Rating: 90")
        
        result = monte_carlo_search_tool.run(
            question="What is the capital of France?",
            model=mock_llm,
            iterations=1
        )
        
        assert isinstance(result, str)
        mock_llm.invoke.assert_called()


class TestIntegration:
    """Integration tests."""
    
    def test_import_all_functions(self):
        """Test that all main functions can be imported."""
        from langchain_mcts import MCTSAgent, mcts_search, create_mcts_chain, MCTS, MCTSNode
        assert MCTSAgent is not None
        assert mcts_search is not None
        assert create_mcts_chain is not None
        assert MCTS is not None
        assert MCTSNode is not None
    
    def test_end_to_end_workflow_with_mock(self):
        """Test a complete workflow using the library with mock."""
        mock_llm = Mock(spec=BaseLanguageModel)
        mock_llm.invoke.return_value = AIMessage(content="Mock response with Rating: 75")
        
        agent = MCTSAgent(model=mock_llm)
        result = agent.search("test query", iterations=1)
        
        assert isinstance(result, str)
        mock_llm.invoke.assert_called()