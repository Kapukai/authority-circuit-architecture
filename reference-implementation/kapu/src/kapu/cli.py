import argparse,json
from pathlib import Path
from .engine import evaluate
def main():
    p=argparse.ArgumentParser(prog="kapu-cell"); p.add_argument("input")
    a=p.parse_args(); data=json.loads(Path(a.input).read_text())
    print(json.dumps(evaluate(data),indent=2,sort_keys=True))
if __name__=="__main__": main()
