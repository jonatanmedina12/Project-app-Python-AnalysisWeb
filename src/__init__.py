from src.controller.vulnerability_scanner import VulnerabilityScanner
from src.controller.nessus_scaner import NessusScaner

def exe():
    v = VulnerabilityScanner()

    cves_encontradas=v.search_cves("ProFTPD 1.3.5")

    v.pretty_print(cves_encontradas)

def exe_nessus():
    x = NessusScaner()
    x.get_policies()
    x.export_scan(7,"pdf")




