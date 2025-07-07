#!/usr/bin/env python3
"""
Minimal MCP server that fetches URLs and converts HTML to Markdown using Pandoc.
"""

import asyncio
import json
import sys
import subprocess
import requests
from typing import Any, Dict


class FetchPandocMCP:
    def __init__(self):
        self.tools = [
            {
                "name": "fetch",
                "description": "Fetch a URL and convert HTML to Markdown using Pandoc",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": "The URL to fetch"
                        }
                    },
                    "required": ["url"]
                }
            }
        ]
    
    async def handle_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming JSON-RPC messages"""
        method = message.get("method")
        params = message.get("params", {})
        msg_id = message.get("id")
        
        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {}
                    },
                    "serverInfo": {
                        "name": "fetch-pandoc",
                        "version": "1.0.0"
                    }
                }
            }
        
        elif method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "tools": self.tools
                }
            }
        
        elif method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            
            if tool_name == "fetch":
                result = await self.fetch_and_convert(arguments.get("url"))
                return {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": result
                            }
                        ]
                    }
                }
        
        # Default response for unhandled methods
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "error": {
                "code": -32601,
                "message": f"Method not found: {method}"
            }
        }
    
    async def fetch_and_convert(self, url: str) -> str:
        """Fetch URL and convert HTML to Markdown using Pandoc"""
        try:
            # Fetch the content
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            # Convert HTML to Markdown using Pandoc
            process = subprocess.run(
                ["pandoc", "--from", "html", "--to", "markdown", "--wrap", "none"],
                input=response.text,
                text=True,
                capture_output=True,
                timeout=30
            )
            
            if process.returncode == 0:
                return process.stdout
            else:
                return f"Error converting with Pandoc: {process.stderr}"
                
        except subprocess.TimeoutExpired:
            return "Error: Pandoc conversion timed out"
        except requests.RequestException as e:
            return f"Error fetching URL: {str(e)}"
        except Exception as e:
            return f"Unexpected error: {str(e)}"
    
    async def run(self):
        """Main loop to handle stdin/stdout communication"""
        while True:
            try:
                line = await asyncio.get_event_loop().run_in_executor(
                    None, sys.stdin.readline
                )
                
                if not line:
                    break
                    
                message = json.loads(line.strip())
                response = await self.handle_message(message)
                
                print(json.dumps(response))
                sys.stdout.flush()
                
            except json.JSONDecodeError:
                continue
            except Exception as e:
                error_response = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {
                        "code": -32603,
                        "message": f"Internal error: {str(e)}"
                    }
                }
                print(json.dumps(error_response))
                sys.stdout.flush()


if __name__ == "__main__":
    server = FetchPandocMCP()
    asyncio.run(server.run())
