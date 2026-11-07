"""Optional live smoke test. Requires DEEPSEEK_API_KEY in samples/.env."""

from __future__ import annotations

from dotenv import load_dotenv

from .common import get_model, has_api_key


def main() -> None:
    load_dotenv()
    if not has_api_key():
        raise SystemExit("DEEPSEEK_API_KEY is not set; copy .env.example to .env first.")

    model = get_model()
    response = model.invoke("用一句话解释 LangGraph 的 checkpoint。")
    print(response.content)


if __name__ == "__main__":
    main()
