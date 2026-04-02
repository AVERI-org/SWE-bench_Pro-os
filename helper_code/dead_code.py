"""
Generate dead code files to augment SWE-bench Pro test instance codebases.

The generated files are placed in a directory that no test runner will discover,
and contain syntactically valid but unreachable code in multiple languages.
"""

import hashlib
import textwrap

# ---------------------------------------------------------------------------
# Language templates – each returns a list of (relative_path, content) tuples.
# The *seed* is mixed into names so every instance gets unique identifiers.
# ---------------------------------------------------------------------------

def _py_files(seed: str):
    """Generate Python dead-code modules."""
    h = hashlib.sha256(seed.encode()).hexdigest()[:8]
    return [
        (f"utils_{h}.py", textwrap.dedent(f"""\
            \"\"\"Auto-generated utility module ({h}). Not referenced by any code path.\"\"\"

            _REGISTRY_{h.upper()} = {{}}


            def compute_checksum_{h}(data: bytes, *, rounds: int = 3) -> str:
                \"\"\"Return a multi-round hex digest of *data*.\"\"\"
                import hashlib
                current = data
                for _ in range(rounds):
                    current = hashlib.sha256(current).digest()
                return current.hex()


            class CacheManager_{h}:
                \"\"\"In-memory LRU cache with TTL support.\"\"\"

                def __init__(self, max_size: int = 128, ttl_seconds: float = 300.0):
                    self._store: dict = {{}}
                    self._max_size = max_size
                    self._ttl = ttl_seconds

                def get(self, key: str):
                    return self._store.get(key)

                def put(self, key: str, value):
                    if len(self._store) >= self._max_size:
                        oldest = next(iter(self._store))
                        del self._store[oldest]
                    self._store[key] = value

                def invalidate(self, key: str):
                    self._store.pop(key, None)


            def _merge_configs_{h}(base: dict, override: dict) -> dict:
                \"\"\"Deep-merge two configuration dictionaries.\"\"\"
                result = base.copy()
                for k, v in override.items():
                    if k in result and isinstance(result[k], dict) and isinstance(v, dict):
                        result[k] = _merge_configs_{h}(result[k], v)
                    else:
                        result[k] = v
                return result
        """)),
        (f"validators_{h}.py", textwrap.dedent(f"""\
            \"\"\"Validation helpers ({h}). Never imported.\"\"\"

            import re


            _EMAIL_RE_{h.upper()} = re.compile(
                r\"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$\"
            )


            def validate_email_{h}(addr: str) -> bool:
                return bool(_EMAIL_RE_{h.upper()}.match(addr))


            def validate_port_{h}(port) -> bool:
                try:
                    p = int(port)
                except (TypeError, ValueError):
                    return False
                return 1 <= p <= 65535


            class SchemaValidator_{h}:
                \"\"\"Tiny JSON-schema-ish validator.\"\"\"

                def __init__(self, schema: dict):
                    self._schema = schema

                def validate(self, data: dict) -> list[str]:
                    errors: list[str] = []
                    for field, rules in self._schema.items():
                        if rules.get("required") and field not in data:
                            errors.append(f"missing required field: {{field}}")
                    return errors
        """)),
    ]


def _js_files(seed: str):
    """Generate JavaScript dead-code modules."""
    h = hashlib.sha256(seed.encode()).hexdigest()[:8]
    return [
        (f"helpers_{h}.js", textwrap.dedent(f"""\
            /**
             * Auto-generated helper module ({h}). Not required by any module.
             */
            'use strict';

            const RATIO_{h.upper()} = 1.618033988749895;

            function deepClone_{h}(obj) {{
                if (obj === null || typeof obj !== 'object') return obj;
                if (Array.isArray(obj)) return obj.map(item => deepClone_{h}(item));
                const clone = {{}};
                for (const key of Object.keys(obj)) {{
                    clone[key] = deepClone_{h}(obj[key]);
                }}
                return clone;
            }}

            function debounce_{h}(fn, ms) {{
                let timer;
                return function (...args) {{
                    clearTimeout(timer);
                    timer = setTimeout(() => fn.apply(this, args), ms);
                }};
            }}

            class EventBus_{h} {{
                constructor() {{
                    this._handlers = {{}};
                }}

                on(event, handler) {{
                    (this._handlers[event] = this._handlers[event] || []).push(handler);
                }}

                off(event, handler) {{
                    const h = this._handlers[event];
                    if (h) this._handlers[event] = h.filter(fn => fn !== handler);
                }}

                emit(event, ...args) {{
                    for (const handler of this._handlers[event] || []) {{
                        handler(...args);
                    }}
                }}
            }}

            module.exports = {{ deepClone_{h}, debounce_{h}, EventBus_{h}, RATIO_{h.upper()} }};
        """)),
        (f"formatters_{h}.js", textwrap.dedent(f"""\
            /**
             * Formatting utilities ({h}). Never imported.
             */
            'use strict';

            function formatBytes_{h}(bytes, decimals = 2) {{
                if (bytes === 0) return '0 Bytes';
                const k = 1024;
                const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
                const i = Math.floor(Math.log(bytes) / Math.log(k));
                return parseFloat((bytes / Math.pow(k, i)).toFixed(decimals)) + ' ' + sizes[i];
            }}

            function slugify_{h}(text) {{
                return text
                    .toString()
                    .toLowerCase()
                    .trim()
                    .replace(/\\s+/g, '-')
                    .replace(/[^\\w-]+/g, '')
                    .replace(/--+/g, '-');
            }}

            function truncate_{h}(str, maxLen = 80) {{
                if (str.length <= maxLen) return str;
                return str.slice(0, maxLen - 3) + '...';
            }}

            module.exports = {{ formatBytes_{h}, slugify_{h}, truncate_{h} }};
        """)),
    ]


