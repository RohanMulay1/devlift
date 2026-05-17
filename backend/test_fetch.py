from dotenv import load_dotenv
load_dotenv()
from github_fetcher import fetch_repo_context
import time

print("Fetching express repo...")
t = time.time()
ctx = fetch_repo_context("https://github.com/expressjs/express")
elapsed = time.time() - t
print(f"Done in {elapsed:.1f}s")
print(f"Files: {len(ctx['files'])}")
print(f"Tree lines: {len(ctx['file_tree'].splitlines())}")
print(f"Stars: {ctx['stars']}")
print("First 5 files:", [f['path'] for f in ctx['files'][:5]])
