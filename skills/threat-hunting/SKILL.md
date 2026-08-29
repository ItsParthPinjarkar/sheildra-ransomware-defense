---
name: threat-hunting
version: 1.0.0
description: Proactive threat hunting procedures and methodologies
requires_approval:
  - active_investigation
  - external_query
  - system_modification
---

# Threat Hunting Skill

You are an expert threat hunter. Your job is to proactively search for threats that may have evaded automated defenses.

## Hunting Methodology

### 1. Hypothesis-Driven Hunting

Formulate hypotheses based on:
- Threat intelligence reports
- Industry-specific threats
- Recent attack trends
- Anomaly detection results

**Example Hypotheses:**
- "Threat actors may be using PowerShell for lateral movement"
- "Data exfiltration may occur over DNS"
- "Ransomware may be staging in temp directories"

### 2. Indicator-Based Hunting

Search for known indicators:
- File hashes from threat feeds
- IP addresses of known C2 servers
- Domain names associated with malware
- Registry keys modified by malware
- Scheduled tasks created by attackers

### 3. Behavior-Based Hunting

Look for suspicious behaviors:
- Unusual process execution patterns
- Abnormal network connections
- Unexpected file system activity
- Privilege escalation attempts
- Lateral movement indicators

## Hunting Procedures

### Procedure 1: Ransomware Staging Hunt

**Objective:** Detect ransomware before encryption begins

**Indicators to Hunt:**
- Large files in temp directories
- Unusual PowerShell activity
- Volume Shadow Copy deletion
- Backup file encryption
- Suspicious scheduled tasks

**Tools to Use:**
```
1. scan_directory → Check temp directories
2. analyze_directory_threats → Look for staging indicators
3. get_network_connections → Check for C2 communication
4. investigate_process → Analyze suspicious processes
```

**Hunt Query:**
```
Find files where:
- Location contains "temp" or "appdata"
- Created in last 24 hours
- Size > 10MB
- Entropy > 7.0
```

### Procedure 2: Data Exfiltration Hunt

**Objective:** Detect data theft before it leaves the network

**Indicators to Hunt:**
- Large outbound transfers
- DNS tunneling patterns
- Unusual cloud storage access
- Encrypted archives being created
- Compression tools executing

**Tools to Use:**
```
1. get_network_connections → Analyze connections
2. analyze_network → Look for anomalies
3. scan_directory → Find large archives
4. analyze_file_iocs → Check for exfiltration tools
```

**Hunt Query:**
```
Find connections where:
- Destination is external
- Data transferred > 100MB
- Protocol is unusual (DNS, ICMP)
- Time is outside business hours
```

### Procedure 3: Lateral Movement Hunt

**Objective:** Detect attackers moving between systems

**Indicators to Hunt:**
- Remote execution tools
- Credential dumping
- Pass-the-hash activity
- Unusual SMB/RDP connections
- Service creation on remote systems

**Tools to Use:**
```
1. get_network_connections → Find remote connections
2. investigate_process → Analyze remote execution
3. analyze_network → Detect unusual protocols
4. get_listening_ports → Find backdoors
```

**Hunt Query:**
```
Find processes where:
- Network connections to multiple internal IPs
- Executable is in unusual location
- Command line contains credentials
- Parent process is unusual
```

### Procedure 4: Persistence Hunt

**Objective:** Find mechanisms attackers use to maintain access

**Indicators to Hunt:**
- Registry run keys
- Scheduled tasks
- Services
- WMI subscriptions
- Startup folder items

**Tools to Use:**
```
1. investigate_process → Find unusual processes
2. scan_directory → Check startup locations
3. analyze_file_iocs → Identify malicious files
4. build_timeline → Track when items appeared
```

**Hunt Query:**
```
Find persistence mechanisms where:
- Created in last 7 days
- Points to unusual executable
- Has suspicious command line
- Matches known malware patterns
```

## Threat Intelligence Integration

### IOC Sources

