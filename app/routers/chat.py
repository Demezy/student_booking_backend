import os
import openai

# openai.api_key = os.getenv("OPENAI_API_KEY")

# @router.post('/{id}')
# def complete(id: str, body: dict = Body(...), token: str = Depends(get_token_from_header)):
#   response = openai.Completion.create(
#     model="text-davinci-003",
#     prompt="",
#     temperature=0.9,
#     max_tokens=4096,
#     top_p=1,
#     frequency_penalty=0,
#     presence_penalty=0.6,
#     stop=["Human:", "AI:"]
#   )
