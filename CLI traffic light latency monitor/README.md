
###   Real-Time "Traffic Light" Latency Monitor (CLI Tool)

A Python command-line application designed to diagnose network bottlenecks by providing a color-coded health status across three distinct network tiers.

-   **Problem Solved:** Isolating the source of slow internet performance (LAN vs. ISP vs. Global Internet).

-   **Key Contributions:**

    -   Developed a Python script using the **`subprocess`** module to execute simultaneous `ping` commands against the **Router (Tier 1)**, **ISP Gateway (Tier 2)**, and **Global DNS (Tier 3)**.

    -   Implemented **custom scoring and visualization logic** to translate raw latency (ms) into an actionable **Green/Yellow/Red** status, immediately identifying the network segment experiencing delay.

    -   Demonstrated proficiency in **network diagnostics** and **Layer 3 (IP) analysis** by creating a decisive, color-coded metric for operational health.

