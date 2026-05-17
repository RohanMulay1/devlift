from dotenv import load_dotenv
load_dotenv()
import os, time
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference

print("Testing watsonx connection...")
print("URL:", os.getenv("WATSONX_URL"))
print("Project:", os.getenv("WATSONX_PROJECT_ID")[:8], "...")

credentials = Credentials(
    url=os.getenv("WATSONX_URL"),
    api_key=os.getenv("WATSONX_API_KEY"),
)

model = ModelInference(
    model_id="meta-llama/llama-3-3-70b-instruct",
    credentials=credentials,
    project_id=os.getenv("WATSONX_PROJECT_ID"),
    params={"max_new_tokens": 50, "temperature": 0.1},
)

print("Sending test prompt...")
t = time.time()
result = model.generate_text(prompt="Say hello in one word.")
print(f"Response in {time.time()-t:.1f}s: {result!r}")
