# scripts/main.py

import argparse
from content.generate_website_content import main as generate_content

def main():
    parser = argparse.ArgumentParser(description="Website maintenance scripts")
    parser.add_argument('task', choices=['generate_content'], help='Maintenance task to run')
    args = parser.parse_args()

    if args.task == 'generate_content':
        generate_content()

if __name__ == "__main__":
    main()
