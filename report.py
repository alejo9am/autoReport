from pathlib import Path
import pandas as pd
import json
import jinja2


def get_all_table_paths(path: str) -> dict:
    path = Path(path).resolve()
    tables = list(path.glob('*.csv'))
    return tables
    
    
def create_tables_dict(paths: list) -> dict:
    tables = {}
    for i, pt in enumerate(paths, 1):
        df = pd.read_csv(pt)
        name = Path(pt).name
        tables[name] = df.to_html()
    return tables
    
    
def read_meta_data(path):
    with open(path) as f:
        meta = json.load(f)
    return meta


def get_template(folder_path, template_name):
    loader = jinja2.FileSystemLoader(folder_path)
    env = jinja2.Environment(loader=loader)
    templ = env.get_template(template_name)
    return templ
    
    
def save_report(report_data, path):
    with open(path, 'w') as f:
        f.write(report_data)
        
if __name__ == '__main__':
    folder_path = 'data'
    paths = get_all_table_paths(folder_path)
    tables = create_tables_dict(paths)
    
    json_path = 'data/meta.json'
    meta = read_meta_data(json_path)
    
    template_name = 'my_template.html'
    templates_folder = 'templates'
    template = get_template(templates_folder, template_name)
    
    report_data = template.render(meta=meta, tables=tables)
    
    out_path = 'data/report.html'
    save_report(report_data, out_path)
    
    print(f"Report save to: {out_path}\n")