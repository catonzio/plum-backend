import json
import requests as req
from uuid import uuid4

url = "http://0.0.0.0:8000/"

messages: list[dict] = []


def separator() -> None:
    print("# " + "-" * 50 + "#")


def uri(path: str, params: dict | None = None) -> str:
    if not path.startswith("/"):
        path = "/" + path

    if params:
        query_string = "&".join(f"{key}={value}" for key, value in params.items())
        return f"{url}{path}?{query_string}"
    return f"{url}{path}"


def main():
    thread_id = str(uuid4())
    user_id = str(uuid4())
    query_params = {
        "args": None,
        "kwargs": None,
    }
    body = {
        "thread_id": thread_id,
        "user_id": user_id,
    }

    try:
        while True:
            message = input("You: > ")
            if message.lower() == "exit":
                break
            messages.append({"role": "user", "content": message})
            body["message"] = message
            response = req.post(uri("/agent/invoke", params=query_params), json=body)
            if response.status_code == 200:
                answer = response.json()
                messages.append(answer)
                separator()
                print(f"Assistant:\n\n{answer['content']}")
                separator()
            else:
                print(f"Error: {response.status_code} - {response.text}")
    finally:
        with open("chat_history.json", "w") as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
