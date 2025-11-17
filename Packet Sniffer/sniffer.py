#!/usr/bin/env python3
"""
Network Packet Sniffer & Analyzer
A real-time network traffic monitoring tool with protocol analysis
"""

import socket
import struct
import time
import threading
from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Dict, List, Optional
import json
import argparse
from datetime import datetime

@dataclass
class Packet:
    timestamp: float
    src_ip: str
    dst_ip: str
    src_port: Optional[int]
    dst_port: Optional[int]
    protocol: str
    size: int
    flags: str = ""
    payload: bytes = b""

class RealTimeSniffer:
    def __init__(self, interface: str = None, max_packets: int = 10000):
        self.interface = interface
        self.max_packets = max_packets
        self.packets = deque(maxlen=max_packets)
        self.running = False
        self.socket = None
        
        # Statistics
        self.stats = {
            'total_packets': 0,
            'protocols': defaultdict(int),
            'ips': defaultdict(int),
            'ports': defaultdict(int),
            'bandwidth': deque(maxlen=100),  # Store last 100 bandwidth readings
            'start_time': time.time()
        }
        
        # Alert system
        self.alerts = []
        self.alert_thresholds = {
            'high_bandwidth': 1000000,  # 1MB/s
            'suspicious_port': 9999,
            'many_connections': 100
        }
        
        print("🚀 Network Packet Sniffer Initialized")
        print(f"📊 Max packets to store: {max_packets}")
        print(f"🔔 Alert thresholds: {self.alert_thresholds}")
    
    def create_socket(self):
        """Create raw socket for packet capture"""
        try:
            # Create raw socket
            self.socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))
            
            if self.interface:
                self.socket.bind((self.interface, 0))
                print(f"📡 Listening on interface: {self.interface}")
            else:
                print("📡 Listening on all interfaces...")
                
        except PermissionError:
            print("❌ ERROR: Root privileges required for packet sniffing!")
            print("   Run: sudo python sniffer.py")
            exit(1)
        except Exception as e:
            print(f"❌ Socket creation failed: {e}")
            exit(1)
    
    def start_sniffing(self):
        """Start the packet sniffing process"""
        self.create_socket()
        self.running = True
        
        print("\n🎯 Starting packet capture...")
        print("   Press Ctrl+C to stop and generate report\n")
        
        # Start statistics thread
        stats_thread = threading.Thread(target=self._update_statistics, daemon=True)
        stats_thread.start()
        
        # Start alert monitor
        alert_thread = threading.Thread(target=self._monitor_alerts, daemon=True)
        alert_thread.start()
        
        try:
            while self.running:
                packet_data = self.socket.recv(65535)
                packet = self._parse_packet(packet_data)
                
                if packet:
                    self.packets.append(packet)
                    self._update_realtime_stats(packet)
                    
        except KeyboardInterrupt:
            print("\n⏹️  Stopping packet capture...")
        finally:
            self.stop_sniffing()
    
    def stop_sniffing(self):
        """Stop the packet sniffing process"""
        self.running = False
        if self.socket:
            self.socket.close()
        print("📊 Capture stopped. Generating report...")
    
    def _parse_packet(self, packet_data: bytes) -> Optional[Packet]:
        """Parse raw packet data into structured format"""
        try:
            # Parse Ethernet header
            eth_header = packet_data[:14]
            eth = struct.unpack('!6s6sH', eth_header)
            eth_protocol = socket.ntohs(eth[2])
            
            # Parse IP packet
            if eth_protocol == 0x0800:  # IPv4
                return self._parse_ip_packet(packet_data[14:])
            elif eth_protocol == 0x86DD:  # IPv6
                return self._parse_ipv6_packet(packet_data[14:])
            else:
                # Other protocols (ARP, etc.)
                return self._parse_other_protocol(packet_data, eth_protocol)
                
        except Exception as e:
            return None
    
    def _parse_ip_packet(self, ip_packet: bytes) -> Optional[Packet]:
        """Parse IPv4 packet"""
        try:
            # Parse IP header (first 20 bytes)
            ip_header = ip_packet[:20]
            iph = struct.unpack('!BBHHHBBH4s4s', ip_header)
            
            version_ihl = iph[0]
            ihl = version_ihl & 0xF
            iph_length = ihl * 4
            protocol = iph[6]
            src_ip = socket.inet_ntoa(iph[8])
            dst_ip = socket.inet_ntoa(iph[9])
            
            # TCP packet
            if protocol == 6:
                return self._parse_tcp_packet(ip_packet, iph_length, src_ip, dst_ip)
            # UDP packet
            elif protocol == 17:
                return self._parse_udp_packet(ip_packet, iph_length, src_ip, dst_ip)
            # ICMP packet
            elif protocol == 1:
                return self._parse_icmp_packet(ip_packet, iph_length, src_ip, dst_ip)
            else:
                return Packet(
                    timestamp=time.time(),
                    src_ip=src_ip,
                    dst_ip=dst_ip,
                    src_port=None,
                    dst_port=None,
                    protocol=f"IP_{protocol}",
                    size=len(ip_packet)
                )
                
        except Exception as e:
            return None
    
    def _parse_tcp_packet(self, ip_packet: bytes, iph_length: int, src_ip: str, dst_ip: str) -> Packet:
        """Parse TCP packet"""
        tcp_header = ip_packet[iph_length:iph_length+20]
        tcph = struct.unpack('!HHLLBBHHH', tcp_header)
        
        src_port = tcph[0]
        dst_port = tcph[1]
        flags = tcph[5]
        
        # Parse TCP flags
        flag_str = ""
        if flags & 0x01: flag_str += "FIN "
        if flags & 0x02: flag_str += "SYN "
        if flags & 0x04: flag_str += "RST "
        if flags & 0x08: flag_str += "PSH "
        if flags & 0x10: flag_str += "ACK "
        if flags & 0x20: flag_str += "URG "
        
        data_offset = (flags >> 12) * 4
        payload = ip_packet[iph_length + data_offset:]
        
        return Packet(
            timestamp=time.time(),
            src_ip=src_ip,
            dst_ip=dst_ip,
            src_port=src_port,
            dst_port=dst_port,
            protocol="TCP",
            size=len(ip_packet),
            flags=flag_str.strip(),
            payload=payload
        )
    
    def _parse_udp_packet(self, ip_packet: bytes, iph_length: int, src_ip: str, dst_ip: str) -> Packet:
        """Parse UDP packet"""
        udp_header = ip_packet[iph_length:iph_length+8]
        udph = struct.unpack('!HHHH', udp_header)
        
        src_port = udph[0]
        dst_port = udph[1]
        payload = ip_packet[iph_length+8:]
        
        return Packet(
            timestamp=time.time(),
            src_ip=src_ip,
            dst_ip=dst_ip,
            src_port=src_port,
            dst_port=dst_port,
            protocol="UDP",
            size=len(ip_packet),
            payload=payload
        )
    
    def _parse_icmp_packet(self, ip_packet: bytes, iph_length: int, src_ip: str, dst_ip: str) -> Packet:
        """Parse ICMP packet"""
        return Packet(
            timestamp=time.time(),
            src_ip=src_ip,
            dst_ip=dst_ip,
            src_port=None,
            dst_port=None,
            protocol="ICMP",
            size=len(ip_packet)
        )
    
    def _parse_ipv6_packet(self, ip_packet: bytes) -> Optional[Packet]:
        """Parse IPv6 packet (simplified)"""
        try:
            # Basic IPv6 parsing
            return Packet(
                timestamp=time.time(),
                src_ip="IPv6_SRC",
                dst_ip="IPv6_DST",
                src_port=None,
                dst_port=None,
                protocol="IPv6",
                size=len(ip_packet)
            )
        except:
            return None
    
    def _parse_other_protocol(self, packet_data: bytes, protocol: int) -> Packet:
        """Parse other network protocols"""
        protocol_name = {
            0x0806: "ARP",
            0x8035: "RARP",
            0x86DD: "IPv6"
        }.get(protocol, f"UNKNOWN_{protocol}")
        
        return Packet(
            timestamp=time.time(),
            src_ip="N/A",
            dst_ip="N/A",
            src_port=None,
            dst_port=None,
            protocol=protocol_name,
            size=len(packet_data)
        )
    
    def _update_realtime_stats(self, packet: Packet):
        """Update real-time statistics"""
        self.stats['total_packets'] += 1
        self.stats['protocols'][packet.protocol] += 1
        self.stats['ips'][packet.src_ip] += 1
        self.stats['ips'][packet.dst_ip] += 1
        
        if packet.src_port:
            self.stats['ports'][packet.src_port] += 1
        if packet.dst_port:
            self.stats['ports'][packet.dst_port] += 1
    
    def _update_statistics(self):
        """Update bandwidth and other statistics in background"""
        last_time = time.time()
        last_packets = 0
        
        while self.running:
            time.sleep(1)  # Update every second
            
            current_time = time.time()
            current_packets = self.stats['total_packets']
            
            time_diff = current_time - last_time
            packet_diff = current_packets - last_packets
            
            if time_diff > 0:
                packets_per_second = packet_diff / time_diff
                bytes_per_second = sum(p.size for p in list(self.packets)[-packet_diff:]) / time_diff
                
                self.stats['bandwidth'].append({
                    'timestamp': current_time,
                    'packets_ps': packets_per_second,
                    'bytes_ps': bytes_per_second
                })
            
            last_time = current_time
            last_packets = current_packets
    
    def _monitor_alerts(self):
        """Monitor for suspicious activity"""
        while self.running:
            time.sleep(5)  # Check every 5 seconds
            
            # Check for high bandwidth
            if self.stats['bandwidth']:
                current_bw = self.stats['bandwidth'][-1]['bytes_ps']
                if current_bw > self.alert_thresholds['high_bandwidth']:
                    self._add_alert(f"🚨 High bandwidth detected: {current_bw/1000000:.2f} MB/s")
            
            # Check for suspicious ports
            suspicious_ports = [port for port in self.stats['ports'] 
                              if port > self.alert_thresholds['suspicious_port']]
            if suspicious_ports:
                self._add_alert(f"⚠️  Suspicious high port activity: {suspicious_ports[:3]}")
    
    def _add_alert(self, message: str):
        """Add a new alert"""
        alert = {
            'timestamp': datetime.now().isoformat(),
            'message': message
        }
        self.alerts.append(alert)
        print(f"🔔 {message}")
    
    def get_realtime_dashboard(self):
        """Generate real-time dashboard data"""
        if not self.packets:
            return "No packets captured yet..."
        
        current_time = time.time()
        runtime = current_time - self.stats['start_time']
        
        dashboard = [
            "=" * 60,
            "📊 REAL-TIME NETWORK DASHBOARD",
            "=" * 60,
            f"🕐 Runtime: {runtime:.1f}s",
            f"📦 Total Packets: {self.stats['total_packets']}",
            f"📈 Packet Rate: {self.stats['bandwidth'][-1]['packets_ps']:.1f} pkt/s" if self.stats['bandwidth'] else "📈 Packet Rate: 0 pkt/s",
            f"💾 Data Rate: {self.stats['bandwidth'][-1]['bytes_ps']/1000:.1f} KB/s" if self.stats['bandwidth'] else "💾 Data Rate: 0 KB/s",
            "",
            "🌐 Protocol Distribution:"
        ]
        
        # Top protocols
        for protocol, count in sorted(self.stats['protocols'].items(), 
                                    key=lambda x: x[1], reverse=True)[:5]:
            percentage = (count / self.stats['total_packets']) * 100
            dashboard.append(f"  {protocol}: {count} ({percentage:.1f}%)")
        
        dashboard.extend([
            "",
            "🔍 Top IP Addresses:"
        ])
        
        # Top IPs
        for ip, count in sorted(self.stats['ips'].items(), 
                              key=lambda x: x[1], reverse=True)[:5]:
            dashboard.append(f"  {ip}: {count} packets")
        
        dashboard.extend([
            "",
            "🔔 Recent Alerts:"
        ])
        
        # Recent alerts
        for alert in self.alerts[-3:]:
            dashboard.append(f"  {alert['timestamp'][11:19]} - {alert['message']}")
        
        dashboard.append("=" * 60)
        
        return "\n".join(dashboard)
    
    def display_realtime_stats(self):
        """Display real-time statistics in console"""
        try:
            while self.running:
                print("\033[2J\033[H")  # Clear screen
                print(self.get_realtime_dashboard())
                time.sleep(2)
        except KeyboardInterrupt:
            pass

def main():
    """Main function to run the packet sniffer"""
    parser = argparse.ArgumentParser(description="Network Packet Sniffer & Analyzer")
    parser.add_argument("-i", "--interface", help="Network interface to sniff on")
    parser.add_argument("-m", "--max-packets", type=int, default=10000, 
                       help="Maximum packets to store in memory")
    parser.add_argument("--no-display", action="store_true", 
                       help="Run without real-time display")
    
    args = parser.parse_args()
    
    # Create sniffer instance
    sniffer = RealTimeSniffer(interface=args.interface, max_packets=args.max_packets)
    
    # Start real-time display in separate thread if not disabled
    if not args.no_display:
        display_thread = threading.Thread(target=sniffer.display_realtime_stats, daemon=True)
        display_thread.start()
    
    # Start packet capture
    sniffer.start_sniffing()
    
    # After capture stops, generate final report
    from analyzer import PacketAnalyzer
    analyzer = PacketAnalyzer(list(sniffer.packets), sniffer.stats, sniffer.alerts)
    analyzer.generate_comprehensive_report()

if __name__ == "__main__":
    main()