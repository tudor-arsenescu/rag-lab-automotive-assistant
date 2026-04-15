# Local vs. Cloud LLM Inference — Discussion Notes

## The Spectrum

| Dimension | Local (Ollama + llama3.2:3b) | Cloud (e.g., GPT-4, Claude) |
|-----------|------------------------------|------------------------------|
| **Latency** | Depends on hardware; 1-10s per response on CPU | Typically 1-5s (network + compute) |
| **Cost** | Free after hardware investment | Pay per token; scales with usage |
| **Privacy** | Data never leaves the device | Data sent to third-party servers |
| **Quality** | Good for focused tasks with RAG; limited reasoning | State-of-the-art reasoning and generation |
| **Connectivity** | Works offline | Requires internet |
| **Model size** | Limited by RAM (3B-13B typical on laptops) | No practical limit (100B+ parameters) |
| **Updates** | Manual model pulls | Automatic, provider-managed |

## Why Local Matters for Automotive

In the context of the Android Virtual Assistant project running on a car's infotainment system:

**No reliable connectivity.** A car driving through a tunnel, rural area, or parking garage has no internet. The assistant must work offline.

**Privacy requirements.** Vehicle telemetry, driver behavior data, and personal preferences should not leave the car. OEMs and regulators increasingly mandate on-device processing.

**Latency guarantees.** A driver asking "What does this warning light mean?" needs an answer in seconds, not after a network round-trip that may timeout.

**Cost at scale.** Millions of vehicles making API calls per day would generate enormous cloud costs. On-device inference is a one-time hardware cost.

## How RAG Changes the Equation

RAG reduces the burden on the language model. Instead of needing a massive model that "knows everything," a smaller model only needs to read and summarize the relevant context that RAG retrieves. This is why a 3B parameter model with RAG can outperform a much larger model without RAG on domain-specific questions.

In the automotive PoC, this means a model small enough to run on an ARM Cortex-A76 (the head unit's CPU) can still give accurate answers about the vehicle — because it's reading from the owner's manual, not relying on training data.

## Discussion Questions

1. You tested the pipeline with llama3.2:3b today. What kinds of questions did it handle well? Where did it struggle?

2. If you had access to GPT-4 via API, where would you expect it to produce better answers? Would RAG still help?

3. The production system uses Qwen2.5-0.5B (even smaller than what we used today) on the head unit. What trade-offs does that imply? How might you compensate?

4. Beyond automotive, what other domains benefit from local inference + RAG? (Think: medical devices, factory floor, field service, defense.)

5. If the car does have connectivity sometimes, how would you design a hybrid system that uses local inference offline but can optionally call a cloud model when connected?
