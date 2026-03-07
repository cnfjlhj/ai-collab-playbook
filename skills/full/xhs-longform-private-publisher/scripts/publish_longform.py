#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Callable

from playwright.sync_api import Dialog, Locator, Page, TimeoutError as PlaywrightTimeoutError, sync_playwright


ARTICLE_ENTRY_URL = "https://creator.xiaohongshu.com/publish/publish?from=menu&target=article"
MANAGER_URL = "https://creator.xiaohongshu.com/new/note-manager"
VISIBILITY_TEXT = {
    "private": "仅自己可见",
    "public": "公开可见",
    "mutual": "仅互关好友可见",
}


class PayloadValidationError(ValueError):
    pass


class PublishAutomationError(RuntimeError):
    pass


@dataclass(slots=True)
class LongformPayload:
    title: str
    parts: list[str]
    images: list[Path]
    desc: str = ""


@dataclass(slots=True)
class PublishArtifacts:
    screenshot_dir: Path
    editor_screenshot: Path | None = None
    manager_screenshot: Path | None = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Publish a Xiaohongshu longform article from a prepared JSON payload."
    )
    parser.add_argument("--payload", required=True, type=Path, help="Path to the JSON payload.")
    parser.add_argument(
        "--user-data-dir",
        type=Path,
        default=Path.home() / ".codex/skills/xhs-longform-private-publisher/.playwright-xhs-profile",
        help="Persistent browser profile directory for Xiaohongshu login reuse.",
    )
    parser.add_argument(
        "--browser-channel",
        default="chrome",
        choices=["chrome", "msedge", "chromium"],
        help="Browser channel to launch with Playwright.",
    )
    parser.add_argument(
        "--visibility",
        choices=sorted(VISIBILITY_TEXT),
        default="private",
        help="Final note visibility. Default is private.",
    )
    parser.add_argument("--publish", action="store_true", help="Actually click the final publish button.")
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Validate payload and print the execution plan without launching the browser.",
    )
    parser.add_argument("--title", help="Optional title override.")
    parser.add_argument("--desc", help="Optional short description override for the post-layout page.")
    parser.add_argument("--desc-file", type=Path, help="Read the short description override from a file.")
    parser.add_argument("--headless", action="store_true", help="Run browser in headless mode.")
    parser.add_argument("--slow-mo", type=int, default=0, help="Playwright slow-mo delay in milliseconds.")
    parser.add_argument("--timeout-ms", type=int, default=20_000, help="Default Playwright timeout in milliseconds.")
    parser.add_argument(
        "--layout-timeout-ms",
        type=int,
        default=180_000,
        help="Timeout for one-click layout generation in milliseconds.",
    )
    parser.add_argument(
        "--manager-timeout-ms",
        type=int,
        default=60_000,
        help="Timeout for manager-page verification in milliseconds.",
    )
    parser.add_argument(
        "--screenshot-dir",
        type=Path,
        help="Directory for screenshots and summary output. Defaults to a timestamped directory in the current working directory.",
    )
    parser.add_argument(
        "--pause-on-finish",
        action="store_true",
        help="Pause for Enter before closing the browser, useful for manual inspection in dry runs.",
    )
    return parser.parse_args()


def build_title_prefix(title: str, limit: int = 14) -> str:
    normalized = re.sub(r"\s+", " ", title).strip()
    return normalized[:limit]


def card_matches(card_text: str, title_prefix: str, visibility_text: str) -> bool:
    return title_prefix in card_text and visibility_text in card_text


def load_desc_override(args: argparse.Namespace, payload_desc: str) -> str:
    if args.desc and args.desc_file:
        raise PayloadValidationError("不能同时使用 --desc 和 --desc-file。")
    if args.desc_file:
        if not args.desc_file.is_file():
            raise PayloadValidationError(f"描述文件不存在：{args.desc_file}")
        return args.desc_file.read_text(encoding="utf-8")
    if args.desc is not None:
        return args.desc
    return payload_desc


