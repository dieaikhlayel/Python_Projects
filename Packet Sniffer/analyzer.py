#!/usr/bin/env python3
"""
Packet Analysis and Reporting Module
Analyzes captured packets and generates comprehensive reports
"""

import json
import time
from collections import Counter, defaultdict
from datetime import datetime
from typing import List, Dict, Any
from dataclasses import dataclass
import matplotlib.pyplot as plt
import numpy as np
from sniffer import Packet

class PacketAnalyzer:
    def __init__(self, packets: List[Packet], stats: Dict, alerts: List[Dict]):
        self.packets = packets
        self.stats = stats
        self.alerts = alerts
        self.analysis_results = {}
        
        print(f"🔍 Analyzing {len(packets)} captured packets...")
    
    def generate_comprehensive_report(self):
        """Generate a comprehensive analysis report"""
        print("\n" + "="*70)
        print("📊 COMPREHENSIVE NETWORK ANALYSIS REPORT")
        print("="*70)
        
        self._analyze_protocols()
        self._analyze_traffic_patterns()
        self._analyze_connections()
        self._analyze_security()
        self._analyze_bandwidth()
        self._generate_visualizations()
        self._export_results()
        
        print("\n✅ Analysis complete! Reports saved to 'network_report.json'")
        print("📈 Charts saved as PNG files")
    
    def _analyze_protocols(self):
        """Analyze protocol distribution and characteristics"""
        print("\n🌐 PROTOCOL ANALYSIS")
        print("-" * 40)
        
        protocol_stats = defaultdict(lambda: {'count': 0, 'total_size': 0, 'ports': set()})
        
        for packet in self.packets:
            proto = packet.protocol
            protocol_stats[proto]['count'] += 1
            protocol_stats[proto]['total_size'] += packet.size
            if packet.src_port:
                protocol_stats[proto]['ports'].add(packet.src_port)
            if packet.dst_port:
                protocol_stats[proto]['ports'].add(packet.dst_port)
        
        # Display protocol summary
        total_packets = len(self.packets)
        for protocol, stats in sorted(protocol_stats.items(), 
                                    key=lambda x: x[1]['count'], reverse=True):
            percentage = (stats['count'] / total_packets) * 100
            avg_size = stats['total_size'] / stats['count'] if stats['count'] > 0 else 0
            unique_ports = len(stats['ports'])
            
            print(f"📡 {protocol:8} | {stats['count']:6} packets | {percentage:5.1f}% | "
                  f"Avg: {avg_size:5.1f} bytes | Ports: {unique_ports:3}")
        
        self.analysis_results['protocols'] = protocol_stats
    
    def _analyze_traffic_patterns(self):
        """Analyze traffic patterns and trends"""
        print("\n📈 TRAFFIC PATTERN ANALYSIS")
        print("-" * 40)
        
        if not self.packets:
            print("No packets to analyze")
            return
        
        # Time-based analysis
        timestamps = [p.timestamp for p in self.packets]
        start_time = min(timestamps)
        end_time = max(timestamps)
        duration = end_time - start_time
        
        print(f"⏱️  Capture Duration: {duration:.1f} seconds")
        print(f"📦 Total Packets: {len(self.packets)}")
        print(f"🚀 Average Rate: {len(self.packets)/duration:.1f} packets/second")
        
        # Size distribution
        sizes = [p.size for p in self.packets]
        avg_size = np.mean(sizes)
        max_size = max(sizes)
        min_size = min(sizes)
        
        print(f"💾 Packet Sizes: Avg={avg_size:.1f} bytes, Min={min_size}, Max={max_size}")
        
        # Traffic bursts
        time_windows = self._detect_traffic_bursts()
        if time_windows:
            print(f"⚡ Traffic Bursts Detected: {len(time_windows)} high-activity periods")
        
        self.analysis_results['traffic_patterns'] = {
            'duration': duration,
            'avg_packet_rate': len(self.packets) / duration,
            'size_stats': {'avg': avg_size, 'min': min_size, 'max': max_size},
            'traffic_bursts': time_windows
        }
    
    def _detect_traffic_bursts(self, window_seconds: int = 5, threshold: int = 100) -> List[Dict]:
        """Detect periods of high network activity"""
        if not self.packets:
            return []
        
        timestamps = [p.timestamp for p in self.packets]
        start_time = min(timestamps)
        
        # Create time windows
        windows = defaultdict(int)
        for ts in timestamps:
            window_num = int((ts - start_time) / window_seconds)
            windows[window_num] += 1
        
        # Find bursts (windows with packet count above threshold)
        bursts = []
        for window_num, count in windows.items():
            if count > threshold:
                window_start = start_time + (window_num * window_seconds)
                bursts.append({
                    'start': window_start,
                    'packet_count': count,
                    'rate_per_second': count / window_seconds
                })
        
        return sorted(bursts, key=lambda x: x['packet_count'], reverse=True)
    
    def _analyze_connections(self):
        """Analyze network connections and conversations"""
        print("\n🔗 CONNECTION ANALYSIS")
        print("-" * 40)
        
        connections = defaultdict(lambda: {'packets': 0, 'bytes': 0, 'ports': set()})
        
        for packet in self.packets:
            if packet.src_ip and packet.dst_ip:
                # Create connection key (bidirectional)
                conn_key = tuple(sorted([packet.src_ip, packet.dst_ip]))
                connections[conn_key]['packets'] += 1
                connections[conn_key]['bytes'] += packet.size
                if packet.src_port:
                    connections[conn_key]['ports'].add(packet.src_port)
                if packet.dst_port:
                    connections[conn_key]['ports'].add(packet.dst_port)
        
        # Display top connections
        top_connections = sorted(connections.items(), 
                               key=lambda x: x[1]['packets'], reverse=True)[:10]
        
        print("Top Connections (by packet count):")
        for (ip1, ip2), stats in top_connections:
            avg_size = stats['bytes'] / stats['packets'] if stats['packets'] > 0 else 0
            ports = list(stats['ports'])[:5]  # Show first 5 ports
            print(f"  {ip1:15} ↔ {ip2:15} | {stats['packets']:4} packets | "
                  f"Avg: {avg_size:5.1f} bytes | Ports: {ports}")
        
        self.analysis_results['connections'] = {
            'total_unique': len(connections),
            'top_connections': top_connections
        }
    
    def _analyze_security(self):
        """Analyze potential security issues"""
        print("\n🛡️  SECURITY ANALYSIS")
        print("-" * 40)
        
        security_findings = []
        
        # Check for suspicious ports
        common_ports = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
            80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 993: "IMAPS",
            995: "POP3S", 3389: "RDP", 5900: "VNC"
        }
        
        suspicious_ports = []
        for packet in self.packets:
            for port in [packet.src_port, packet.dst_port]:
                if port and port > 10000 and port not in common_ports:
                    suspicious_ports.append(port)
        
        if suspicious_ports:
            port_counts = Counter(suspicious_ports)
            top_suspicious = port_counts.most_common(5)
            security_findings.append(f"🚨 High port activity: {top_suspicious}")
            print(f"🚨 Suspicious high port numbers detected")
            for port, count in top_suspicious:
                print(f"   Port {port}: {count} packets")
        
        # Check for TCP flags patterns
        tcp_flags = Counter()
        for packet in self.packets:
            if packet.protocol == "TCP" and packet.flags:
                tcp_flags[packet.flags] += 1
        
        unusual_flags = [flags for flags, count in tcp_flags.items() 
                        if "RST" in flags or "FIN" in flags]
        if unusual_flags:
            security_findings.append(f"⚠️  Unusual TCP flags: {unusual_flags}")
            print(f"⚠️  Unusual TCP flag patterns detected")
        
        # Alert summary
        if self.alerts:
            print(f"🔔 Security Alerts Generated: {len(self.alerts)}")
            for alert in self.alerts[-5:]:  # Show last 5 alerts
                print(f"   {alert['timestamp'][11:19]} - {alert['message']}")
        else:
            print("✅ No security alerts generated")
        
        self.analysis_results['security'] = {
            'findings': security_findings,
            'alerts_count': len(self.alerts),
            'recent_alerts': self.alerts[-5:] if self.alerts else []
        }
    
    def _analyze_bandwidth(self):
        """Analyze bandwidth usage patterns"""
        print("\n💾 BANDWIDTH ANALYSIS")
        print("-" * 40)
        
        if not self.packets:
            print("No packets for bandwidth analysis")
            return
        
        total_bytes = sum(p.size for p in self.packets)
        duration = max(p.timestamp for p in self.packets) - min(p.timestamp for p in self.packets)
        
        if duration > 0:
            avg_bandwidth_bps = (total_bytes * 8) / duration
            avg_bandwidth_mbps = avg_bandwidth_bps / 1000000
            
            print(f"📊 Total Data: {total_bytes/1000000:.2f} MB")
            print(f"🌊 Average Bandwidth: {avg_bandwidth_bps:.0f} bps ({avg_bandwidth_mbps:.2f} Mbps)")
            
            # Protocol bandwidth usage
            protocol_bytes = defaultdict(int)
            for packet in self.packets:
                protocol_bytes[packet.protocol] += packet.size
            
            print("\nBandwidth by Protocol:")
            for protocol, bytes_used in sorted(protocol_bytes.items(), 
                                             key=lambda x: x[1], reverse=True)[:5]:
                percentage = (bytes_used / total_bytes) * 100
                print(f"  {protocol:8} | {bytes_used/1000:8.1f} KB | {percentage:5.1f}%")
        
        self.analysis_results['bandwidth'] = {
            'total_bytes': total_bytes,
            'average_bps': avg_bandwidth_bps if duration > 0 else 0,
            'protocol_usage': dict(protocol_bytes)
        }
    
    def _generate_visualizations(self):
        """Generate visualization charts"""
        try:
            import matplotlib.pyplot as plt
            
            print("\n📈 GENERATING VISUALIZATIONS...")
            
            # Protocol distribution pie chart
            if self.analysis_results.get('protocols'):
                protocols = self.analysis_results['protocols']
                labels = list(protocols.keys())
                sizes = [stats['count'] for stats in protocols.values()]
                
                plt.figure(figsize=(10, 8))
                
                plt.subplot(2, 2, 1)
                plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
                plt.title('Protocol Distribution')
                
                # Top IP addresses bar chart
                if self.stats.get('ips'):
                    top_ips = Counter(self.stats['ips']).most_common(10)
                    ips, counts = zip(*top_ips) if top_ips else ([], [])
                    
                    plt.subplot(2, 2, 2)
                    plt.bar(range(len(ips)), counts)
                    plt.title('Top IP Addresses')
                    plt.xticks(range(len(ips)), ips, rotation=45, ha='right')
                    plt.ylabel('Packet Count')
                
                # Bandwidth over time (if available)
                if self.stats.get('bandwidth'):
                    bandwidth_data = list(self.stats['bandwidth'])
                    timestamps = [bw['timestamp'] for bw in bandwidth_data]
                    bytes_rates = [bw['bytes_ps'] for bw in bandwidth_data]
                    
                    # Convert to relative time
                    if timestamps:
                        start_time = min(timestamps)
                        relative_times = [ts - start_time for ts in timestamps]
                        
                        plt.subplot(2, 2, 3)
                        plt.plot(relative_times, bytes_rates)
                        plt.title('Bandwidth Usage Over Time')
                        plt.xlabel('Time (seconds)')
                        plt.ylabel('Bytes/Second')
                
                # Packet size distribution
                sizes = [p.size for p in self.packets]
                plt.subplot(2, 2, 4)
                plt.hist(sizes, bins=50, alpha=0.7, edgecolor='black')
                plt.title('Packet Size Distribution')
                plt.xlabel('Packet Size (bytes)')
                plt.ylabel('Frequency')
                
                plt.tight_layout()
                plt.savefig('network_analysis.png', dpi=150, bbox_inches='tight')
                print("✅ Charts saved as 'network_analysis.png'")
                
                plt.close()
                
        except ImportError:
            print("⚠️  matplotlib not available. Skipping visualizations.")
        except Exception as e:
            print(f"⚠️  Visualization generation failed: {e}")
    
    def _export_results(self):
        """Export analysis results to JSON file"""
        export_data = {
            'analysis_timestamp': datetime.now().isoformat(),
            'summary': {
                'total_packets': len(self.packets),
                'capture_duration': self.analysis_results.get('traffic_patterns', {}).get('duration', 0),
                'total_alerts': len(self.alerts)
            },
            'protocol_analysis': self.analysis_results.get('protocols', {}),
            'traffic_patterns': self.analysis_results.get('traffic_patterns', {}),
            'connection_analysis': self.analysis_results.get('connections', {}),
            'security_analysis': self.analysis_results.get('security', {}),
            'bandwidth_analysis': self.analysis_results.get('bandwidth', {}),
            'alerts': self.alerts
        }
        
        with open('network_report.json', 'w') as f:
            json.dump(export_data, f, indent=2, default=str)
        
        print("✅ Full report exported to 'network_report.json'")

