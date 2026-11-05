"""Run a batch of evaluation questions through the agent and print answer, SQL, timing.

python tests/run_eval.py tests/questions.txt [-j 4]
"""
import argparse
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from dotenv import load_dotenv  # noqa: E402

load_dotenv(ROOT / ".env", override=True)
sys.stdout.reconfigure(encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("-j", type=int, default=4)
    ap.add_argument("--out", default=str(ROOT / "logs" / "eval.jsonl"))
    a = ap.parse_args()
    import agent as ag

    A = ag.Agent()
    qs = [
        l.strip()
        for l in Path(a.file).read_text(encoding="utf-8").splitlines()
        if l.strip() and not l.startswith("#")
    ]

    def run(q):
        try:
            return q, A.ask(q)
        except Exception as e:  # noqa: BLE001
            return q, {"answer": f"ERROR {e}", "sql": [], "elapsed": -1, "verified": None}

    t0 = time.time()
    Path(a.out).parent.mkdir(exist_ok=True)
    with ThreadPoolExecutor(a.j) as ex, open(a.out, "w", encoding="utf-8") as f:
        for i, (q, r) in enumerate(ex.map(run, qs), 1):
            print("=" * 100, flush=True)
            print(f"[{i}] Q: {q}", flush=True)
            print(f"--- {r['elapsed']}s verified={r['verified']} model={r.get('model')} lang={r.get('lang')}", flush=True)
            for s in r["sql"]:
                print("SQL:", " ".join(s.split())[:600], flush=True)
            print("A:", r["answer"], flush=True)
            f.write(
                json.dumps(
                    {
                        "q": q,
                        "answer": r["answer"],
                        "sql": r["sql"],
                        "elapsed": r["elapsed"],
                        "verified": r["verified"],
                        "model": r.get("model"),
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )
            f.flush()
    print(f"\nTOTAL {time.time() - t0:.1f}s", flush=True)


if __name__ == "__main__":
    main()
