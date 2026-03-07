#!/usr/bin/env python3
"""
小红书笔记发布脚本 - 增强版
支持直接发布（本地签名）和通过 API 服务发布两种方式

使用方法:
    # 直接发布（使用本地签名）
    python publish_xhs.py --title "标题" --desc "描述" --images cover.png card_1.png
    
    # 通过 API 服务发布
    python publish_xhs.py --title "标题" --desc "描述" --images cover.png card_1.png --api-mode

环境变量:
    在同目录或项目根目录下创建 .env 文件，配置：
    
    # 必需：小红书 Cookie
    XHS_COOKIE=your_cookie_string_here
    
    # 可选：API 服务地址（使用 --api-mode 时需要）
    XHS_API_URL=http://localhost:5005

依赖安装:
    pip install xhs python-dotenv requests
"""

import argparse
import os
import sys
import json
import re
import io
import glob
import contextlib
from pathlib import Path
from typing import List, Optional, Dict, Any

try:
    from dotenv import load_dotenv
    import requests
except ImportError as e:
    print(f"缺少依赖: {e}")
    print("请运行: pip install python-dotenv requests")
    sys.exit(1)


def load_cookie() -> str:
    """从 .env 文件加载 Cookie"""
    # 尝试从多个位置加载 .env
    env_paths = [
        Path.cwd() / '.env',
        Path(__file__).parent.parent / '.env',
        Path(__file__).parent.parent.parent / '.env',
    ]
    
    for env_path in env_paths:
        if env_path.exists():
            load_dotenv(env_path)
            break
    
    cookie = os.getenv('XHS_COOKIE')
    if not cookie:
        print("❌ 错误: 未找到 XHS_COOKIE 环境变量")
        print("请创建 .env 文件，添加以下内容：")
        print("XHS_COOKIE=your_cookie_string_here")
        print("\nCookie 获取方式：")
        print("1. 在浏览器中登录小红书（https://www.xiaohongshu.com）")
        print("2. 打开开发者工具（F12）")
        print("3. 在 Network 标签中查看任意请求的 Cookie 头")
        print("4. 复制完整的 cookie 字符串")
        sys.exit(1)
    
    return cookie


def parse_cookie(cookie_string: str) -> Dict[str, str]:
    """解析 Cookie 字符串为字典"""
    cookies = {}
    for item in cookie_string.split(';'):
        item = item.strip()
        if '=' in item:
            key, value = item.split('=', 1)
            cookies[key.strip()] = value.strip()
    return cookies


def validate_cookie(cookie_string: str) -> bool:
    """验证 Cookie 是否包含必要的字段"""
    cookies = parse_cookie(cookie_string)
    
    # 检查必需的 cookie 字段
    required_fields = ['a1', 'web_session']
    missing = [f for f in required_fields if f not in cookies]
    
    if missing:
        print(f"⚠️ Cookie 可能不完整，缺少字段: {', '.join(missing)}")
        print("这可能导致签名失败，请确保 Cookie 包含 a1 和 web_session 字段")
        return False
    
    return True


def get_api_url() -> str:
    """获取 API 服务地址"""
    return os.getenv('XHS_API_URL', 'http://localhost:5005')


def validate_images(image_paths: List[str]) -> List[str]:
    """验证图片文件是否存在"""
    valid_images = []
    for path in image_paths:
        if os.path.exists(path):
            valid_images.append(os.path.abspath(path))
        else:
            print(f"⚠️ 警告: 图片不存在 - {path}")
    
    if not valid_images:
        print("❌ 错误: 没有有效的图片文件")
        sys.exit(1)
    
    return valid_images


def _natural_sort_key(text: str):
    """用于对 card_1/card_2/... 做自然排序"""
    return [int(tok) if tok.isdigit() else tok.lower() for tok in re.split(r'(\d+)', text)]


def load_desc(desc: str, desc_file: Optional[str]) -> str:
    """从参数或文件加载描述（保留真实换行）"""
    if desc and desc_file:
        print("❌ 错误: 不能同时使用 --desc 和 --desc-file")
        sys.exit(1)
    if desc_file:
        path = Path(desc_file)
        if not path.exists():
            print(f"❌ 错误: 描述文件不存在 - {desc_file}")
            sys.exit(1)
        return path.read_text(encoding='utf-8')
    return desc or ""