def load_payload(payload_path: Path) -> LongformPayload:
    if not payload_path.is_file():
        raise PayloadValidationError(f"载荷文件不存在：{payload_path}")

    data = json.loads(payload_path.read_text(encoding="utf-8"))
    title = str(data.get("title", "")).strip()
    parts = data.get("parts")
    images = data.get("images")
    desc = str(data.get("desc", ""))

    if not title:
        raise PayloadValidationError("载荷缺少非空标题字段 `title`。")
    if not isinstance(parts, list) or not parts or not all(isinstance(item, str) for item in parts):
        raise PayloadValidationError("载荷字段 `parts` 必须是非空字符串列表。")
    if images is None:
        images = []
    if not isinstance(images, list) or not all(isinstance(item, str) for item in images):
        raise PayloadValidationError("载荷字段 `images` 必须是字符串路径列表。")

    resolved_images = [Path(item).expanduser().resolve() for item in images]
    missing = [str(path) for path in resolved_images if not path.is_file()]
    if missing:
        raise PayloadValidationError(f"以下图片不存在：{', '.join(missing)}")
    if len(parts) != len(resolved_images) + 1:
        raise PayloadValidationError(
            "载荷结构不合法：`parts` 数量必须等于 `images` 数量加一。"
            f"当前 parts={len(parts)}, images={len(resolved_images)}"
        )

    return LongformPayload(title=title, parts=parts, images=resolved_images, desc=desc)


def ensure_screenshot_dir(path: Path | None) -> Path:
    if path is None:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        path = Path.cwd() / f"xhs-longform-run-{timestamp}"
    path.mkdir(parents=True, exist_ok=True)
    return path


def print_plan(payload: LongformPayload, visibility: str, publish: bool, screenshot_dir: Path, desc: str) -> None:
    print("=== Xiaohongshu Longform Plan ===")
    print(f"title: {payload.title}")
    print(f"parts: {len(payload.parts)}")
    print(f"images: {len(payload.images)}")
    print(f"visibility: {VISIBILITY_TEXT[visibility]}")
    print(f"mode: {'publish' if publish else 'dry-run'}")
    print(f"short_desc_length: {len(desc)}")
    print(f"screenshot_dir: {screenshot_dir}")
    for index, image in enumerate(payload.images, start=1):
        print(f"image_{index}: {image}")


def to_plain_desc_html(text: str) -> str:
    text = text.strip()
    if not text:
        return ""
    paragraphs = []
    for chunk in text.split("\n\n"):
        lines = [line.strip() for line in chunk.splitlines() if line.strip()]
        if not lines:
            continue
        paragraph_text = "<br>".join(escape_html(line) for line in lines)
        paragraphs.append(f"<p>{paragraph_text}</p>")
    return "".join(paragraphs)


