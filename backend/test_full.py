from dotenv import load_dotenv
load_dotenv()
import time

# Step 1: GitHub fetch
print("Step 1: GitHub fetch...")
t = time.time()
from github_fetcher import fetch_repo_context
ctx = fetch_repo_context("https://github.com/expressjs/express")
print(f"  Done in {time.time()-t:.1f}s — {len(ctx['files'])} files")

# Step 2: Build prompt
print("Step 2: Building prompt...")
t = time.time()
from prompt_builder import build_onboarding_prompt
prompt = build_onboarding_prompt(ctx)
print(f"  Done in {time.time()-t:.1f}s — prompt length: {len(prompt)} chars")

# Step 3: Watsonx call
print("Step 3: Calling watsonx (llama-3-3-70b)...")
t = time.time()
from bob_client import generate_onboarding_kit
kit = generate_onboarding_kit(prompt)
print(f"  Done in {time.time()-t:.1f}s")
print("  Kit keys:", list(kit.keys()))
print("  Architecture preview:", kit.get("architecture_overview","")[:200])