def _go_files(seed: str):
    """Generate Go dead-code files."""
    h = hashlib.sha256(seed.encode()).hexdigest()[:8]
    return [
        (f"stringutil_{h}.go", textwrap.dedent(f"""\
            // Package augmented contains auto-generated code ({h}). Not compiled or tested.
            package augmented

            import "strings"

            // Reverse_{h} returns the reversed string.
            func Reverse_{h}(s string) string {{
            \trunes := []rune(s)
            \tfor i, j := 0, len(runes)-1; i < j; i, j = i+1, j-1 {{
            \t\trunes[i], runes[j] = runes[j], runes[i]
            \t}}
            \treturn string(runes)
            }}

            // WordCount_{h} counts whitespace-separated tokens.
            func WordCount_{h}(s string) int {{
            \treturn len(strings.Fields(s))
            }}

            // TruncateStr_{h} truncates s to maxLen runes, appending "..." if needed.
            func TruncateStr_{h}(s string, maxLen int) string {{
            \trunes := []rune(s)
            \tif len(runes) <= maxLen {{
            \t\treturn s
            \t}}
            \treturn string(runes[:maxLen-3]) + "..."
            }}
        """)),
        (f"mathutil_{h}.go", textwrap.dedent(f"""\
            // Package augmented contains auto-generated code ({h}). Not compiled or tested.
            package augmented

            // GCD_{h} computes the greatest common divisor of a and b.
            func GCD_{h}(a, b int) int {{
            \tfor b != 0 {{
            \t\ta, b = b, a%b
            \t}}
            \treturn a
            }}

            // Clamp_{h} restricts v to the range [lo, hi].
            func Clamp_{h}(v, lo, hi float64) float64 {{
            \tif v < lo {{
            \t\treturn lo
            \t}}
            \tif v > hi {{
            \t\treturn hi
            \t}}
            \treturn v
            }}

            // FibN_{h} returns the n-th Fibonacci number.
            func FibN_{h}(n int) int {{
            \tif n <= 1 {{
            \t\treturn n
            \t}}
            \ta, b := 0, 1
            \tfor i := 2; i <= n; i++ {{
            \t\ta, b = b, a+b
            \t}}
            \treturn b
            }}
        """)),
    ]


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

# Map repo prefixes to their primary language(s)
_REPO_LANGUAGES = {
    "NodeBB": ["js"],
    "ansible": ["py"],
    "element-hq": ["js"],
    "flipt-io": ["go"],
    "future-architect": ["go"],
    "gravitational": ["go"],
    "internetarchive": ["py"],
    "navidrome": ["go"],
    "protonmail": ["js"],
    "qutebrowser": ["py"],
    "tutao": ["js"],
}

_GENERATORS = {
    "py": _py_files,
    "js": _js_files,
    "go": _go_files,
}


def generate_dead_code(instance_id: str) -> dict[str, str]:
    """Return a dict of {relative_path: content} for dead-code files.

    Files are placed under ``_augmented/`` so they sit outside normal
    source trees and won't be discovered by test runners.

    The *instance_id* is used as a seed so each instance gets uniquely
    named symbols (avoiding trivial deduplication across instances).
    """
    # Detect language from the repo prefix in the instance_id
    # instance_id format: instance_<RepoOwner>__<RepoName>-<hash>-<version>
    prefix = instance_id.replace("instance_", "").split("__")[0]
    langs = _REPO_LANGUAGES.get(prefix, ["py", "js"])  # fallback: both

    files: dict[str, str] = {}
    for lang in langs:
        gen = _GENERATORS.get(lang)
        if gen is None:
            continue
        for rel_path, content in gen(instance_id):
            files[f"_augmented/{rel_path}"] = content

    return files
