"""
Ralpha MCP Client - Connect to UE5 RalphaPlugin server
"""

import socket
import json
from typing import Optional, Dict, Any


class RalphaClient:
    """Client for communicating with the Ralpha MCP server in UE5."""

    def __init__(self, host: str = '127.0.0.1', port: int = 30010):
        self.host = host
        self.port = port

    def send_command(self, command: Dict[str, Any]) -> Dict[str, Any]:
        """Send a command to the MCP server and return the response."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10.0)
        try:
            sock.connect((self.host, self.port))
            message = json.dumps(command) + '\n'
            sock.send(message.encode('utf-8'))
            response = sock.recv(1024 * 1024).decode('utf-8')
            return json.loads(response.strip())
        finally:
            sock.close()

    def is_connected(self) -> bool:
        """Check if the MCP server is reachable."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2.0)
            sock.connect((self.host, self.port))
            sock.close()
            return True
        except:
            return False

    # Screenshot
    def capture_screenshot(self, width: int = 1920, height: int = 1080) -> Dict[str, Any]:
        """Capture a screenshot from the UE5 viewport."""
        return self.send_command({
            "type": "capture_screenshot",
            "width": width,
            "height": height
        })

    # Parameters
    def get_all_parameters(self) -> Dict[str, Any]:
        """Get all current rendering parameters."""
        return self.send_command({"type": "get_all_parameters"})

    # Post-Process
    def set_post_process(self, **params) -> Dict[str, Any]:
        """Set post-process volume parameters."""
        return self.send_command({
            "type": "set_post_process",
            "parameters": params
        })

    # Directional Light
    def set_directional_light(self, **params) -> Dict[str, Any]:
        """Set directional light (sun) parameters."""
        return self.send_command({
            "type": "set_directional_light",
            "parameters": params
        })

    # Sky Light
    def set_sky_light(self, **params) -> Dict[str, Any]:
        """Set sky light parameters."""
        return self.send_command({
            "type": "set_sky_light",
            "parameters": params
        })

    # Fog
    def set_fog(self, **params) -> Dict[str, Any]:
        """Set exponential height fog parameters."""
        return self.send_command({
            "type": "set_exponential_height_fog",
            "parameters": params
        })

    # Camera
    def set_camera(self, **params) -> Dict[str, Any]:
        """Set cine camera parameters."""
        return self.send_command({
            "type": "set_camera",
            "parameters": params
        })

    # Assets
    def search_assets(self, query: str, asset_type: str = "All", max_results: int = 20) -> Dict[str, Any]:
        """Search for assets in the project."""
        return self.send_command({
            "type": "search_assets",
            "query": query,
            "asset_type": asset_type,
            "max_results": max_results
        })

    # Actors
    def spawn_actor(self, asset_path: str, location: tuple = (0, 0, 0),
                    rotation: tuple = (0, 0, 0), scale: float = 1.0,
                    label: str = "") -> Dict[str, Any]:
        """Spawn a static mesh actor."""
        return self.send_command({
            "type": "spawn_actor",
            "asset_path": asset_path,
            "location": {"x": location[0], "y": location[1], "z": location[2]},
            "rotation": {"pitch": rotation[0], "yaw": rotation[1], "roll": rotation[2]},
            "scale": scale,
            "actor_label": label
        })

    def list_actors(self, class_filter: str = "", name_filter: str = "",
                    include_transforms: bool = True) -> Dict[str, Any]:
        """List actors in the scene."""
        return self.send_command({
            "type": "list_actors",
            "class_filter": class_filter,
            "name_filter": name_filter,
            "include_transforms": include_transforms
        })

    def delete_actor(self, actor_id: str) -> Dict[str, Any]:
        """Delete an actor by ID."""
        return self.send_command({
            "type": "delete_actor",
            "actor_id": actor_id
        })


# Convenience function
def connect(host: str = '127.0.0.1', port: int = 30010) -> RalphaClient:
    """Create a new Ralpha client connection."""
    return RalphaClient(host, port)


if __name__ == "__main__":
    # Test connection
    client = RalphaClient()
    if client.is_connected():
        print("Connected to Ralpha MCP server")
        params = client.get_all_parameters()
        print(json.dumps(params, indent=2))
    else:
        print("Could not connect to Ralpha MCP server on port 30010")
        print("Make sure UE5 is running with RalphaPlugin loaded")
