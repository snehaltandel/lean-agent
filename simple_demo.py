#!/usr/bin/env python3
"""Simple example usage of the WasteDetector tool without LangGraph."""

from app.tools.waste_detector import WasteDetector


def main():
    """Run a simple example with the WasteDetector tool."""
    print("Lean Concepts Agent - WasteDetector Demo")
    print("=" * 50)
    
    # Create the tool
    detector = WasteDetector()
    
    # Example process descriptions
    examples = [
        "Our team has a manual approval process where team members wait for managers to review documents, causing delays and requiring people to walk back and forth between desks.",
        "The automated pipeline runs smoothly with no bottlenecks.",
        "Workers have to manually fill out the same information on three different forms, and then wait for each form to be processed separately."
    ]
    
    for i, process_description in enumerate(examples, 1):
        print(f"\nExample {i}:")
        print(f"Process: {process_description}")
        print("-" * 60)
        
        # Run the waste detector
        result = detector.run({"process_description": process_description})
        
        # Display results
        print(f"Summary: {result['summary']}")
        if result['wastes']:
            print("Identified Wastes:")
            for waste in result['wastes']:
                print(f"  - {waste['category'].title()}: {waste['supporting_evidence']}")
                print(f"    Action: {waste['recommended_action']}")
        print()


if __name__ == "__main__":
    main()
