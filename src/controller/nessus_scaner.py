import os

import requests
from dotenv import load_dotenv
import urllib3

import  time
#Desactivamos el warning relacionado con la comprobación

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class NessusScaner:
    def __int__(self):
        #TODO carga las variables de entorno fichero .env
        load_dotenv()
        self.baseurl =os.getenv("NESSUS_URL")
        self.username =os.getenv("NESSUS_USERNAME")
        self.password=os.getenv("NESSUS_PASSWORD")
        self.token_=None

    def create_session(self):
        """Crea una sesion en NESSUS y almacena el token de sesion.   """
        response = requests.post(f"{self.baseurl}/session",json={"username":self.username,"password":self.password},verify=False)
        if response.status_code ==200:
            self.token_=response.json()['token']
        else:
            print(f"Error al crear la sesión:{response.status_code}-{response.text}")
            return False
        return True

    def get_policies(self):
        """ Obtiene la lista de politicas definidas en nessus """
        if not self.token_:
            print("No hay token de sesion. Iniciando sesion ")
            if not self.create_session():
                return
        headers ={"X-Cookie":f"token={self.token_};"}
        response = requests.get(f"{self.baseurl}/policies",headers=headers,verify=False)
        if response.status_code==200:
            policies = response.json()
            print("lista de politicas : ",policies)
        else:
            print(f"Error al obtener las politicas {response.status_code}-{response.text}")

    def create_scan(self,uuid,scan_name,text_targets,policy_id=None,description="",enable=True,launch="ON_DEMAND"):
        """Crea un escaneo nuevo en nessus"""

        if not self.token_:
            print("No hay token de sesion. Iniciando sesion ")
            if not self.create_session():
                return
        scan_settings ={
            "uuid":uuid,
            "settings":{
                "name":scan_name,
                "description":description,
                "enable":str(enable).lower(),
                "launch":launch,
                "text_targets":text_targets,
                "agent_group_id":[],
                "policy_id":policy_id

            }
        }
        headers = {"X-cookie":f"token:{self.token_};"}
        response = requests.post(f"{self.baseurl}/scan",json=scan_settings,headers=headers,verify=False)
        if response.status_code==200:
            scan = response.json()
        else:
            print("Error al crear el scaner en Nassus")


    def list_scans(self,folder_id=None,last_modification_date=None):
        """ obtiene y muestra todos los escaneos de Nessus """
        if not self.token_:
            print("No hay token de sesion. Iniciando sesion ")
            if not self.create_session():
                return
        headers = {"X-cookie":f"token:{self.token_};"}
        params ={}
        if folder_id:
            params["folder_id"]=folder_id
        if last_modification_date:
            params["last_modification_date"]=last_modification_date
        response = requests.get(f"{self.baseurl}/scan",headers=headers,params=params,verify=False)
        if response.status_code==200:
            scans=response.json().get('scans',[])
            if scans:
                for scan in scans:
                    print(f"ID:{scan['id']}, Nombre:{scan['name']}, Estado: {scan['status']}")
            else:
                print("No se encontraron escaneos en Nessus")
            return scans

        else:
            print(f"Error AL OBTENER EL LISTADO DE ESCANEOS :{response.status_code}-{response.text}")
            return None
    def export_scan(self,scan_id,format_type,file_id=None):
        """ Exporta y descarga los resultados del escaneo en nessus """

        if not self.token_:
            print("No hay token de sesion. Iniciando sesion ")
            if not self.create_session():
                return
        headers = {"X-cookie": f"token:{self.token_};"}

        export_payload = {'format':format_type,'template_id':21}
        export_response =requests.post(f"{self.baseurl}/scans/{scan_id}/export",json=export_payload,headers=headers,verify=False)

        if export_response.status_code!=200:
            print(f"Error al exportar el scaneo {export_response.status_code}-{export_response.text}")
            return None

        # Necesitamos comprobar el file_id del escaneo exportado

        if not file_id:
            file_id =export_response.json()['file']

        # Polling para verficar si el reporte esta listo

        polling_interval = 10

        while True:
            status_response = requests.get(f"{self.baseurl}/scans/{scan_id}/export/{file_id}/status",headers=headers,verify=False)
            print(f"Consultado el estado del informe: {status_response.json()['status']}")
            if status_response.status_code==200 and status_response.json()['status']=='ready':
                break
            time.sleep(polling_interval)
        # DESCARGAMOS EL ARCHIVO

        download_response = requests.get(f"{self.baseurl}/scans/{scan_id}/export/{file_id}/download",headers=headers,verify=False)

        if download_response.status_code==200:
            file_path = f"scan_{scan_id}_export.{format_type}"
            with open(file_path,'wb') as f:
                f.write(download_response.content)
                print(f"Escaneo exportado y descargado con exito {file_path}")
        else:
            print(f"Error al descargar el escaneo exportado :{download_response.status_code}-{download_response.text}")

