#!/usr/bin/env python3
"""
Test suite for Traffic Light Latency Monitor
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from traffic_light import TrafficLightMonitor, PingResult, Status, TierConfig

class TestTrafficLightMonitor(unittest.TestCase):
    
    def setUp(self):
        self.monitor = TrafficLightMonitor()
    
    def test_status_determination(self):
        config = TierConfig("Test", "1.1.1.1", "Test", 50.0, 100.0)
        
        self.assertEqual(self.monitor._determine_status(25.0, config), Status.GREEN)
        self.assertEqual(self.monitor._determine_status(75.0, config), Status.YELLOW)
        self.assertEqual(self.monitor._determine_status(150.0, config), Status.RED)
    
    def test_parse_ping_output_windows(self):
        windows_output = """
Pinging 8.8.8.8 with 32 bytes of data:
Reply from 8.8.8.8: bytes=32 time=23ms TTL=115
Ping statistics for 8.8.8.8:
    Minimum = 22ms, Maximum = 25ms, Average = 23ms
"""
        latency = self.monitor.parse_ping_output(windows_output)
        self.assertEqual(latency, 23.0)
    
    def test_parse_ping_output_linux(self):
        linux_output = """
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=115 time=23.4 ms
--- 8.8.8.8 ping statistics ---
rtt min/avg/max/mdev = 22.800/23.875/25.100/0.900 ms
"""
        latency = self.monitor.parse_ping_output(linux_output)
        self.assertEqual(latency, 23.875)
    
    def test_parse_ping_output_failure(self):
        invalid_output = "This is not a ping output"
        latency = self.monitor.parse_ping_output(invalid_output)
        self.assertIsNone(latency)
    
    @patch('subprocess.run')
    def test_ping_target_success(self, mock_subprocess):
        mock_process = MagicMock()
        mock_process.returncode = 0
        mock_process.stdout = "Average = 13ms"
        mock_subprocess.return_value = mock_process
        
        config = TierConfig("Test", "1.1.1.1", "Test", 50.0, 100.0)
        result = self.monitor.ping_target(config)
        
        self.assertEqual(result.latency, 13.0)
        self.assertEqual(result.status, Status.GREEN)
        self.assertIsNone(result.error)
    
    @patch('subprocess.run')
    def test_ping_target_failure(self, mock_subprocess):
        mock_process = MagicMock()
        mock_process.returncode = 1
        mock_process.stdout = "Ping request could not find host"
        mock_subprocess.return_value = mock_process
        
        config = TierConfig("Test", "invalid.host", "Test", 50.0, 100.0)
        result = self.monitor.ping_target(config)
        
        self.assertIsNone(result.latency)
        self.assertEqual(result.status, Status.RED)
        self.assertIsNotNone(result.error)

class TestEdgeCases(unittest.TestCase):
    
    def setUp(self):
        self.monitor = TrafficLightMonitor()
    
    def test_extreme_latency_values(self):
        config = TierConfig("Test", "1.1.1.1", "Test", 50.0, 100.0)
        
        self.assertEqual(self.monitor._determine_status(0.1, config), Status.GREEN)
        self.assertEqual(self.monitor._determine_status(1000.0, config), Status.RED)
    
    def test_empty_ping_output(self):
        latency = self.monitor.parse_ping_output("")
        self.assertIsNone(latency)

if __name__ == "__main__":
    print("Running unit tests...")
    unittest.main(verbosity=2)