from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.recoco import Timer
import requests
import time

log = core.getLogger()

# API Endpoint
API_URL = "http://your-api-endpoint.amazonaws.com/predict"  # Replace with your actual API URL

def _handle_ConnectionUp(event):
    log.info("🔌 Connection established with Switch %s", event.dpid)

def _handle_FlowStatsReceived(event):
    dpid = event.connection.dpid
    flow_entries = event.stats

    pktcount = 0
    bytecount = 0
    flows = len(flow_entries)
    tot_dur = 0
    proto_counts = {"TCP": 0, "UDP": 0, "ICMP": 0}

    for flow in flow_entries:
        pktcount += flow.packet_count
        bytecount += flow.byte_count
        duration = flow.duration_sec + flow.duration_nsec / 1e9
        tot_dur += duration

        if flow.match.nw_proto == 6:
            proto_counts["TCP"] += 1
        elif flow.match.nw_proto == 17:
            proto_counts["UDP"] += 1
        elif flow.match.nw_proto == 1:
            proto_counts["ICMP"] += 1

    byteperflow = bytecount / flows if flows > 0 else 0
    tot_kbps = (bytecount * 8) / (tot_dur * 1000) if tot_dur > 0 else 0
    rx_kbps = tot_kbps * 0.47  # Approximation

    # Majority protocol
    Protocol = max(proto_counts, key=proto_counts.get)

    # Prepare payload for API
    data = {
        "byteperflow": round(byteperflow, 2),
        "tot_kbps": round(tot_kbps, 2),
        "rx_kbps": round(rx_kbps, 2),
        "flows": flows,
        "bytecount": bytecount,
        "tot_dur": round(tot_dur, 2),
        "Protocol": Protocol
    }

    print("Sending data to model:", data) 

    try:
        response = requests.post(API_URL, json=data)
        result = response.json()
        print("✅ Prediction:", result.get("prediction"))
    except Exception as e:
        print("❌ Error contacting model API:", e)

def request_flow_stats():
    for conn in core.openflow._connections.values():
        conn.send(of.ofp_stats_request(body=of.ofp_flow_stats_request()))

def launch():
    log.info("🚀 Starting Flow Monitor with AWS Lambda Integration")
    core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
    core.openflow.addListenerByName("FlowStatsReceived", _handle_FlowStatsReceived)
    Timer(30, request_flow_stats, recurring=True)  # Poll every 30 seconds
