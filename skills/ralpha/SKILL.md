---
name: ralpha
description: "Control Unreal Engine 5 rendering via MCP. Use when manipulating UE5 scenes, adjusting lighting, post-process effects, fog, cameras, or capturing screenshots. Triggers on: adjust ue5, render settings, lighting control, post-process, capture screenshot, scene manipulation."
---

# Ralpha - UE5 Rendering Control

Control Unreal Engine 5 rendering parameters via the Ralpha MCP server. Enables AI-driven style transfer and scene manipulation.

---

## Prerequisites

- UE5 project with RalphaPlugin loaded and running
- MCP server active on `localhost:30010`
- Scene should have: PostProcessVolume, DirectionalLight, SkyLight, ExponentialHeightFog, CineCameraActor

---

## The Job

1. Connect to the Ralpha MCP server (TCP port 30010)
2. Send JSON commands to get/set rendering parameters
3. Capture screenshots for visual feedback
4. Iterate to achieve desired visual style

---

## Connection

Send newline-delimited JSON to `localhost:30010`. Each command returns a JSON response.

**Python example:**
```python
import socket
import json

def send_command(cmd):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', 30010))
    sock.send((json.dumps(cmd) + '\n').encode())
    response = sock.recv(65536).decode()
    sock.close()
    return json.loads(response)

# Get all current parameters
result = send_command({"type": "get_all_parameters"})
print(result)
```

---

## Available Commands

### Screenshot Capture

```json
{"type": "capture_screenshot", "width": 1920, "height": 1080}
```
Returns: `{"success": true, "base64": "...", "path": "..."}`

### Get All Parameters

```json
{"type": "get_all_parameters"}
```
Returns current values for post-process, lighting, fog, and camera.

### Post-Process Volume

```json
{
  "type": "set_post_process",
  "parameters": {
    "exposure_compensation": 1.5,
    "color_saturation": 1.2,
    "color_contrast": 1.1,
    "white_balance_temp": 6500,
    "white_balance_tint": 0,
    "bloom_intensity": 0.8,
    "bloom_threshold": 1.0,
    "vignette_intensity": 0.4,
    "film_grain_intensity": 0.1,
    "chromatic_aberration_intensity": 0.5
  }
}
```

### Directional Light (Sun)

```json
{
  "type": "set_directional_light",
  "parameters": {
    "intensity": 10.0,
    "color": "#FFE4B5",
    "temperature": 5500,
    "pitch": -45.0,
    "yaw": 120.0,
    "source_angle": 1.0,
    "source_soft_angle": 2.0
  }
}
```

### Sky Light

```json
{
  "type": "set_sky_light",
  "parameters": {
    "intensity": 1.0,
    "color": "#87CEEB"
  }
}
```

### Exponential Height Fog

```json
{
  "type": "set_exponential_height_fog",
  "parameters": {
    "enabled": true,
    "fog_density": 0.02,
    "fog_height_falloff": 0.2,
    "fog_inscattering_color": "#B4C8DC",
    "fog_max_opacity": 1.0,
    "start_distance": 0,
    "volumetric_fog": true,
    "volumetric_fog_scattering_distribution": 0.2
  }
}
```

### Camera

```json
{
  "type": "set_camera",
  "parameters": {
    "focal_length": 35.0,
    "aperture": 2.8,
    "focus_distance": 1000.0,
    "dof_enabled": true,
    "motion_blur_amount": 0.5
  }
}
```

### Asset Search

```json
{"type": "search_assets", "query": "tree", "asset_type": "StaticMesh", "max_results": 20}
```

### Spawn Actor

```json
{
  "type": "spawn_actor",
  "asset_path": "/Game/Meshes/Tree.Tree",
  "location": {"x": 0, "y": 0, "z": 0},
  "rotation": {"pitch": 0, "yaw": 45, "roll": 0},
  "scale": 1.0,
  "actor_label": "MyTree"
}
```

### List Actors

```json
{"type": "list_actors", "class_filter": "StaticMesh", "name_filter": "", "include_transforms": true}
```

### Delete Actor

```json
{"type": "delete_actor", "actor_id": "StaticMeshActor_0"}
```

---

## Style Transfer Workflow

1. **Capture reference** - Get current screenshot
2. **Analyze** - Compare to target style/reference image
3. **Adjust** - Modify parameters to move toward target
4. **Iterate** - Repeat until style matches

**Key parameters for mood:**
- **Warm sunset:** High color temp (7000+), orange light color, low sun pitch
- **Cool morning:** Low color temp (5000), blue fog, high exposure
- **Dramatic:** High contrast, deep shadows, vignette
- **Soft/dreamy:** Low contrast, bloom, film grain

---

## Example: Golden Hour Setup

```python
# Set warm directional light
send_command({
    "type": "set_directional_light",
    "parameters": {
        "intensity": 8.0,
        "color": "#FFB347",
        "temperature": 4500,
        "pitch": -15.0,
        "yaw": 280.0
    }
})

# Add warm post-process
send_command({
    "type": "set_post_process",
    "parameters": {
        "exposure_compensation": 0.5,
        "color_saturation": 1.1,
        "white_balance_temp": 5500,
        "bloom_intensity": 1.2,
        "vignette_intensity": 0.3
    }
})

# Add atmospheric fog
send_command({
    "type": "set_exponential_height_fog",
    "parameters": {
        "enabled": true,
        "fog_density": 0.015,
        "fog_inscattering_color": "#FFD4A0",
        "volumetric_fog": true
    }
})

# Capture result
result = send_command({"type": "capture_screenshot"})
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Connection refused | Ensure UE5 editor is running with RalphaPlugin |
| No response | Check Output Log in UE5 for errors |
| Parameters not changing | Verify scene has required actors (PostProcessVolume, etc.) |
| Screenshot blank | Ensure viewport is visible and rendering |

---

## Checklist

Before using this skill:

- [ ] UE5 project is open with RalphaPlugin
- [ ] MCP server shows "started on port 30010" in Output Log
- [ ] Scene has PostProcessVolume (set to Unbound)
- [ ] Scene has DirectionalLight, SkyLight, ExponentialHeightFog
- [ ] Scene has CineCameraActor for camera control