def load_images(images: List[str], images_glob: Optional[str]) -> List[str]:
    """从显式路径或 glob 加载图片列表，并做自然排序。"""
    if images and images_glob:
        print("❌ 错误: 不能同时使用 --images 和 --images-glob")
        sys.exit(1)
    if images_glob:
        matched = glob.glob(images_glob)
        matched = sorted(matched, key=_natural_sort_key)
        if not matched:
            print(f"❌ 错误: images glob 未匹配到文件 - {images_glob}")
            sys.exit(1)
        return matched
    return images


@contextlib.contextmanager
def maybe_suppress_output(verbose: bool):
    """
    一些第三方库会在发布过程中向 stdout/stderr 打印大量调试信息。
    默认隐藏这些输出，避免噪音和潜在敏感信息泄露；需要排查时用 --verbose 打开。
    """
    if verbose:
        yield
        return
    with io.StringIO() as _out, io.StringIO() as _err:
        with contextlib.redirect_stdout(_out), contextlib.redirect_stderr(_err):
            yield


class LocalPublisher:
    """本地发布模式：直接使用 xhs 库"""
    
    def __init__(self, cookie: str, *, verbose: bool = False):
        self.cookie = cookie
        self.verbose = verbose
        self.client = None
        
    def init_client(self):
        """初始化 xhs 客户端"""
        try:
            from xhs import XhsClient
            from xhs.help import sign as local_sign
        except ImportError:
            print("❌ 错误: 缺少 xhs 库")
            print("请运行: pip install xhs")
            sys.exit(1)
        
        cookies = parse_cookie(self.cookie)
        a1 = cookies.get('a1', '')
        b1 = cookies.get('b1', '')
        
        def sign_func(uri, data=None, **kwargs):
            """
            xhs 库对 sign 回调的调用参数在不同版本间可能不同（可能会传 a1/ctime/b1 等关键字参数）。
            这里用 **kwargs 兼容，并优先使用 cookie 中解析出的 a1/b1。
            """
            ctime = kwargs.get("ctime")
            a1_param = kwargs.get("a1", "")
            b1_param = kwargs.get("b1", "")
            return local_sign(
                uri,
                data,
                ctime=ctime,
                a1=a1 or a1_param,
                b1=b1 or b1_param,
            )
        
        self.client = XhsClient(cookie=self.cookie, sign=sign_func)
        
    def get_user_info(self) -> Optional[Dict[str, Any]]:
        """获取当前登录用户信息"""
        try:
            info = self.client.get_self_info()
            print(f"👤 当前用户: {info.get('nickname', '未知')}")
            return info
        except Exception as e:
            print(f"⚠️ 无法获取用户信息: {e}")
            return None
    
    def publish(self, title: str, desc: str, images: List[str], 
                is_private: bool = False, post_time: str = None) -> Dict[str, Any]:
        """发布图文笔记"""
        print(f"\n🚀 准备发布笔记（本地模式）...")
        print(f"  📌 标题: {title}")
        print(f"  📝 描述: {desc[:50]}..." if len(desc) > 50 else f"  📝 描述: {desc}")
        print(f"  🖼️ 图片数量: {len(images)}")
        
        try:
            with maybe_suppress_output(self.verbose):
                result = self.client.create_image_note(
                    title=title,
                    desc=desc,
                    files=images,
                    is_private=is_private,
                    post_time=post_time
                )
            
            print("\n✨ 笔记发布成功！")
            if isinstance(result, dict):
                note_id = result.get('note_id') or result.get('id')
                if note_id:
                    print(f"  📎 笔记ID: {note_id}")
                    print(f"  🔗 链接: https://www.xiaohongshu.com/explore/{note_id}")
            
            return result
            
        except Exception as e:
            error_msg = str(e)
            print(f"\n❌ 发布失败: {error_msg}")
            
            # 提供具体的错误排查建议
            if 'sign' in error_msg.lower() or 'signature' in error_msg.lower():
                print("\n💡 签名错误排查建议：")
                print("1. 确保 Cookie 包含有效的 a1 和 web_session 字段")
                print("2. Cookie 可能已过期，请重新获取")
                print("3. 尝试使用 --api-mode 通过 API 服务发布")
            elif 'cookie' in error_msg.lower():
                print("\n💡 Cookie 错误排查建议：")
                print("1. 确保 Cookie 格式正确")
                print("2. Cookie 可能已过期，请重新获取")
                print("3. 确保 Cookie 来自已登录的小红书网页版")
            
            raise


