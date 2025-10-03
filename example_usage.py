#!/usr/bin/env python3
"""Example usage of the Lean Concepts Agent."""

from app.agent.graph import build_graph
from app.agent.state import AgentState


def main():
    """Run a simple example with the Lean Agent."""
    # Build the LangGraph state machine
    graph = build_graph()
    compiled_graph = graph.compile()
    
    # Create initial state with a user goal
    initial_state = AgentState(
        user_goal="Our team has a manual approval process where team members wait for managers to review documents, causing delays and requiring people to walk back and forth between desks."
    )
    
    # Execute the graph
    print("Running Lean Concepts Agent...")
    print(f"User Goal: {initial_state.user_goal}")
    print("-" * 60)
    
    # Run the agent
    result = compiled_graph.invoke(initial_state)
    
    # Display results
    print("Agent Analysis:")
    print(f"Final Response: {result.final_response}")
    print("\nConversation History:")
    for entry in result.conversation_history:
        print(f"Tool: {entry['tool']}")
        print(f"Result: {entry['result']}")
        print("-" * 40)


if __name__ == "__main__":
    main()
