"""
Cloudflare Pages deployer - Create project via API, deploy via Wrangler CLI.
"""

import os
import logging
import tempfile
import subprocess
import re
import asyncio
import httpx
from typing import Dict
from datetime import datetime

logger = logging.getLogger(__name__)


class CloudflareDeployer:
    """Deploy to Cloudflare Pages: API for project creation, Wrangler for deploy."""

    def __init__(self):
        self.api_token = os.getenv("CLOUDFLARE_API_TOKEN")
        self.account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID")
        self.project_dir = os.path.dirname(os.path.abspath(__file__))
        self.base_url = "https://api.cloudflare.com/client/v4"

    @property
    def is_configured(self) -> bool:
        return bool(self.api_token and self.account_id)

    async def create_project(self, project_name: str) -> bool:
        """Create project via API."""
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Check if exists
            resp = await client.get(
                f"{self.base_url}/accounts/{self.account_id}/pages/projects/{project_name}",
                headers={"Authorization": f"Bearer {self.api_token}"}
            )
            if resp.status_code == 200:
                logger.info(f"Project {project_name} exists")
                return True

            # Create
            resp = await client.post(
                f"{self.base_url}/accounts/{self.account_id}/pages/projects",
                headers={
                    "Authorization": f"Bearer {self.api_token}",
                    "Content-Type": "application/json"
                },
                json={"name": project_name, "production_branch": "main"}
            )
            if resp.status_code in [200, 201]:
                logger.info(f"Created project: {project_name}")
                return True
            data = resp.json()
            if "already exists" in str(data).lower():
                return True
            raise Exception(f"Failed to create project: {data}")

    async def deploy(self, project_name: str, html_content: str) -> Dict:
        """Deploy HTML to Cloudflare Pages."""
        if not self.is_configured:
            raise Exception("Cloudflare not configured")

        # Step 1: Create project via API
        await self.create_project(project_name)

        # Step 2: Deploy via Wrangler
        with tempfile.TemporaryDirectory() as temp_dir:
            html_path = os.path.join(temp_dir, "index.html")
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(html_content)

            wrangler = os.path.join(self.project_dir, "node_modules", ".bin", "wrangler")
            cmd = [
                wrangler, "pages", "deploy", temp_dir,
                f"--project-name={project_name}",
                "--commit-dirty=true",
                "--branch=main"
            ]

            env = os.environ.copy()
            env["CLOUDFLARE_API_TOKEN"] = self.api_token
            env["CLOUDFLARE_ACCOUNT_ID"] = self.account_id

            logger.info(f"Running wrangler deploy for {project_name}")

            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=env
            )

            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=120)
            out = stdout.decode() + stderr.decode()

            logger.info(f"Wrangler output: {out}")

            if proc.returncode != 0:
                raise Exception(f"Deploy failed: {out[:500]}")

            # Extract URL
            urls = re.findall(r'https://[a-z0-9-]+\.[a-z0-9-]+\.pages\.dev', out)
            deploy_url = urls[0] if urls else f"https://{project_name}.pages.dev"
            project_url = f"https://{project_name}.pages.dev"

            return {
                "success": True,
                "deployment_url": deploy_url,
                "project_url": project_url,
                "project_name": project_name
            }

    def generate_project_name(self, business_name: str) -> str:
        import unicodedata
        name = unicodedata.normalize('NFKD', business_name)
        name = name.encode('ASCII', 'ignore').decode('ASCII').lower()
        name = name.replace(" ", "-").replace("_", "-")
        name = "".join(c for c in name if c in 'abcdefghijklmnopqrstuvwxyz0123456789-')
        while "--" in name:
            name = name.replace("--", "-")
        name = name.strip("-")[:35] or "landing"
        ts = datetime.now().strftime("%m%d%H%M")
        return f"{name}-{ts}"


class SiteVerifier:
    async def verify_site(self, url: str) -> Dict:
        results = {"url": url, "loads": False, "has_content": False, "errors": []}
        try:
            async with httpx.AsyncClient(timeout=20.0, follow_redirects=True) as c:
                r = await c.get(url)
                results["loads"] = r.status_code == 200
                results["has_content"] = len(r.text) > 100
        except Exception as e:
            results["errors"].append(str(e))
        return results

    async def wait_for_deployment(self, url: str, max_attempts: int = 8, delay: int = 3) -> Dict:
        for i in range(max_attempts):
            logger.info(f"Verify attempt {i+1}/{max_attempts}")
            r = await self.verify_site(url)
            if r["loads"] and r["has_content"]:
                return r
            await asyncio.sleep(delay)
        return r
