# scripts/gera_relatorio.py
import json
import os
from jinja2 import Environment, FileSystemLoader

# Caminho dos relatórios JSON
scanner_files = {
    "ESLint": "reports/eslint-report.json",
    "Semgrep": "reports/semgrep-report.json",
    "Snyk": "reports/snyk-report.json",
    "Trivy FS": "reports/trivy-app-report.json",
    "Trivy Config": "reports/trivy-docker-report.json",
    "Checkov": "reports/checkov-report.json",
    "Gitleaks": "reports/gitleaks-report.json"
}

# Criticidade -> cor
severity_colors = {
    "CRITICAL": "red",
    "HIGH": "orange",
    "MEDIUM": "yellow",
    "LOW": "blue",
    "INFO": "gray"
}

# Função para normalizar alertas
def parse_json(scanner, file_path):
    alerts = []
    if not os.path.exists(file_path):
        return alerts

    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return alerts

    if scanner == "ESLint":
        for item in data:
            alerts.append({
                "scanner": scanner,
                "file": item.get("filePath"),
                "line": item.get("messages")[0]["line"] if item.get("messages") else None,
                "severity": {2: "HIGH", 1: "MEDIUM"}.get(item.get("messages")[0]["severity"], "LOW") if item.get("messages") else "INFO",
                "message": item.get("messages")[0]["message"] if item.get("messages") else "No message",
                "alert_type": "Codificação e Vulnerabilidade"  # <-- Alerta 
            })
    elif scanner == "Semgrep":
        for item in data.get("results", []):
            alerts.append({
                "scanner": scanner,
                "file": item.get("path"),
                "line": item.get("start", {}).get("line"),
                "severity": item.get("extra", {}).get("severity", "INFO").upper(),
                "message": item.get("message"),
                "alert_type": "Vulnerabilidade"  # <-- alerta de segurança 
            })
    elif scanner == "Snyk":
        for vuln in data.get("vulnerabilities", []):
            alerts.append({
                "scanner": scanner,
                "file": vuln.get("from")[0] if vuln.get("from") else None,
                "line": None,
                "severity": vuln.get("severity", "INFO").upper(),
                "message": vuln.get("title"),
                "alert_type": "Vulnerabilidade"  # <-- alerta de segurança 
            })
    elif scanner.startswith("Trivy"):
        for result in data.get("Results", []):
            # Vulnerabilidades de pacotes
            for v in result.get("Vulnerabilities", []):
                alerts.append({
                    "scanner": scanner,
                    "file": result.get("Target"),
                    "line": v.get("PkgLine", None),  # se disponível
                    "severity": v.get("Severity", "UNKNOWN").upper(),
                    "message": f"{v.get('PkgName', '')} - {v.get('Title', '')}",
                    "alert_type": "Vulnerabilidade"
                })
            # Misconfigurations (configs erradas)
            for m in result.get("Misconfigurations", []):
                alerts.append({
                    "scanner": scanner,
                    "file": result.get("Target"),
                    "line": None,
                    "severity": m.get("Severity", "INFO").upper(),
                    "message": m.get("Title"),
                    "alert_type": "Configuração"
                })
    elif scanner == "Checkov":
        if isinstance(data, list):
            for report in data:
                for result_type in ["failed_checks", "passed_checks", "skipped_checks"]:
                    for check in report.get("results", {}).get(result_type, []):
                        alerts.append({
                            "scanner": scanner,
                            "file": check.get("file_path"),
                            "line": check.get("file_line_range")[0] if check.get("file_line_range") else None,
                            "severity": check.get("severity", "INFO").upper() if check.get("severity") else ("LOW" if result_type=="passed_checks" else "HIGH"),
                            "message": check.get("check_name") + f" ({result_type})",
                            "alert_type": "Seguro" 
                        })
        elif isinstance(data, list):
            for check in data:
                alerts.append({
                    "scanner": scanner,
                    "file": check.get("file_path"),
                    "line": check.get("file_line_range")[0] if check.get("file_line_range") else None,
                    "severity": check.get("severity", "INFO").upper(),
                    "message": check.get("check_name"),
                    "alert_type": "Vulnerabilidade" 
                })
    elif scanner == "Gitleaks":
        for leak in data:
            alerts.append({
                "scanner": scanner,
                "file": leak.get("file"),
                "line": leak.get("line"),
                "severity": "HIGH",
                "message": leak.get("description"),
                "alert_type": "Vulnerabilidade"  # <-- alerta de segurança 
            })
    return alerts

# Coletar todos os alertas
all_alerts = []
for scanner, file_path in scanner_files.items():
    all_alerts.extend(parse_json(scanner, file_path))

# Preparar Jinja2
env = Environment(loader=FileSystemLoader("./scripts"))
template = env.from_string("""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Relatório de Segurança</title>
<style>
body { font-family: Arial, sans-serif; background: #f5f5f5; }
h1 { text-align: center; }
table { width: 100%; border-collapse: collapse; margin-bottom: 2rem; }
th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
th { background: #333; color: white; }
tr:hover { background: #eee; }

/* Cores por severidade */
.high { background-color: red; color: white; }
.critical { background-color: red; color: white; }
.medium { background-color: yellow; }
.low { background-color: lightblue; }
.info { background-color: lightgray; }

/* Cores por tipo de alerta */
.code { font-weight: normal; }
.security { font-weight: bold; }
</style>
</head>
<body>
<h1>Relatório de Segurança do Pipeline</h1>
<table>
<thead>
<tr>
<th>Scanner</th>
<th>Arquivo</th>
<th>Linha</th>
<th>Severidade</th>
<th>Tipo</th>
<th>Mensagem</th>
</tr>
</thead>
<tbody>
{% for alert in alerts %}
<tr class="{{ alert.severity|lower }} {{ alert.alert_type }}">
<td>{{ alert.scanner }}</td>
<td>{{ alert.file or "-" }}</td>
<td>{{ alert.line or "-" }}</td>
<td>{{ alert.severity }}</td>
<td>{{ alert.alert_type }}</td>
<td>{{ alert.message }}</td>
</tr>
{% endfor %}
</tbody>
</table>
<p>Total de alertas: {{ alerts|length }}</p>
</body>
</html>
""")

# Criar pasta reports se não existir
os.makedirs("reports", exist_ok=True)

# Gerar HTML
output_file = "reports/pipeline-report.html"
with open(output_file, "w", encoding="utf-8") as f:
    f.write(template.render(alerts=all_alerts))

print(f"✅ Relatório gerado: {output_file}, total alertas: {len(all_alerts)}")
