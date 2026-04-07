import requests
import yaml
from datetime import datetime

def convert_netset_to_yaml(url, output_file, list_name):
    print(f"正在下载并转换: {list_name} ({url})")
    response = requests.get(url)
    response.raise_for_status()
    
    lines = response.text.strip().splitlines()
    cidrs = []
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue  # 跳过空行和注释行
        
        if '/' in line:
            # 已经是 CIDR（如 1.2.3.4/24），直接保留
            cidrs.append(line)
        else:
            # 是单个 IP，自动加上 /32
            cidrs.append(line + '/32')
    
    data = {
        "payload": cidrs
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    
    print(f"✅ 转换完成 → {output_file}，共 {len(cidrs)} 条记录")

if __name__ == "__main__":
    # 在这里统一管理所有要转换的列表
    lists = [
        {
            "name": "firehol_level1",
            "url": "https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/firehol_level1.netset",
            "output": "firehol_level1.yaml"
        },
        {
            "name": "firehol_level2",
            "url": "https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/firehol_level2.netset",
            "output": "firehol_level2.yaml"
        }
    ]
    
    for item in lists:
        convert_netset_to_yaml(item["url"], item["output"], item["name"])
    
    print(f"\n🎉 全部列表转换完成！时间：{datetime.now()}")
