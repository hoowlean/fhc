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
            continue
        
        if '/' in line:
            cidrs.append(line)
        else:
            cidrs.append(line + '/32')
    
    # 增加时间戳注释，让每次生成的文件内容都不一样
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')
    header = [
        f"# Generated from FireHOL {list_name} at {timestamp}",
        f"# Total records: {len(cidrs)}",
        "# https://iplists.firehol.org/"
    ]
    
    data = {
        "payload": cidrs
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for h in header:
            f.write(h + '\n')
        f.write('\n')
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    
    print(f"✅ 转换完成 → {output_file}，共 {len(cidrs)} 条记录")

if __name__ == "__main__":
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
        },
    ]
    
    for item in lists:
        convert_netset_to_yaml(item["url"], item["output"], item["name"])
    
    print(f"\n🎉 全部列表转换完成！时间：{datetime.now()}")
