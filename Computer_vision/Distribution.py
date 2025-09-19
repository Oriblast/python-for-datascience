import sys
from distribution import distribution

if len(sys.argv) >= 2:
    distribution(sys.argv[1])
