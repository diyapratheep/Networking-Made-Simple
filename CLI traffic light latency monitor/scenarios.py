#!/usr/bin/env python3
"""
Real-world scenarios demonstrating how the Traffic Light Monitor solves common problems
"""

def demonstrate_problem_solving():
    scenarios = {
        "Scenario 1: Wi-Fi Router Issues": {
            "Tier 1": "RED (45ms+)", 
            "Tier 2": "GREEN (25ms)",
            "Tier 3": "GREEN (30ms)",
            "Diagnosis": "Local network bottleneck - fix your Wi-Fi/router",
            "Solution": "Restart router, check Wi-Fi signal, use Ethernet cable"
        },
        "Scenario 2: ISP Problems": {
            "Tier 1": "GREEN (3ms)",
            "Tier 2": "RED (200ms+)", 
            "Tier 3": "RED (250ms+)",
            "Diagnosis": "ISP connectivity issue",
            "Solution": "Contact your internet provider, check ISP status page"
        },
        "Scenario 3: Global Internet Issues": {
            "Tier 1": "GREEN (2ms)",
            "Tier 2": "GREEN (20ms)",
            "Tier 3": "RED (500ms+)", 
            "Diagnosis": "Global routing or destination server issues",
            "Solution": "Wait for routing to improve, try different services"
        },
        "Scenario 4: Perfect Network": {
            "Tier 1": "GREEN (1ms)",
            "Tier 2": "GREEN (15ms)",
            "Tier 3": "GREEN (25ms)",
            "Diagnosis": "Network is perfectly healthy",
            "Solution": "No action needed"
        }
    }
    
    print("🔍 REAL-WORLD PROBLEM SOLVING EXAMPLES")
    print("=" * 60)
    
    for scenario, details in scenarios.items():
        print(f"\n{scenario}")
        print("-" * 40)
        print(f"Local (Tier 1):    {details['Tier 1']}")
        print(f"ISP (Tier 2):      {details['Tier 2']}")
        print(f"Global (Tier 3):   {details['Tier 3']}")
        print(f"🔎 Diagnosis:  {details['Diagnosis']}")
        print(f"🛠️  Solution:   {details['Solution']}")

if __name__ == "__main__":
    demonstrate_problem_solving()