# Constants for Specify CLI
from pathlib import Path

# AI assistant choices
AI_CHOICES = {
    "copilot": "GitHub Copilot",
    "claude": "Claude Code",
    "gemini": "Gemini CLI",
    "cursor": "Cursor",
    "qwen": "Qwen Code",
    "opencode": "opencode",
    "codex": "Codex CLI",
    "windsurf": "Windsurf",
    "kilocode": "Kilo Code",
    "auggie": "Auggie CLI",
    "roo": "Roo Code",
    "q": "Amazon Q Developer CLI",
}

# Script type choices
SCRIPT_TYPE_CHOICES = {"sh": "POSIX Shell (bash/zsh)", "ps": "PowerShell"}

# Official implementation guides repository URL
# This is the canonical source for implementation guides that will be automatically
# integrated into every project initialized with specify init.
# Override: Set SPECIFY_GUIDES_REPO_URL environment variable to use a different repository.
GUIDES_REPO_URL = "git@github.com:yousourceinc/implementation-guides.git"

# Claude CLI local installation path after migrate-installer
CLAUDE_LOCAL_PATH = Path.home() / ".claude" / "local" / "claude"

# ASCII Art Banner
BANNER = """
██╗   ██╗███████╗    ███████╗██████╗ ███████╗ ██████╗██╗███████╗██╗   ██╗
╚██╗ ██╔╝██╔════╝    ██╔════╝██╔══██╗██╔════╝██╔════╝██║██╔════╝╚██╗ ██╔╝
 ╚████╔╝ ███████╗    ███████╗██████╔╝█████╗  ██║     ██║█████╗   ╚████╔╝
  ╚██╔╝  ╚════██║    ╚════██║██╔═══╝ ██╔══╝  ██║     ██║██╔══╝    ╚██╔╝
   ██║   ███████║    ███████║██║     ███████╗╚██████╗██║██║        ██║
   ╚═╝   ╚══════╝    ╚══════╝╚═╝     ╚══════╝ ╚═════╝╚═╝╚═╝        ╚═╝
"""

TAGLINE = "YourSource Spec Kit - Spec-Driven Development Toolkit"

# Mini banner for smaller displays
MINI_BANNER = """
╔═╗╔═╗╔═╗╔═╗╦╔═╗╦ ╦
╚═╗╠═╝║╣ ║  ║╠╣ ╚╦╝
╚═╝╩  ╚═╝╚═╝╩╚   ╩
"""