#!/usr/bin/env python3
"""
Traffic Light Latency Monitor - Three-Tier Health Check
Diagnose network bottlenecks with color-coded latency monitoring.
"""

import subprocess
import re
import time
import threading
from dataclasses import dataclass
from typing import Optional, Dict, List
from enum import Enum
import sys
import platform

class Status(Enum):
    GREEN = "GREEN"
    YELLOW = "YELLOW"
    RED = "RED"

@dataclass
class TierConfig:
    name: str
    target: str
    description: str
    green_threshold: float
    yellow_threshold: float

@dataclass
class PingResult:
    tier: str
    target: str
    latency: Optional[float]
    status: Status
    error: Optional[str] = None

class TrafficLightMonitor:
    def __init__(self):
        self.tiers = {
            "Tier 1": TierConfig(
                name="Tier 1 (Local)",
                target="192.168.1.1",
                description="Wi-Fi/Ethernet Health - Your Router",
                green_threshold=5.0,
                yellow_threshold=10.0
            ),
            "Tier 2": TierConfig(
                name="Tier 2 (ISP)",
                target="1.1.1.1",
                description="Gateway Connection - ISP DNS",
                green_threshold=50.0,
                yellow_threshold=100.0
            ),
            "Tier 3": TierConfig(
                name="Tier 3 (Global)",
                target="8.8.8.8",
                description="Deep Internet Health - Global Server",
                green_threshold=150.0,
                yellow_threshold=300.0
            )
        }
        
        self.colors = {
            Status.GREEN: "\033[92m",
            Status.YELLOW: "\033[93m",
            Status.RED: "\033[91m",
            "RESET": "\033[0m",
            "BOLD": "\033[1m"
        }

    def get_ping_command(self, target: str) -> List[str]:
        if platform.system().lower() == "windows":
            return ["ping", "-n", "4", target]
        else:
            return ["ping", "-c", "4", target]

    def parse_ping_output(self, output: str) -> Optional[float]:
        patterns = [
            r"Average = (\d+)ms",
            r"min/avg/max/[^=]*=\s*[\d.]+\/([\d.]+)\/[\d.]+\/[\d.]+",
            r"rtt min/avg/max/mdev = [\d.]+/([\d.]+)/[\d.]+/[\d.]+ ms",
            r"([\d.]+)\s*ms\s*[^=]*=\s*[^=]*=\s*[^=]*time"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, output, re.IGNORECASE)
            if match:
                try:
                    return float(match.group(1))
                except (ValueError, IndexError):
                    continue
        return None

    def ping_target(self, tier_config: TierConfig) -> PingResult:
        try:
            command = self.get_ping_command(tier_config.target)
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=10,
                check=False
            )
            
            if result.returncode == 0:
                latency = self.parse_ping_output(result.stdout)
                if latency is not None:
                    status = self._determine_status(latency, tier_config)
                    return PingResult(
                        tier=tier_config.name,
                        target=tier_config.target,
                        latency=latency,
                        status=status
                    )
                else:
                    return PingResult(
                        tier=tier_config.name,
                        target=tier_config.target,
                        latency=None,
                        status=Status.RED,
                        error="Could not parse ping output"
                    )
            else:
                return PingResult(
                    tier=tier_config.name,
                    target=tier_config.target,
                    latency=None,
                    status=Status.RED,
                    error=f"Ping failed with return code {result.returncode}"
                )
                
        except subprocess.TimeoutExpired:
            return PingResult(
                tier=tier_config.name,
                target=tier_config.target,
                latency=None,
                status=Status.RED,
                error="Ping timeout"
            )
        except Exception as e:
            return PingResult(
                tier=tier_config.name,
                target=tier_config.target,
                latency=None,
                status=Status.RED,
                error=f"Unexpected error: {str(e)}"
            )

    def _determine_status(self, latency: float, config: TierConfig) -> Status:
        if latency <= config.green_threshold:
            return Status.GREEN
        elif latency <= config.yellow_threshold:
            return Status.YELLOW
        else:
            return Status.RED

    def colorize_text(self, text: str, status: Status) -> str:
        return f"{self.colors[status]}{text}{self.colors['RESET']}"

    def display_results(self, results: Dict[str, PingResult]):
        print(f"\n{self.colors['BOLD']}🚦 TRAFFIC LIGHT LATENCY MONITOR{self.colors['RESET']}")
        print("=" * 70)
        print(f"{'TIER':<20} {'TARGET':<15} {'LATENCY':<10} {'STATUS':<10} {'DIAGNOSIS'}")
        print("-" * 70)
        
        for tier_name, result in results.items():
            config = self.tiers[tier_name]
            
            if result.latency is not None:
                latency_str = f"{result.latency:.1f} ms"
                status_str = self.colorize_text(result.status.value, result.status)
            else:
                latency_str = "FAILED"
                status_str = self.colorize_text("ERROR", Status.RED)
            
            diagnosis = self._get_diagnosis(results)
            
            print(f"{config.name:<20} {config.target:<15} {latency_str:<10} {status_str:<20} {diagnosis.get(tier_name, '')}")

    def _get_diagnosis(self, results: Dict[str, PingResult]) -> Dict[str, str]:
        diagnosis = {}
        
        for tier_name, result in results.items():
            if result.status == Status.RED:
                if tier_name == "Tier 1":
                    diagnosis[tier_name] = "🔴 Local network issue"
                elif tier_name == "Tier 2":
                    diagnosis[tier_name] = "🔴 ISP connectivity issue"
                elif tier_name == "Tier 3":
                    diagnosis[tier_name] = "🔴 Global internet issue"
            elif result.status == Status.YELLOW:
                diagnosis[tier_name] = "🟡 Performance degraded"
            else:
                diagnosis[tier_name] = "🟢 Healthy"
        
        if (results["Tier 1"].status == Status.RED and 
            results["Tier 2"].status != Status.RED):
            diagnosis["Tier 1"] = "🔴 LOCAL NETWORK BOTTLENECK - Check router/Wi-Fi"
        
        if (results["Tier 2"].status == Status.RED and 
            results["Tier 1"].status != Status.RED):
            diagnosis["Tier 2"] = "🔴 ISP BOTTLENECK - Contact your internet provider"
        
        return diagnosis

    def run_single_check(self) -> Dict[str, PingResult]:
        results = {}
        threads = []
        thread_results = {}
        
        def ping_wrapper(tier_name, config):
            thread_results[tier_name] = self.ping_target(config)
        
        for tier_name, config in self.tiers.items():
            thread = threading.Thread(target=ping_wrapper, args=(tier_name, config))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        return thread_results

    def run_continuous_monitor(self, interval: int = 10):
        print(f"{self.colors['BOLD']}Starting continuous monitoring (Ctrl+C to stop){self.colors['RESET']}")
        try:
            while True:
                results = self.run_single_check()
                self.display_results(results)
                print(f"\nNext check in {interval} seconds...")
                time.sleep(interval)
        except KeyboardInterrupt:
            print(f"\n{self.colors['BOLD']}Monitoring stopped.{self.colors['RESET']}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Traffic Light Latency Monitor - Three-Tier Network Health Check",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # Single check with default targets
  %(prog)s --continuous       # Continuous monitoring every 10 seconds
  %(prog)s --interval 5       # Continuous monitoring every 5 seconds
  %(prog)s --custom-router 192.168.0.1  # Use custom router IP

Diagnosis Guide:
  🟢 All Green: Network is healthy
  🔴 Tier 1 Red: Local network issue (router/Wi-Fi)
  🔴 Tier 2 Red: ISP connectivity problem  
  🔴 Tier 3 Red: Global internet routing issue
        """
    )
    
    parser.add_argument("--continuous", "-c", action="store_true", help="Run continuous monitoring")
    parser.add_argument("--interval", "-i", type=int, default=10, help="Monitoring interval in seconds")
    parser.add_argument("--custom-router", type=str, help="Custom router IP address for Tier 1")
    
    args = parser.parse_args()
    
    monitor = TrafficLightMonitor()
    
    if args.custom_router:
        monitor.tiers["Tier 1"].target = args.custom_router
    
    if args.continuous:
        monitor.run_continuous_monitor(args.interval)
    else:
        results = monitor.run_single_check()
        monitor.display_results(results)

if __name__ == "__main__":
    main()