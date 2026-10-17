"""lablog：把脚本输出同步写入项目根的 logs/lab.log，终端显示不受影响。

用法（每个阶段脚本开头调用一次）：
    from lablog import start
    start("00 · 环境与模型链路")

之后所有 print 与报错堆栈照常显示在终端，同时自动追加到 logs/lab.log。
跑完不用复制输出，直接让 AI 读 logs/lab.log 即可复盘。
"""

import atexit
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LOG_FILE = ROOT / "logs" / "lab.log"

_file = None


class _Tee:
    """同时写到原流（终端）和日志文件。"""

    def __init__(self, original):
        self.original = original

    def write(self, data):
        self.original.write(data)
        if _file is not None and not _file.closed:  # 退出时 atexit 已关日志，别再写
            _file.write(data)
            _file.flush()
        return len(data)

    def flush(self):
        self.original.flush()
        if _file is not None and not _file.closed:
            _file.flush()


def start(title: str) -> None:
    """接管的 stdout/stderr 双写。重复调用只生效一次。"""
    global _file
    if _file is not None:
        return
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    _file = open(LOG_FILE, "a", encoding="utf-8")
    _file.write(f"\n{'=' * 60}\n### {datetime.now():%Y-%m-%d %H:%M:%S} · {title}\n{'=' * 60}\n")
    _file.flush()
    sys.stdout = _Tee(sys.stdout)
    sys.stderr = _Tee(sys.stderr)
    atexit.register(_footer)


def _footer() -> None:
    if _file is None or _file.closed:
        return
    _file.write(f"### 结束 {datetime.now():%H:%M:%S}\n")
    _file.close()