class ApiPublisher:
    """API 发布模式：通过 xhs-api 服务发布"""
    
    def __init__(self, cookie: str, api_url: str = None, *, verbose: bool = False):
        self.cookie = cookie
        self.api_url = api_url or get_api_url()
        self.verbose = verbose
        self.session_id = 'md2redbook_session'
        
    def init_client(self):
        """初始化 API 客户端"""
        print(f"📡 连接 API 服务: {self.api_url}")
        
        # 健康检查
        try:
            resp = requests.get(f"{self.api_url}/health", timeout=5)
            if resp.status_code != 200:
                raise Exception("API 服务不可用")
        except requests.exceptions.RequestException as e:
            print(f"❌ 无法连接到 API 服务: {e}")
            print(f"\n💡 请确保 xhs-api 服务已启动：")
            print(f"   cd xhs-api && python app_full.py")
            sys.exit(1)
        
        # 初始化 session
        try:
            resp = requests.post(
                f"{self.api_url}/init",
                json={
                    "session_id": self.session_id,
                    "cookie": self.cookie
                },
                timeout=30
            )
            result = resp.json()
            
            if resp.status_code == 200 and result.get('status') == 'success':
                print(f"✅ API 初始化成功")
                user_info = result.get('user_info', {})
                if user_info:
                    print(f"👤 当前用户: {user_info.get('nickname', '未知')}")
            elif result.get('status') == 'warning':
                print(f"⚠️ {result.get('message')}")
            else:
                raise Exception(result.get('error', '初始化失败'))
                
        except Exception as e:
            print(f"❌ API 初始化失败: {e}")
            sys.exit(1)
    
    def get_user_info(self) -> Optional[Dict[str, Any]]:
        """获取当前登录用户信息"""
        try:
            resp = requests.post(
                f"{self.api_url}/user/info",
                json={"session_id": self.session_id},
                timeout=10
            )
            if resp.status_code == 200:
                result = resp.json()
                if result.get('status') == 'success':
                    info = result.get('user_info', {})
                    print(f"👤 当前用户: {info.get('nickname', '未知')}")
                    return info
            return None
        except Exception as e:
            print(f"⚠️ 无法获取用户信息: {e}")
            return None
    
    def publish(self, title: str, desc: str, images: List[str], 
                is_private: bool = False, post_time: str = None) -> Dict[str, Any]:
        """发布图文笔记"""
        print(f"\n🚀 准备发布笔记（API 模式）...")
        print(f"  📌 标题: {title}")
        print(f"  📝 描述: {desc[:50]}..." if len(desc) > 50 else f"  📝 描述: {desc}")
        print(f"  🖼️ 图片数量: {len(images)}")
        
        try:
            payload = {
                "session_id": self.session_id,
                "title": title,
                "desc": desc,
                "files": images,
                "is_private": is_private
            }
            if post_time:
                payload["post_time"] = post_time
            
            resp = requests.post(
                f"{self.api_url}/publish/image",
                json=payload,
                timeout=120
            )
            result = resp.json()
            
            if resp.status_code == 200 and result.get('status') == 'success':
                print("\n✨ 笔记发布成功！")
                publish_result = result.get('result', {})
                if isinstance(publish_result, dict):
                    note_id = publish_result.get('note_id') or publish_result.get('id')
                    if note_id:
                        print(f"  📎 笔记ID: {note_id}")
                        print(f"  🔗 链接: https://www.xiaohongshu.com/explore/{note_id}")
                return publish_result
            else:
                raise Exception(result.get('error', '发布失败'))
                
        except Exception as e:
            error_msg = str(e)
            print(f"\n❌ 发布失败: {error_msg}")
            raise


