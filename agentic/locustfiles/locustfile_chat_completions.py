"""
Locust load test for LlamaStack Chat Completions API (baseline)
"""

from locust import task, between
from locust.contrib.oai import OpenAIUser
import random


class ChatCompletionsUser(OpenAIUser):
    """
    Test user for Chat Completions API (baseline for comparison).
    """
    
    wait_time = between(1, 2)  # Re-enabled to smooth out load pattern
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Override the OpenAI client to use LlamaStack's base URL
        # Append /v1/openai/v1 to reach LlamaStack's OpenAI-compatible endpoints
        self.client.base_url = f"{self.host}/v1/openai/v1"
    
    # Synthetic prompt with ~256 tokens (to match GuideLLM)
    # This is random text from Pride and Prejudice, repeated to reach ~256 tokens
    synthetic_prompt = """It is a truth universally acknowledged that a single man in possession of a good fortune must be in want of a wife However little known the feelings or views of such a man may be on his first entering a neighbourhood this truth is so well fixed in the minds of the surrounding families that he is considered the rightful property of some one or other of their daughters My dear Mr Bennet said his lady to him one day have you heard that Netherfield Park is let at last Mr Bennet replied that he had not But it is returned she for Mrs Long has just been here and she told me all about it Mr Bennet made no answer Do you not want to know who has taken it cried his wife impatiently You want to tell me and I have no objection to hearing it This was invitation enough Why my dear you must know Mrs Long says that Netherfield is taken by a young man of large fortune from the north of England that he came down on Monday in a chaise and four to see the place and was so much delighted with it that he agreed with Mr Morris immediately that he is to take possession before Michaelmas and some of his servants are to be in the house by the end"""
    
    @task
    def test_chat_completions(self):
        """Test Chat Completions API with synthetic data (256 input, 128 output tokens)"""
        
        self.client.chat.completions.create(
            model="vllm-inference/llama-32-3b-instruct",
            messages=[
                {"role": "user", "content": self.synthetic_prompt}
            ],
            max_tokens=128,  # Match GuideLLM: 128 output tokens
            stream=False,
        )

