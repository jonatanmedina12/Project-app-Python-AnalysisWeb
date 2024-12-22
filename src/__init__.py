from src.controller.vulnerability_scanner import VulnerabilityScanner


def exe():
    v = VulnerabilityScanner()

    print(    v.search_cves("ProFTPD 1.3.5"))



