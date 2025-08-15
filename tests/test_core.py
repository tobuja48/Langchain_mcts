"""Tests for core MCTS functionality."""

import pytest
import warnings
from langchain_mcts import MCTSAgent, mcts_search, create_mcts_chain
from langchain_mcts.core import MCTSNode


class TestMCTSAgent:
    """Test cases for MCTSAgent class."""
    
    def test_agent_initialization(self):
        """Test that MCTSAgent can be initialized."""
        agent = MCTSAgent()
        assert agent is not None
        assert agent.model is None
        assert agent.config == {}
    
    def test_agent_initialization_with_config(self):
        """Test MCTSAgent initialization with configuration."""
        config = {"temperature": 0.5, "max_depth": 10}
        agent = MCTSAgent(model="test_model", **config)
        assert agent.model == "test_model"
        assert agent.config == config
    
    def test_search_returns_development_message(self):
        """Test that search method returns development message."""
        agent = MCTSAgent()
        result = agent.search("test query")
        assert "está en desarrollo" in result
        assert "🚧" in result
    
    def test_expand_node_returns_development_message(self):
        """Test that expand_node returns development message."""
        agent = MCTSAgent()
        result = agent.expand_node({"state": "test"})
        assert isinstance(result, list)
        assert len(result) == 1
        assert "está en desarrollo" in result[0]["message"]
    
    def test_simulate_warns_development(self):
        """Test that simulate method warns about development status."""
        agent = MCTSAgent()
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = agent.simulate({"state": "test"})
            assert len(w) == 1
            assert "está en desarrollo" in str(w[0].message)
            assert result == 0.5
    
    def test_backpropagate_prints_development(self, capsys):
        """Test that backpropagate prints development message."""
        agent = MCTSAgent()
        agent.backpropagate([{"node": 1}, {"node": 2}], 0.8)
        captured = capsys.readouterr()
        assert "está en desarrollo" in captured.out


class TestMCTSFunctions:
    """Test cases for module-level functions."""
    
    def test_mcts_search_returns_development_message(self):
        """Test that mcts_search function returns development message."""
        result = mcts_search("test query")
        assert "está en desarrollo" in result
        assert "test query" in result
        assert "🚧" in result
    
    def test_create_mcts_chain_returns_agent(self, capsys):
        """Test that create_mcts_chain returns MCTSAgent instance."""
        result = create_mcts_chain(model="test_model", config="test")
        assert isinstance(result, MCTSAgent)
        assert result.model == "test_model"
        assert result.config == {"config": "test"}
        
        captured = capsys.readouterr()
        assert "está en desarrollo" in captured.out


class TestMCTSNode:
    """Test cases for MCTSNode class."""
    
    def test_node_initialization(self):
        """Test MCTSNode initialization."""
        node = MCTSNode(state="test_state")
        assert node.state == "test_state"
        assert node.parent is None
        assert node.children == []
        assert node.visits == 0
        assert node.value == 0.0
    
    def test_node_with_parent(self):
        """Test MCTSNode initialization with parent."""
        parent = MCTSNode(state="parent")
        child = MCTSNode(state="child", parent=parent)
        assert child.parent == parent
    
    def test_is_leaf_true(self):
        """Test is_leaf returns True for node without children."""
        node = MCTSNode()
        assert node.is_leaf() is True
    
    def test_is_leaf_false(self):
        """Test is_leaf returns False for node with children."""
        node = MCTSNode()
        node.children = [MCTSNode()]
        assert node.is_leaf() is False
    
    def test_add_child(self):
        """Test adding child node."""
        parent = MCTSNode(state="parent")
        child = parent.add_child("child_state")
        assert len(parent.children) == 1
        assert child.state == "child_state"
        assert child.parent == parent
    
    def test_update_prints_development(self, capsys):
        """Test that update method prints development message."""
        node = MCTSNode()
        node.update(0.7)
        captured = capsys.readouterr()
        assert "está en desarrollo" in captured.out
        assert "0.7" in captured.out
        assert node.visits == 1


class TestIntegration:
    """Integration tests."""
    
    def test_import_all_functions(self):
        """Test that all main functions can be imported."""
        from langchain_mcts import MCTSAgent, mcts_search, create_mcts_chain
        assert MCTSAgent is not None
        assert mcts_search is not None
        assert create_mcts_chain is not None
    
    def test_end_to_end_workflow(self, capsys):
        """Test a complete workflow using the library."""
        # Create agent
        agent = MCTSAgent(model="test")
        
        # Perform search
        search_result = agent.search("test query", iterations=50)
        assert "está en desarrollo" in search_result
        
        # Use convenience function
        convenience_result = mcts_search("another query")
        assert "está en desarrollo" in convenience_result
        
        # Create chain
        chain = create_mcts_chain()
        assert isinstance(chain, MCTSAgent)
        
        captured = capsys.readouterr()
        assert "está en desarrollo" in captured.out