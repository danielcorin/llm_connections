# LLM connections

Python code to evaluate a language model by having it try and solve a [Connections](https://www.nytimes.com/games/connections)
word puzzle.

## Setup

Install dependencies

```sh
python -m venv env
. env/bin/activate
pip install -r requirements.txt
llm install -U llm
llm install llm-claude-3
# ... install any other models you want to try
```

Add secrets.
This project uses [`direnv`](https://direnv.net/#basic-installation).

```sh
cp .envrc.template .envrc
# add OPENAI_API_KEY
direnv allow
```

The remainder of the keys can be set/managed with

```sh
llm keys set <provider>
```

For example

```sh
llm keys set anthropic
```

I'm not exactly sure why this approach doesn't work for OpenAI models for me, but setting the environment variable seems to be a workaround.

## Run

```sh
python connections.py <model_name>
```

For example

```sh
python connections.py claude-3-opus
```

assuming you have installed this model via `llm install llm-claude-3`.