def quick_analysis(packets: List[Packet]):
    """Quick analysis function for basic insights"""
    if not packets:
        print("No packets to analyze")
        return
    
    print("\n🚀 QUICK ANALYSIS")
    print("-" * 40)
    
    # Basic stats
    total_packets = len(packets)
    total_bytes = sum(p.size for p in packets)
    protocols = Counter(p.protocol for p in packets)
    
    print(f"📦 Total Packets: {total_packets}")
    print(f"💾 Total Data: {total_bytes/1000:.1f} KB")
    print(f"🌐 Protocols: {', '.join(f'{k}({v})' for k, v in protocols.most_common(5))}")
    
    # Top talkers
    ips = Counter()
    for p in packets:
        if p.src_ip: ips[p.src_ip] += 1
        if p.dst_ip: ips[p.dst_ip] += 1
    
    print(f"🔝 Top IP: {ips.most_common(1)[0] if ips else 'N/A'}")
    
    # Port activity
    ports = Counter()
    for p in packets:
        if p.src_port: ports[p.src_port] += 1
        if p.dst_port: ports[p.dst_port] += 1
    
    if ports:
        top_port, count = ports.most_common(1)[0]
        print(f"🔌 Most Active Port: {top_port} ({count} packets)")

if __name__ == "__main__":
    # Demo mode - create some sample data
    sample_packets = [
        Packet(time.time(), "192.168.1.1", "192.168.1.2", 80, 54321, "TCP", 1500),
        Packet(time.time(), "192.168.1.2", "192.168.1.1", 54321, 80, "TCP", 60),
        Packet(time.time(), "8.8.8.8", "192.168.1.1", 53, 54322, "UDP", 512),
    ]
    
    sample_stats = {'total_packets': 3, 'protocols': {'TCP': 2, 'UDP': 1}}
    sample_alerts = []
    
    analyzer = PacketAnalyzer(sample_packets, sample_stats, sample_alerts)
    quick_analysis(sample_packets)