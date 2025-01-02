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



def main ():
    client = connect_metasploit()
    keyword = input("Introduce la palabra clave para buscar exploits:")
    search_exploit(client,keyword)


if __name__ == "__main__":
    main()