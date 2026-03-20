Integration: deterministic-before-LLM routing

Flow:
request → gate_evaluator → capabilities → provider

Assertions:
- deterministic path chosen when possible
- LLM not invoked for weather queries
- full path traceable
