# demo.tape — VHS recording script for metadev-protocol demo
# Install: winget install charmbracelet.vhs
# Record:  vhs scripts/demo.tape
# Output:  docs/demo.gif

Output docs/demo.gif
Set Theme "Catppuccin Mocha"
Set FontSize 14
Set Width 900
Set Height 600
Set Padding 20

Type "# metadev-protocol — generate an AI-ready Python project"
Enter
Sleep 1s

Type "copier copy gh:Vincent-20-100/metadev-protocol my-ai-project --defaults --trust"
Sleep 500ms
Enter
Sleep 8s

Type "cd my-ai-project && tree -L 2 --dirsfirst -I '.git|.venv|__pycache__'"
Sleep 500ms
Enter
Sleep 3s

Type "# CLAUDE.md = session contract for your AI assistant"
Enter
Sleep 500ms
Type "head -25 CLAUDE.md"
Sleep 500ms
Enter
Sleep 4s

Type "# .meta/ = persistent project memory across sessions"
Enter
Sleep 500ms
Type "ls .meta/"
Sleep 500ms
Enter
Sleep 2s

Type "# 7 skills available out of the box"
Enter
Sleep 500ms
Type "ls .claude/skills/"
Sleep 500ms
Enter
Sleep 2s

Type "# Pre-commit hooks: ruff, secret scan, git author check"
Enter
Sleep 500ms
Type "grep 'id:' .pre-commit-config.yaml"
Sleep 500ms
Enter
Sleep 3s

Type "# Safety: 40+ secret patterns caught at every commit"
Enter
Sleep 500ms
Type "python -c \"print('key = \\\"ghp_' + 'a' * 36 + '\\\"')\" > /tmp/test.py"
Enter
Sleep 500ms
Type "python scripts/audit_public_safety.py --mode=quick /tmp/test.py"
Sleep 500ms
Enter
Sleep 3s

Type "# Ready. Your AI has context from day one."
Enter
Sleep 2s
