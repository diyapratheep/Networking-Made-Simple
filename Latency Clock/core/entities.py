from dataclasses import dataclass
from enum import Enum
from typing import Optional
import time

class NetworkStatus(Enum):
    EXCELLENT = "excellent"
    GOOD = "good"
    POOR = "poor"
    OFFLINE = "offline"

@dataclass
class LatencyMeasurement:
    timestamp: float
    latency_ms: float
    packet_loss: bool
    jitter: Optional[float] = None
    target_host: str = "8.8.8.8"

@dataclass
class NetworkStats:
    current_latency: float
    average_latency: float
    packet_loss_rate: float
    jitter: float
    status: NetworkStatus
    trend: str 

class AlertThreshold:
    EXCELLENT_MAX = 5.0
    GOOD_MAX = 20.0
    # Above 20ms is POOR