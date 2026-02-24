"""Prompt templates for the monitoring daemon agent.

The monitoring daemon primarily operates on deterministic rule checks
rather than LLM inference, so prompts are minimal. The agent relies on
the monitoring_service for executing checks and uses structured logic
for drift detection and alert generation."""

# No LLM prompts needed for this agent -- it operates on deterministic checks.
# This file is included for pattern consistency with other agents.
