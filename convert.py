import requests
import yaml
import sys
from datetime import datetime

def convert_netset_to_yaml(url, output_file, list_name):
    print(f"正在下载并转换: {list_name} ({url})")
    response = requests.get(url)
    response.raise_for_status()
    
    lines = response.text.strip().splitlines()
    cidrs = []
    
    for line in lines:
        line = line.strip()
        if line and not line.startswith('#') and ('.' in line or ':' in line):
            cidrs.append(line)
    
    data = {
        "payload": cidrs
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    
    print(f"转换完成 → {output_file}，共 {len(cidrs)} 条 IP/CIDR")

if __name__ == "__main__":
    # 可以在这里添加更多列表
    lists = [
        {
            "name": "firehol_level1",
            "url": "https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/firehol_level1.netset",
            "output": "firehol_level1.yaml"
        }
    ]
    
    for item in lists:
        convert_netset_to_yaml(item["url"], item["output"], item["name"])
    
    print(f"\n全部转换完成！时间：{datetime.now()}")