def main():
    parser = argparse.ArgumentParser(
        description='将图片发布为小红书笔记',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  # 基本用法
  python publish_xhs.py -t "我的标题" -d "正文内容" -i cover.png card_1.png card_2.png
  
  # 推荐：从文件读取描述（保留换行）
  python publish_xhs.py -t "我的标题" --desc-file desc.txt -i cover.png card_1.png
  
  # 推荐：用 glob 自动收集并按数字排序图片
  python publish_xhs.py -t "我的标题" --desc-file desc.txt --images-glob "out/card_*.png" --require-image-count 9

  # 使用 API 模式
  python publish_xhs.py -t "我的标题" -d "正文内容" -i *.png --api-mode
  
  # 默认即为私密笔记（推荐先私密预览）
  python publish_xhs.py -t "我的标题" -d "正文内容" -i *.png
  
  # 显式公开发布
  python publish_xhs.py -t "我的标题" -d "正文内容" -i *.png --public
  
  # 定时发布
  python publish_xhs.py -t "我的标题" -d "正文内容" -i *.png --post-time "2024-12-01 10:00:00"
'''
    )
    parser.add_argument(
        '--title', '-t',
        required=True,
        help='笔记标题（不超过20字）'
    )
    parser.add_argument(
        '--desc', '-d',
        default='',
        help='笔记描述/正文内容'
    )
    parser.add_argument(
        '--desc-file',
        default=None,
        help='从文件读取笔记描述/正文（UTF-8，保留真实换行）'
    )
    parser.add_argument(
        '--images', '-i',
        nargs='+',
        default=[],
        help='图片文件路径（可以多个，与 --images-glob 二选一）'
    )
    parser.add_argument(
        '--images-glob',
        default=None,
        help='使用 glob 匹配图片（会按自然序排序，如 card_1, card_2...）'
    )
    parser.add_argument(
        '--require-image-count',
        type=int,
        default=None,
        help='要求图片数量必须等于该值，否则直接报错退出（例如 9）'
    )
    visibility_group = parser.add_mutually_exclusive_group()
    visibility_group.add_argument(
        '--private',
        dest='private',
        action='store_true',
        help='设为私密笔记（默认）'
    )
    visibility_group.add_argument(
        '--public',
        dest='private',
        action='store_false',
        help='设为公开笔记（显式覆盖默认私密）'
    )
    parser.set_defaults(private=True)
    parser.add_argument(
        '--post-time',
        default=None,
        help='定时发布时间（格式：2024-01-01 12:00:00）'
    )
    parser.add_argument(
        '--api-mode',
        action='store_true',
        help='使用 API 模式发布（需要 xhs-api 服务运行）'
    )
    parser.add_argument(
        '--api-url',
        default=None,
        help='API 服务地址（默认: http://localhost:5005）'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='仅验证，不实际发布'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='显示底层库输出（默认会隐藏噪音日志）'
    )
    parser.add_argument(
        '--debug-json',
        default=None,
        help='将最终发布结果写入 JSON 文件（可能包含敏感信息，请谨慎保存）'
    )
    
    args = parser.parse_args()
    
    # 验证标题长度
    if len(args.title) > 20:
        print(f"⚠️ 警告: 标题超过20字，将被截断")
        args.title = args.title[:20]
    
    # 加载 Cookie
    cookie = load_cookie()
    
    # 验证 Cookie 格式
    validate_cookie(cookie)
    
    # 加载描述（支持从文件读取）
    desc = load_desc(args.desc, args.desc_file)
    
    # 加载图片列表（支持 glob）
    image_inputs = load_images(args.images, args.images_glob)
    if not image_inputs:
        print("❌ 错误: 必须提供图片（--images 或 --images-glob）")
        sys.exit(1)
    
    # 验证图片
    valid_images = validate_images(image_inputs)
    if args.require_image_count is not None and len(valid_images) != args.require_image_count:
        print(f"❌ 错误: 图片数量不符合要求：期望 {args.require_image_count}，实际 {len(valid_images)}")
        sys.exit(1)
    
    if args.dry_run:
        print("\n🔍 验证模式 - 不会实际发布")
        print(f"  📌 标题: {args.title}")
        print(f"  📝 描述: {desc}")
        print(f"  🖼️ 图片: {valid_images}")
        print(f"  🔒 私密: {args.private}")
        print(f"  ⏰ 定时: {args.post_time or '立即发布'}")
        print(f"  📡 模式: {'API' if args.api_mode else '本地'}")
        print(f"  🧾 verbose: {args.verbose}")
        print("\n✅ 验证通过，可以发布")
        return
    
    # 选择发布方式
    if args.api_mode:
        publisher = ApiPublisher(cookie, args.api_url, verbose=args.verbose)
    else:
        publisher = LocalPublisher(cookie, verbose=args.verbose)
    
    # 初始化客户端
    publisher.init_client()
    
    # 发布笔记
    try:
        result = publisher.publish(
            title=args.title,
            desc=desc,
            images=valid_images,
            is_private=args.private,
            post_time=args.post_time
        )
        if args.debug_json:
            Path(args.debug_json).write_text(
                json.dumps(result, ensure_ascii=False, indent=2),
                encoding='utf-8'
            )
    except Exception as e:
        sys.exit(1)


if __name__ == '__main__':
    main()
