# DeOps UI Flow & UX Design

## System Context
**AI Mission Control** is a browser-based dashboard built with Streamlit or a React + FastAPI stack. Users can command robots, monitor telemetry, and enforce ethics rules in real time.

## High-Level Flow
```
Login -> Dashboard Home -> [Select Mission]
                        -> Agent View
                        -> Ethics & Fault Monitor
                        -> Mission Controls
                        -> TRN Map & Navigation
                        -> Simulation Mode
                        -> Admin Panel
```

## 1. Login & Authentication
- **Login Screen**: Email/password or admin token
- **Role-Based Access**: Operator, Admin, Developer, Ethics Officer
- **Session Resume**: Reload last mission context if available

## 2. Dashboard Home
| Panel              | Function                                                  |
| ------------------ | --------------------------------------------------------- |
| **Active Agents**  | Avatars and health status for each deployed agent         |
| **TRN Map**        | Real-time 2D/3D terrain-relative map with agent pins      |
| **Telemetry Feed** | Live logs, energy levels, and fault alerts                |
| **Mission Goals**  | Summary of current objectives with reassignment controls  |
| **Active Faults**  | Red flags with timestamp and escalation level             |
| **Ethics Logs**    | Reported rule violations with agent IDs                   |

## 3. Agent View Panel
| Element            | Purpose                                            |
| ------------------ | -------------------------------------------------- |
| **Agent Card**     | Role, energy, tasks, and compliance state          |
| **Location Dot**   | Real-time position on the TRN map                  |
| **Actions**        | Pause, redirect, isolate, or escalate              |
| **Memory**         | Last few tasks or system beliefs                   |
| **Skills**         | Capabilities from `skills.json`                    |
| **Decision Path**  | Mini chain-of-thought visual for latest action    |

## 4. Ethics Monitor Panel
| Feature                 | Description                                              |
| ----------------------- | -------------------------------------------------------- |
| **YAML Editor**         | Edit `de_ethics_rule_sheet.yaml` in-browser              |
| **Rule Impact Visualiser** | Show which agents are affected by each rule           |
| **Violation Logs**      | Filter by timestamp, agent, or policy ID                |
| **Severity Slider**     | Adjust thresholds without a code reload                 |
| **Intervene Button**    | Temporarily disable an agent or reassign a task         |

## 5. TRN Map Panel
| Feature               | Description                                             |
| --------------------- | ------------------------------------------------------- |
| **Terrain Overlay**   | Real or simulated environment with hazards and nodes    |
| **Agent Path Traces** | View past path and upcoming route                       |
| **Goal Nodes**        | Waypoints, mission goals, and hazard markers            |
| **3D Toggle**         | Optional elevation view for space terrain               |
| **Manual Control**    | Drag-and-drop waypoints for direct navigation           |

## 6. Simulation Mode
| Tool                  | Function                                     |
| --------------------- | -------------------------------------------- |
| **Scenario Launcher** | Select preset fault, ethics, or nav tests    |
| **Fault Injector**    | Trigger sensor dropouts or ethics breaches   |
| **Metrics Recorder**  | Export CSV or JSON of agent responses        |
| **Replay Viewer**     | Step-by-step playback of agent activity      |

## 7. Admin Panel
| Tool                  | Use                                           |
| --------------------- | --------------------------------------------- |
| **API/Token Manager** | Regenerate keys and assign scopes            |
| **Self-Healing Status** | View recovery scripts and fault history    |
| **File Uploader**     | Update YAML, mission configs, agent modules  |
| **Logs & Traces**     | Filter by agent, module, or violation        |
| **Restart/Reset**     | Reset mission state or reboot agents         |

## UI Style & Interactions
- **Layout**: Grid-based dashboard with tabbed sections
- **Theme**: Dark mode by default (space operations aesthetic)
- **Colors**: Green = healthy, Yellow = risk, Red = critical
- **Animations**: Pulsing dots for active agents and sliding logs
- **Map**: Zoomable and draggable with modular overlays