def escape_html(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def attach_dialog_logger(page: Page) -> None:
    def _handle(dialog: Dialog) -> None:
        print(f"[dialog] {dialog.type}: {dialog.message}")
        dialog.accept()

    page.on("dialog", _handle)


def click_first_visible(page: Page, builders: list[Callable[[], Locator]], timeout_ms: int = 1_500) -> bool:
    for builder in builders:
        locator = builder()
        try:
            if locator.count() and locator.first.is_visible():
                locator.first.click(timeout=timeout_ms)
                return True
        except PlaywrightTimeoutError:
            continue
    return False


def wait_until_visible(locator: Locator, timeout_ms: int, name: str) -> Locator:
    locator.first.wait_for(state="visible", timeout=timeout_ms)
    return locator.first


def open_longform_editor(page: Page, timeout_ms: int) -> None:
    page.goto(ARTICLE_ENTRY_URL, wait_until="domcontentloaded")
    page.wait_for_load_state("networkidle", timeout=timeout_ms)

    editor_title = page.locator('textarea[placeholder="输入标题"]')
    editor_body = page.locator("div.tiptap.ProseMirror")
    if editor_title.count() and editor_title.first.is_visible() and editor_body.count() and editor_body.first.is_visible():
        return

    click_first_visible(
        page,
        [
            lambda: page.get_by_text("写长文", exact=True),
            lambda: page.locator("text=写长文"),
        ],
        timeout_ms=2_000,
    )

    click_first_visible(
        page,
        [
            lambda: page.get_by_role("button", name="新的创作"),
            lambda: page.locator("text=新的创作"),
        ],
        timeout_ms=2_000,
    )

    wait_until_visible(page.locator('textarea[placeholder="输入标题"]'), timeout_ms, "longform title")
    wait_until_visible(page.locator("div.tiptap.ProseMirror"), timeout_ms, "longform editor")


def clear_contenteditable(page: Page, editor: Locator) -> None:
    editor.click()
    page.keyboard.press("Control+A")
    page.keyboard.press("Backspace")
    page.wait_for_timeout(150)


def place_cursor_at_end_and_insert_html(page: Page, editor_selector: str, html: str) -> None:
    if not html.strip():
        return
    page.evaluate(
        """
        ({ selector, html }) => {
          const editor = document.querySelector(selector);
          if (!editor) {
            throw new Error(`Editor not found: ${selector}`);
          }
          editor.focus();
          const selection = window.getSelection();
          const range = document.createRange();
          range.selectNodeContents(editor);
          range.collapse(false);
          selection.removeAllRanges();
          selection.addRange(range);
          const supported = typeof document.execCommand === 'function';
          if (supported) {
            document.execCommand('insertHTML', false, html);
          } else {
            editor.insertAdjacentHTML('beforeend', html);
            editor.dispatchEvent(new InputEvent('input', { bubbles: true, inputType: 'insertText', data: '' }));
          }
        }
        """,
        {"selector": editor_selector, "html": html},
    )
    page.wait_for_timeout(200)


def locate_image_button(page: Page) -> Locator:
    candidates = [
        page.get_by_role("button", name=re.compile("图片")),
        page.locator('button[title*="图片"]'),
        page.locator('button[aria-label*="图片"]'),
    ]
    for locator in candidates:
        if locator.count() and locator.first.is_visible():
            return locator.first

    menu_buttons = page.locator("button.menu-item")
    if menu_buttons.count() >= 9:
        return menu_buttons.nth(8)
    raise PublishAutomationError("没有找到长文编辑器的图片按钮。")


def insert_image(page: Page, editor: Locator, image_path: Path) -> None:
    button = locate_image_button(page)
    before_count = editor.locator("img").count()

    try:
        with page.expect_file_chooser(timeout=3_000) as chooser_info:
            button.click()
        chooser = chooser_info.value
        chooser.set_files(str(image_path))
    except PlaywrightTimeoutError:
        file_input = page.locator('input[type="file"]').last
        if not file_input.count():
            raise PublishAutomationError("图片按钮点击后没有出现文件选择器。")
        file_input.set_input_files(str(image_path))

    try:
        page.wait_for_function(
            """
            ({ selector, expectedCount }) => {
              const editor = document.querySelector(selector);
              if (!editor) return false;
              return editor.querySelectorAll('img').length >= expectedCount;
            }
            """,
            {"selector": "div.tiptap.ProseMirror", "expectedCount": before_count + 1},
            timeout=30_000,
        )
    except PlaywrightTimeoutError:
        page.wait_for_timeout(5_000)


def fill_longform_editor(page: Page, payload: LongformPayload) -> None:
    title_box = wait_until_visible(page.locator('textarea[placeholder="输入标题"]'), 20_000, "longform title")
    editor = wait_until_visible(page.locator("div.tiptap.ProseMirror"), 20_000, "longform body")

    title_box.fill(payload.title)
    clear_contenteditable(page, editor)
    for index, part in enumerate(payload.parts):
        place_cursor_at_end_and_insert_html(page, "div.tiptap.ProseMirror", part)
        if index < len(payload.images):
            insert_image(page, editor, payload.images[index])
    page.wait_for_timeout(600)


def apply_one_click_layout(page: Page, timeout_ms: int) -> None:
    button = wait_until_visible(page.get_by_role("button", name="一键排版"), 20_000, "one-click layout")
    button.click()

    try:
        page.wait_for_function(
            """
            () => {
              return window.location.href.includes('/publish/update') || document.body.innerText.includes('图片编辑');
            }
            """,
            timeout=timeout_ms,
        )
    except PlaywrightTimeoutError as exc:
        raise PublishAutomationError("一键排版超时，页面没有进入图片发布阶段。") from exc

    wait_until_visible(page.locator('input[placeholder="填写标题会有更多赞哦"]'), timeout_ms, "post-layout title")
    wait_until_visible(page.locator("text=图片编辑"), timeout_ms, "image editor")


def clear_short_desc(page: Page, editor: Locator) -> None:
    editor.click()
    page.keyboard.press("Control+A")
    page.keyboard.press("Backspace")
    page.wait_for_timeout(120)


def fill_post_layout_page(page: Page, payload: LongformPayload, desc: str) -> None:
    title_input = wait_until_visible(
        page.locator('input[placeholder="填写标题会有更多赞哦"]'),
        20_000,
        "post-layout title",
    )
    title_input.fill(payload.title)

    editor = page.locator("div.tiptap.ProseMirror").first
    if editor.count() and editor.is_visible():
        clear_short_desc(page, editor)
        if desc.strip():
            place_cursor_at_end_and_insert_html(page, "div.tiptap.ProseMirror", to_plain_desc_html(desc))


def set_visibility(page: Page, visibility: str) -> None:
    target_label = VISIBILITY_TEXT[visibility]
    toggles = [VISIBILITY_TEXT["public"], VISIBILITY_TEXT["private"], VISIBILITY_TEXT["mutual"]]

    clicked = click_first_visible(
        page,
        [lambda label=label: page.get_by_text(label, exact=True) for label in toggles],
        timeout_ms=1_500,
    )
    if not clicked:
        raise PublishAutomationError("没有找到可见性设置入口。")

    wait_until_visible(page.get_by_text(target_label, exact=True), 10_000, "visibility option").click()
    page.wait_for_timeout(500)


def capture_screenshot(page: Page, path: Path) -> Path:
    page.screenshot(path=str(path), full_page=True)
    return path


def publish_or_stop(page: Page, publish: bool) -> None:
    if not publish:
        print("[dry-run] 已填充完排版后的发布页，未点击最终发布。")
        return
    wait_until_visible(page.get_by_role("button", name="发布"), 10_000, "publish button").click()
    try:
        page.wait_for_function(
            """
            () => {
              return window.location.href.includes('/publish/success') || document.body.innerText.includes('发布成功');
            }
            """,
            timeout=60_000,
        )
    except PlaywrightTimeoutError:
        page.wait_for_timeout(5_000)


def verify_manager_page(page: Page, payload: LongformPayload, visibility: str, timeout_ms: int) -> str:
    title_prefix = build_title_prefix(payload.title)
    visibility_text = VISIBILITY_TEXT[visibility]
    page.goto(MANAGER_URL, wait_until="domcontentloaded")
    page.wait_for_load_state("networkidle", timeout=timeout_ms)

    page.wait_for_function(
        """
        ({ titlePrefix, visibilityText }) => {
          const nodes = Array.from(document.querySelectorAll('div, li, article'));
          return nodes.some(node => {
            const text = node.innerText || '';
            return text.includes(titlePrefix) && text.includes(visibilityText);
          });
        }
        """,
        {"titlePrefix": title_prefix, "visibilityText": visibility_text},
        timeout=timeout_ms,
    )

    matched_text = page.evaluate(
        """
        ({ titlePrefix, visibilityText }) => {
          const nodes = Array.from(document.querySelectorAll('div, li, article'));
          const hit = nodes.find(node => {
            const text = node.innerText || '';
            return text.includes(titlePrefix) && text.includes(visibilityText);
          });
          return hit ? hit.innerText : '';
        }
        """,
        {"titlePrefix": title_prefix, "visibilityText": visibility_text},
    )
    if not card_matches(matched_text, title_prefix, visibility_text):
        raise PublishAutomationError("管理页未找到符合预期的私密长文卡片。")
    return matched_text


def write_summary(path: Path, payload: LongformPayload, visibility: str, publish: bool, artifacts: PublishArtifacts, manager_card_text: str | None) -> None:
    summary = {
        "title": payload.title,
        "title_prefix": build_title_prefix(payload.title),
        "visibility": VISIBILITY_TEXT[visibility],
        "mode": "publish" if publish else "dry-run",
        "editor_screenshot": str(artifacts.editor_screenshot) if artifacts.editor_screenshot else None,
        "manager_screenshot": str(artifacts.manager_screenshot) if artifacts.manager_screenshot else None,
        "manager_card_text": manager_card_text,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
    }
    path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def launch_page(args: argparse.Namespace) -> tuple[object, Page]:
    playwright = sync_playwright().start()
    browser_type = playwright.chromium
    channel = None if args.browser_channel == "chromium" else args.browser_channel
    context = browser_type.launch_persistent_context(
        user_data_dir=str(args.user_data_dir.expanduser()),
        channel=channel,
        headless=args.headless,
        slow_mo=args.slow_mo,
        viewport={"width": 1440, "height": 1200},
    )
    page = context.pages[0] if context.pages else context.new_page()
    page.set_default_timeout(args.timeout_ms)
    attach_dialog_logger(page)
    return (playwright, context, page)


def run(args: argparse.Namespace) -> int:
    payload = load_payload(args.payload)
    desc = load_desc_override(args, payload.desc)
    if args.title:
        payload = LongformPayload(title=args.title.strip(), parts=payload.parts, images=payload.images, desc=payload.desc)

    screenshot_dir = ensure_screenshot_dir(args.screenshot_dir)
    print_plan(payload, args.visibility, args.publish, screenshot_dir, desc)

    if args.validate_only:
        return 0

    artifacts = PublishArtifacts(screenshot_dir=screenshot_dir)
    manager_card_text: str | None = None
    playwright, context, page = launch_page(args)
    try:
        open_longform_editor(page, args.timeout_ms)
        fill_longform_editor(page, payload)
        apply_one_click_layout(page, args.layout_timeout_ms)
        fill_post_layout_page(page, payload, desc)
        set_visibility(page, args.visibility)
        artifacts.editor_screenshot = capture_screenshot(page, screenshot_dir / "prepublish-editor.png")
        publish_or_stop(page, args.publish)

        if args.publish:
            manager_card_text = verify_manager_page(page, payload, args.visibility, args.manager_timeout_ms)
            artifacts.manager_screenshot = capture_screenshot(page, screenshot_dir / "manager-proof.png")

        write_summary(screenshot_dir / "run-summary.json", payload, args.visibility, args.publish, artifacts, manager_card_text)
        print(f"summary: {screenshot_dir / 'run-summary.json'}")
        if artifacts.editor_screenshot:
            print(f"editor_screenshot: {artifacts.editor_screenshot}")
        if artifacts.manager_screenshot:
            print(f"manager_screenshot: {artifacts.manager_screenshot}")

        if args.pause_on_finish:
            input("按回车关闭浏览器...")
        return 0
    finally:
        try:
            context.close()
        finally:
            playwright.stop()


def main() -> int:
    args = parse_args()
    try:
        return run(args)
    except (PayloadValidationError, PublishAutomationError) as exc:
        print(f"❌ {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
