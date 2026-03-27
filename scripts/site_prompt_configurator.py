#!/usr/bin/env python3
"""Standalone utility to generate context-rich LLM build prompts for missing routes."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate route build prompt with site context.")
    parser.add_argument("--endpoint", required=True, help="Missing or target route, e.g. /reports/new")
    parser.add_argument("--goal", default="", help="Desired outcome for the endpoint")
    parser.add_argument("--context-page", default="_work_efforts/reports/report_hub_latest.html", help="Context HTML page")
    parser.add_argument("--wireframe", default="", help="Quick wireframe notes")
    parser.add_argument("--screenshot", default="", help="Optional screenshot path/name")
    parser.add_argument("--output-dir", default="_work_efforts/reports", help="Where prompt artifact is written")
    return parser.parse_args()


def _extract_title_and_h1(html_text: str) -> tuple[str, str]:
    title = "Unknown title"
    h1 = "Unknown header"
    if "<title>" in html_text and "</title>" in html_text:
        title = html_text.split("<title>", 1)[1].split("</title>", 1)[0].strip() or title
    if "<h1>" in html_text and "</h1>" in html_text:
        h1 = html_text.split("<h1>", 1)[1].split("</h1>", 1)[0].strip() or h1
    return title, h1


def main() -> int:
    args = parse_args()
    root = Path.cwd()
    context_page = (root / args.context_page).resolve()
    output_dir = (root / args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    html_text = ""
    if context_page.exists():
        html_text = context_page.read_text(encoding="utf-8", errors="ignore")

    title, h1 = _extract_title_and_h1(html_text)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    goal = args.goal.strip() or "Create a useful endpoint with clear top-level summary and drill-down evidence."
    wireframe = args.wireframe.strip() or "Top: golden nugget, Mid: evidence cards, Bottom: explorer/actions."
    screenshot = args.screenshot.strip() or "(none)"

    prompt = "\n".join(
        [
            "You are continuing WAFT site development.",
            "",
            f"Target endpoint: {args.endpoint}",
            "Current behavior: endpoint may be missing or incomplete (treat as 404-to-feature request).",
            f"Desired outcome: {goal}",
            f"Wireframe notes: {wireframe}",
            f"Screenshot reference: {screenshot}",
            "",
            "Site context:",
            f"- Context page: {context_page}",
            f"- Title: {title}",
            f"- Header: {h1}",
            "",
            "Implementation requirements:",
            "1) Add an abstract top summary that explains current state plainly.",
            "2) Use reverse-cone navigation: summary -> evidence -> deep rabbit holes.",
            "3) Replace dead-end 404 behavior with prompt configurator UX for this route.",
            "4) Keep visual language consistent with existing WAFT cards/tokens.",
            "5) Return code-level implementation and updated docs.",
        ]
    )

    prompt_path = output_dir / f"route_prompt_{stamp}.md"
    wireframe_path = output_dir / f"route_wireframe_{stamp}.txt"
    prompt_path.write_text(prompt + "\n", encoding="utf-8")
    wireframe_path.write_text(
        "\n".join(
            [
                f"Endpoint: {args.endpoint}",
                "",
                "+------------------------------------------------------+",
                "| Golden Nugget (plain-language abstract)              |",
                "+------------------------------------------------------+",
                "| Evidence Cards | Trend Strip | Health                |",
                "+------------------------------------------------------+",
                "| Explorer / Rabbit Holes                              |",
                "+------------------------------------------------------+",
                "| Prompt Configurator (404 fallback)                   |",
                "+------------------------------------------------------+",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    print("=== WAFT Route Prompt Configurator ===")
    print(f"Prompt: {prompt_path}")
    print(f"Wireframe: {wireframe_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
