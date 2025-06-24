import argparse
import json
from .analyzer import analyze_project

def main():
    parser = argparse.ArgumentParser(description="Analyze Python project codebase.")
    parser.add_argument("path", help="Path to the project directory")
    parser.add_argument("-o", "--output", help="Output file (JSON)", default=None)

    args = parser.parse_args()
    report = analyze_project(args.path)

    if args.output:
        with open(args.output, 'w') as f:
            json.dump(report, f, indent=4)
        print(f"Report saved to {args.output}")
    else:
        print(json.dumps(report, indent=4))

if __name__ == "__main__":
    main()