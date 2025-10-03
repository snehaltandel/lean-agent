#!/usr/bin/env python3
"""Main entry point for the Lean Concepts Agent."""

import argparse
import sys
from pathlib import Path

from app.tools.waste_detector import WasteDetector


def interactive_mode():
    """Run the agent in interactive mode."""
    print("🔧 Lean Concepts Agent - Interactive Mode")
    print("=" * 50)
    print("This tool helps identify wastes in your processes using TIMWOODS categories.")
    print("Enter 'quit' or 'exit' to stop.\n")
    
    detector = WasteDetector()
    
    while True:
        try:
            process_description = input("📝 Describe your process: ").strip()
            
            if process_description.lower() in ['quit', 'exit', '']:
                print("👋 Thanks for using the Lean Concepts Agent!")
                break
                
            print("\n🔍 Analyzing process...")
            result = detector.run({"process_description": process_description})
            
            print(f"\n📊 Analysis Results:")
            print(f"Summary: {result['summary']}\n")
            
            if result['wastes']:
                print("🚨 Identified Wastes:")
                for i, waste in enumerate(result['wastes'], 1):
                    print(f"  {i}. {waste['category'].title()}")
                    print(f"     Evidence: {waste['supporting_evidence']}")
                    print(f"     Recommendation: {waste['recommended_action']}")
                    print()
            else:
                print("✅ No obvious wastes detected!")
                
            print("-" * 60)
            
        except KeyboardInterrupt:
            print("\n👋 Thanks for using the Lean Concepts Agent!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


def analyze_file(file_path: Path):
    """Analyze a process description from a file."""
    if not file_path.exists():
        print(f"❌ Error: File {file_path} not found.")
        return
        
    try:
        process_description = file_path.read_text().strip()
        detector = WasteDetector()
        
        print(f"🔧 Lean Concepts Agent - File Analysis")
        print(f"📁 Analyzing: {file_path}")
        print("=" * 60)
        
        result = detector.run({"process_description": process_description})
        
        print(f"📊 Analysis Results:")
        print(f"Summary: {result['summary']}\n")
        
        if result['wastes']:
            print("🚨 Identified Wastes:")
            for i, waste in enumerate(result['wastes'], 1):
                print(f"  {i}. {waste['category'].title()}")
                print(f"     Evidence: {waste['supporting_evidence']}")
                print(f"     Recommendation: {waste['recommended_action']}")
                print()
        else:
            print("✅ No obvious wastes detected!")
            
    except Exception as e:
        print(f"❌ Error processing file: {e}")


def main():
    """Main entry point with CLI argument parsing."""
    parser = argparse.ArgumentParser(
        description="Lean Concepts Agent - Identify waste in your processes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                     # Interactive mode
  %(prog)s --file process.txt  # Analyze file
  %(prog)s --demo             # Run demo examples
        """
    )
    
    parser.add_argument(
        "--file", "-f",
        type=Path,
        help="Analyze process description from a text file"
    )
    
    parser.add_argument(
        "--demo", "-d",
        action="store_true",
        help="Run demo examples"
    )
    
    args = parser.parse_args()
    
    if args.file:
        analyze_file(args.file)
    elif args.demo:
        # Import and run the demo
        from simple_demo import main as demo_main
        demo_main()
    else:
        interactive_mode()


if __name__ == "__main__":
    main()
