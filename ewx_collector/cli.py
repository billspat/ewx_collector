"""Console script for ewx_collector."""
import argparse
import sys


def main():
    """Console script for ewx_collector."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name')
    parser.add_argument('_', nargs='*')

    args = parser.parse_args()

    print("Arguments: " + str(args._))
    
    print(ewx_collector.greet(args.name))
    
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
