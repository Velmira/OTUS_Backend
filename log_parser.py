import argparse
import os
import re
import json
from collections import defaultdict


# python log_analyzer.py /path/to/log/access.log
def parse_log_line(line):
    pattern = (r'(?P<ip>\S+) - - \[(?P<timestamp>.+)\] "(?P<method>\S+) '
               r'(?P<url>\S+)\s?(?P<protocol>\S+)?\s?(?P<status_code>\S+)?\s?(?P<status_text>\S+)?" '
               r'(?P<bytes_sent>\d+) (?P<response_time>\d+) "(?P<referer>.+)" "(?P<user_agent>.+)" '
               r'(?P<duration>\d+)')
    match = re.match(pattern, line)
    if match:
        return match.groupdict()
    return None


def process_log_files(log_path):
    total_requests = 0
    method_counts = defaultdict(int)
    ip_counts = defaultdict(int)
    longest_requests = []

    if os.path.isfile(log_path):
        log_files = [log_path]
    else:
        log_files = [os.path.join(log_path, f) for f in os.listdir(log_path) if f.endswith('.log')]

    for log_file in log_files:
        with open(log_file, 'r') as file:
            for line in file:
                log_data = parse_log_line(line)
                if log_data:
                    total_requests += 1
                    method_counts[log_data['method']] += 1
                    ip_counts[log_data['ip']] += 1

                    longest_requests.append({
                        'ip': log_data['ip'],
                        'date': log_data['timestamp'],
                        'method': log_data['method'],
                        'url': log_data['url'],
                        'duration': int(log_data['duration'])
                    })
                    longest_requests.sort(key=lambda x: x['duration'], reverse=True)
                    longest_requests = longest_requests[:3]

        top_ips = sorted(ip_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        top_ips = {ip: count for ip, count in top_ips}

        log_stats = {
            'top_ips': top_ips,
            'top_longest': longest_requests,
            'total_stat': dict(method_counts),
            'total_requests': total_requests
        }

        log_file_name = os.path.basename(log_file)
        json_file_name = os.path.splitext(log_file_name)[0] + '.json'
        with open(json_file_name, 'w') as json_file:
            json.dump(log_stats, json_file, indent=2)

        print(json.dumps(log_stats, indent=2))
        print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process logs')
    parser.add_argument('path', help='Path to log file or directory with log files')
    args = parser.parse_args()

    process_log_files(args.path)
