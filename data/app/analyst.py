import sys
import subprocess

def process():
    number = int(sys.argv[1])
    squared = number * number
    
    # Python calls the C++ Engine
    result = subprocess.check_output(['engine.exe', str(squared)])
    print(result.decode().strip())

if __name__ == "__main__":
    process()