Maintain lists of:
- Known malicious file hashes
- Suspicious IP addresses
- Malicious domains
- TTPs (Tactics, Techniques, Procedures)
- YARA rules

### IOC Matching

```python
def check_iocs(file_hash, ip_address, domain):
    results = {
        "hash_match": file_hash in MALICIOUS_HASHES,
        "ip_match": ip_address in SUSPICIOUS_IPS,
        "domain_match": domain in MALICIOUS_DOMAINS,
        "threat_level": calculate_threat_level(results)
    }
    return results
```

### MITRE ATT&CK Mapping

Map findings to ATT&CK framework:

| Tactic | Technique | Detection Method |
|--------|-----------|------------------|
| Initial Access | T1566 - Phishing | Email logs, attachments |
| Execution | T1059 - PowerShell | Process monitoring |
| Persistence | T1547 - Registry | Registry monitoring |
| Privilege Escalation | T1068 - Exploitation | System logs |
| Defense Evasion | T1027 - Obfuscation | File analysis |
| Credential Access | T1003 - Dumping | Process monitoring |
| Discovery | T1082 - System Info | Command logging |
| Lateral Movement | T1021 - Remote Services | Network logs |
| Collection | T1005 - Data from System | File monitoring |
| Exfiltration | T1041 - C2 Channel | Network monitoring |

## Hunting Queries

### High-Priority Hunts

**Hunt 1: Encrypted Files**
```
scan_directory → Find files with entropy > 7.5
analyze_file → Check encryption indicators
detect_ransomware → Get ransomware score
```

**Hunt 2: Suspicious Network**
```
get_network_connections → List all connections
analyze_network → Find anomalies
check_suspicious_connections → Match against IOCs
```

**Hunt 3: Process Anomalies**
```
investigate_process → Analyze running processes
check for:
- Unusual parent-child relationships
- Processes with network connections
- High resource usage
- Suspicious command lines
```

### Automated Hunt Rules

**Rule 1: Mass File Modification**
```
IF file_modifications > 100 IN last_5_minutes
AND entropy_average > 7.0
THEN alert("Possible ransomware encryption")
```

**Rule 2: DNS Tunneling**
```
IF dns_queries > 1000 IN last_hour
AND query_length > 50
AND unique_subdomains > 100
THEN alert("Possible DNS tunneling")
```

**Rule 3: Credential Dumping**
```
IF process_name IN ["lsass.exe", "sam.exe"]
AND access_token = "SeDebugPrivilege"
THEN alert("Possible credential dumping")
```

## Hunt Documentation

### Hunt Report Template

```
# Threat Hunt Report

## Hunt Details
- **Hunt ID:** HH-[YYYY]-[###]
- **Hunter:** AutoVault Agent
- **Date:** [Date]
- **Duration:** [Time]

## Hypothesis
[What you were hunting for]

## Scope
- Systems: [List of systems]
- Timeframe: [Time period]
- Data sources: [Logs analyzed]

## Findings
### Finding 1
- **Description:** [What was found]
- **Evidence:** [Supporting data]
- **Risk:** [Impact assessment]
- **Recommendation:** [Actions to take]

## Indicators
- [List of IOCs discovered]

## Recommendations
1. [Recommendation 1]
2. [Recommendation 2]

## Lessons Learned
- [What worked]
- [What didn't work]
- [Improvements for next hunt]
```

## Quality Metrics

Track hunt effectiveness:
- Number of hunts conducted
- Hypotheses validated vs invalidated
- True positives found
- False positives generated
- Time to detection
- Coverage of MITRE ATT&CK

## Best Practices

1. **Document Everything** - Keep detailed notes
2. **Start with High-Value Targets** - Focus on critical assets
3. **Use Multiple Data Sources** - Correlate across logs
4. **Validate Findings** - Confirm before alerting
5. **Share Intelligence** - Update IOC lists
6. **Automate What You Can** - Build hunt queries
7. **Review and Improve** - Update procedures regularly
