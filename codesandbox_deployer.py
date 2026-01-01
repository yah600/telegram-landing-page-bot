"""
CodeSandbox Deployer - Creates React sandboxes via API.
"""

import logging
import httpx
import json
import lzstring
from typing import Dict

logger = logging.getLogger(__name__)


class CodeSandboxDeployer:
    """Deploy React projects to CodeSandbox."""

    def __init__(self):
        self.api_url = "https://codesandbox.io/api/v1/sandboxes/define"

    async def deploy(self, files: Dict[str, str], title: str = "Landing Page") -> Dict:
        """
        Deploy files to CodeSandbox.

        Args:
            files: Dict of {filepath: content}
            title: Sandbox title

        Returns:
            Dict with sandbox_id and urls
        """
        # Create the sandbox definition
        sandbox_def = {
            "files": {}
        }

        for path, content in files.items():
            sandbox_def["files"][path] = {"content": content}

        # Add package.json if not present
        if "package.json" not in files:
            sandbox_def["files"]["package.json"] = {
                "content": json.dumps({
                    "name": title.lower().replace(" ", "-"),
                    "private": True,
                    "scripts": {
                        "dev": "next dev",
                        "build": "next build",
                        "start": "next start"
                    },
                    "dependencies": {
                        "next": "14.0.0",
                        "react": "18.2.0",
                        "react-dom": "18.2.0",
                        "tailwindcss": "3.3.0",
                        "autoprefixer": "10.4.16",
                        "postcss": "8.4.31",
                        "lucide-react": "^0.294.0",
                        "clsx": "^2.0.0",
                        "tailwind-merge": "^2.0.0"
                    }
                }, indent=2)
            }

        # Compress and encode for URL
        compressed = lzstring.LZString().compressToBase64(json.dumps(sandbox_def))

        async with httpx.AsyncClient(timeout=60.0) as client:
            # Use POST with JSON
            response = await client.post(
                self.api_url,
                json={"json": 1, **sandbox_def},
                headers={"Content-Type": "application/json"}
            )

            if response.status_code not in [200, 201]:
                # Try URL method
                sandbox_url = f"https://codesandbox.io/api/v1/sandboxes/define?json=1&parameters={compressed}"
                response = await client.get(sandbox_url)

            if response.status_code not in [200, 201]:
                logger.error(f"CodeSandbox error: {response.text}")
                raise Exception(f"CodeSandbox API failed: {response.status_code}")

            data = response.json()
            sandbox_id = data.get("sandbox_id")

            return {
                "success": True,
                "sandbox_id": sandbox_id,
                "editor_url": f"https://codesandbox.io/s/{sandbox_id}",
                "preview_url": f"https://{sandbox_id}.csb.app",
                "embed_url": f"https://codesandbox.io/embed/{sandbox_id}"
            }

    def create_next_project(self, component_code: str, title: str = "Landing Page") -> Dict[str, str]:
        """Create a complete Next.js project structure."""

        files = {
            "pages/index.js": f'''import LandingPage from '../components/LandingPage'

export default function Home() {{
  return <LandingPage />
}}
''',
            "components/LandingPage.jsx": component_code,

            "pages/_app.js": '''import '../styles/globals.css'

export default function App({ Component, pageProps }) {
  return <Component {...pageProps} />
}
''',

            "styles/globals.css": '''@tailwind base;
@tailwind components;
@tailwind utilities;

* {
  font-family: 'Inter', system-ui, sans-serif;
}
''',

            "tailwind.config.js": '''/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,jsx}',
    './components/**/*.{js,jsx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a',
        }
      }
    }
  },
  plugins: []
}
''',

            "postcss.config.js": '''module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
''',

            "package.json": json.dumps({
                "name": title.lower().replace(" ", "-"),
                "private": True,
                "scripts": {
                    "dev": "next dev",
                    "build": "next build",
                    "start": "next start"
                },
                "dependencies": {
                    "next": "14.0.0",
                    "react": "18.2.0",
                    "react-dom": "18.2.0",
                    "tailwindcss": "3.3.0",
                    "autoprefixer": "10.4.16",
                    "postcss": "8.4.31",
                    "lucide-react": "^0.294.0"
                }
            }, indent=2),

            "next.config.js": '''/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
}
module.exports = nextConfig
'''
        }

        return files
