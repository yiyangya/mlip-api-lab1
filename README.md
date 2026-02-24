# Lab 1: Calling, Building, and Securing APIs
In homework I1 you will use third-party LLM APIs, and in the group project you will develop your own APIs. In this lab you will experiment with both: connecting to an LLM of your choice, and providing your own API endpoint. 

To receive credit for this lab, show your work to the TA during recitation.

## Deliverables
- [ ] Use an API key to invoke an LLM API and generate a schema-enforced JSON travel itinerary.
- [ ] Run the API endpoint with the LLM call implemented and demonstrate that it works using an example invocation.
- [ ] Commit your code without committing your credentials. Explain to the TA why hard-coding credentials is a bad idea, and explain any remedial steps you might take should credentials accidentally be leaked. 

## Getting started
Clone the starter code from this Git repository

The code implements a Flask web application that exposes an API endpoint for generating a structured travel itinerary for a given destination. The API accepts a destination string and returns a JSON response containing high-level travel information. 

To generate this response, you will need to call an LLM. We suggest using Meta's [Llama](https://www.llama.com/), hosted by [Groq](https://groq.com/), using [LiteLLM](https://docs.litellm.ai/docs/) to abstract client-specific details.

Install the dependencies listed in requirements.txt using pip or a similar tool. The Flask server can be started with:
```
python3 app.py
```

Once running, the API will be available at:
```
http://localhost:8000/api/v1/itinerary
```

## Generate an LLM API Key
For this we suggest using an API key from Groq but you are certainly free to use other API keys, such as those from OpenAI, Anthropic, etc. Instructions for using those keys can be found [here](https://docs.litellm.ai/docs/providers/openai). The instructions below are shown for getting an API key from Groq.

1. Sign into your Groq account and [navigate to the API keys console](https://console.groq.com/keys).
2. Generate a new API key.
3. **Do not hard-code this key in the source code.** Instead, set it as an environment variable named `GROQ_API_KEY` (see the setup section below) and then run and test the app.


## Secure your Credentials
The starter code hardcodes credentials in the code. This is a bad practice. 

Research and discuss best practices, such as never hard-code credentials, never commit credentials to Git, rotate secrets regularly, encrypt your secrets at rest/in-transit if possible, practice least-access privilege on machines where your credentials are stored as environment variables or within local files.

Rewrite the code to load credentials from a file or an environment variable and commit the code without the credentials.

## Implement the call to the LLM
Using LiteLLM, implement the logic in analyze.py to call a an LLM. We suggest `groq/llama-3.3-70b-versatile` but you are free to use others. 

Your implementation should 
- Make at least one LLM call using LiteLLM
- Request a [structured JSON response](https://docs.litellm.ai/docs/completion/json_mode)
- Enforce (or validate) the structure of the response against a predefined schema. The schema should include the following fields:
  - `destination`
  - `price_range`
  - `ideal_visit_times`
  - `top_attractions`

The response from your implemented API call should look something like what is shown below:

```JSON
{
    "destination": "...",
    "ideal_visit_times": [
        ...
    ],
    "price_range": ...,
    "top_attractions": [
       ...
    ]
}
```

## Calling your own API
The Flask server serves a simple documentation page at:
```
http://localhost:8000/
```
It also exposes the API endpoint:
```
GET http://localhost:8000/api/v1/itinerary
```
The endpoint expects a required query parameter:
 - `destination`: the destination to generate an itinerary for

You can use tools like [curl](https://curl.se/) or [Postman](https://www.postman.com/) to ensure your API endpoint is functioning appropriately. 

The file [mlip-api-lab-collection.json](./mlip-api-lab-collection.json) has a sample request to test calls to your API with Postman. Consider using [Postman test scripts](https://learning.postman.com/docs/tests-and-scripts/write-scripts/test-scripts/) to test the response of your API endpoints (status codes, response structure, etc.,).


## Additional resources 
- [Redhat article on API](https://www.redhat.com/en/topics/api/what-are-application-programming-interfaces)
- [API Design Best Practices](https://blog.stoplight.io/crud-api-design?_ga=2.223919515.1813989671.1674077556-1488117179.1674077556)
- [API Endpoint Best Practices](https://www.telerik.com/blogs/7-tips-building-good-web-api)
- [LiteLLM documentation](https://docs.litellm.ai/)


## Local setup and dependencies

- **Requirements**:  
  - **Python**: 3.9+  
  - **Pip**: installed and on your `PATH`

- **Install dependencies**:

```bash
# (Optional but recommended) create and activate a virtualenv
python -m venv .venv
# PowerShell:
.\.venv\Scripts\Activate.ps1
# CMD:
.\.venv\Scripts\activate.bat

# Install required packages
pip install -r requirements.txt
```

The main Python dependencies (defined in `requirements.txt`) are:

- `Flask` – web framework for the API server  
- `litellm` – unified client for calling LLM APIs (e.g., Groq Llama models)


## Configure your LLM API key

This project expects your LLM API key to be provided via an **environment variable**, not hard-coded in the code. By default, `analyze.py` looks for an environment variable named `GROQ_API_KEY`.

- **Windows PowerShell (current session only)**:

```powershell
$env:GROQ_API_KEY = "YOUR_REAL_GROQ_API_KEY_HERE"
```

- **macOS / Linux (bash/zsh)**:

```bash
export GROQ_API_KEY="YOUR_REAL_GROQ_API_KEY_HERE"
```

> **Important**: Do **not** put your real API key into the Python files or commit it to git. The key should only live in your environment.


## Start the app

From the project root:

```bash
python app.py
```

By default, the Flask server will start on port `8000`.

- **Docs page**:  
  - `http://localhost:8000/`
- **API endpoint**:  
  - `GET http://localhost:8000/api/v1/itinerary?destination=Paris`


## Testing the API

- **Quick test with browser or curl**:

```bash
curl "http://localhost:8000/api/v1/itinerary?destination=Paris"
```

You should receive a JSON response containing:

- `destination`  
- `price_range`  
- `ideal_visit_times` (array)  
- `top_attractions` (array)

- **Test with Postman**:
  - Import `mlip-api-lab-collection.json` into Postman.
  - Update the request (if needed) to call `http://localhost:8000/api/v1/itinerary`.
  - Send a request with a `destination` query parameter and check that:
    - Status code is `200`.
    - Response body has the required JSON fields and sensible values.


## Why environment variables instead of hard-coding API keys?

- **No secrets in source control**: If you put an API key directly in `analyze.py`, it will be stored in git history and is easy to accidentally leak when you share or push the repo. Using an environment variable means the secret never appears in the code or commit history.
- **Easy rotation**: When you need to rotate a key, you can change the environment value without touching the code, so you do not need new commits just to update credentials.
- **Separation of config and code**: The same codebase can be safely used in different environments (your laptop, a server, CI) just by setting different environment variables, with no code changes.
- **Remediation if a key leaks**: If a key is ever exposed, the correct response is to revoke/rotate it in the provider’s console (e.g., Groq dashboard), remove it from any logs or files where it appeared, and then set a new value in the environment variable. You never need to keep the leaked key in the repository.