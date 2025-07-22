# DeOps Agent Codex

## DePilot
- **What**: High-level navigation & route planning.
- **Why**: Provides safe, efficient path decisions.
- **Who**: Works with TRN sensors and interacts with mission operators.
- **Where**: Onboard flight computer or edge device.
- **When**: During active mission segments.
- **How**: Uses ML-based sensor fusion to select routes.

## SwarmBot
- **What**: Manages team coordination for multi-robot tasks.
- **Why**: Enables distributed coverage and shared workloads.
- **Who**: Communicates with peer SwarmBots and DeOps.
- **Where**: Cloud-based or on specialized nodes.
- **When**: When tasks require multi-agent collaboration.
- **How**: Uses consensus protocols for synchronized operations.

## De-Ethics
- **What**: Evaluates actions against compliance rules.
- **Why**: Prevents unsafe or unethical behavior.
- **Who**: Interfaces with Mission Control and reasoning layer.
- **Where**: Runs in a secure container or on dedicated hardware.
- **When**: Continuously during operations.
- **How**: Applies YAML-based rule set and issues alerts on violations.

## DeOps Support
- **What**: Handles system updates and resource monitoring.
- **Why**: Maintains operational reliability.
- **Who**: Works closely with Mission Control.
- **Where**: Cloud/edge nodes.
- **When**: Background processes throughout the mission lifecycle.
- **How**: Monitors CPU, memory, and network usage; pushes patches.

