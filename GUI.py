import json
import requests
requests.packages.urllib3.disable_warnings()

# Variables globales
api_url = "https://192.168.56.102/restconf/"
basicauth = ("cisco", "cisco123!")
headers = {"Accept": "application/yang-data+json", "Content-type": "application/yang-data+json"}

def menu():
    while True:
        print("\nMenú:")
        print("1. Mostrar interfaces")
        print("2. Mostrar restconf")
        print("3. Obtener Banner")
        print("4. Cambiar banner")
        print("5. Configurar OSPF")
        print("6. Eliminar OSPF")
        print("7. Mostrar OSPF")
        print("8. Salir")
        option = int(input("Elija una opción: "))
        if option == 1:
            get_interfaces()
        elif option == 2:
            get_restconf_native()
        elif option == 3:
            get_banner()
        elif option == 4:
            datos_banner()
        elif option == 5:
            pedirdatos_OSPF()
        elif option == 6:
            delete_ospf()
        elif option == 7:
            show_ospf()
        elif option == 8:
            break
        else:
            print("Opción inválida. Intente de nuevo.")

def get_interfaces():
    module = "data/ietf-interfaces:interfaces"
    resp = requests.get(f'{api_url}{module}', auth=basicauth, headers=headers, verify=False)
    if resp.status_code == 200:
        data_json = resp.json()
        print(json.dumps(data_json, indent=4))
        for interface in data_json.get("ietf-interfaces:interfaces", {}).get("interface", []):
            print(f"Nombre de la interface: {interface.get('name')}")
            print(f"Descripción de la interface: {interface.get('description')}")
            print(f"Status de la interface: {interface.get('enabled')}\n")
    else:
        print(f'Error al realizar la consulta del modulo {module}')

def get_restconf_native():
    module = "data/Cisco-IOS-XE-native:native"
    resp = requests.get(f'{api_url}{module}', auth=basicauth, headers=headers, verify=False)
    if resp.status_code == 200:
        print(json.dumps(resp.json(), indent=4))
    else:
        print(f'Error al consumir la API para el modulo {module}')

def get_banner():
    module = "data/Cisco-IOS-XE-native:native/banner/motd"
    resp = requests.get(f'{api_url}{module}', auth=basicauth, headers=headers, verify=False)
    if resp.status_code == 200:
        print(json.dumps(resp.json(), indent=4))
    else:
        print(f'Error al consumir la API para el modulo {module}')

def datos_banner():
    banner = input("Ingresa el mensaje del banner: ")
    put_banner(banner)

def put_banner(banner):
    banner_data = {
        "Cisco-IOS-XE-native:motd": {
            "banner": banner
        }
    }
    module = "data/Cisco-IOS-XE-native:native/banner/motd"
    resp = requests.put(f'{api_url}{module}', data=json.dumps(banner_data), auth=basicauth, headers=headers, verify=False)
    if resp.status_code == 204:
        print("Actualizado exitoso")
    else:
        print(f"Error, no se puede realizar la actualizacion al modulo {module}")

def pedirdatos_OSPF():
    idproc = int(input("Ingresa el id del proceso: "))
    ip = input("Ingresa la dirección IP: ")
    wild = input("Ingresa la wildcard: ")
    area = int(input("Ingresa el área de OSPF: "))
    configure_ospf(idproc, ip, wild, area)

def configure_ospf(idproc, ip, wild, area):
    ospf_config = {
        "Cisco-IOS-XE-native:router": {
            "Cisco-IOS-XE-ospf:ospf": {
                "process-id": [
                    {
                        "id": idproc,
                        "network": [
                            {
                                "ip": ip,
                                "wildcard": wild,
                                "area": area
                            }
                        ]
                    }
                ]
            }
        }
    }
    module = "data/Cisco-IOS-XE-native:native/router"
    resp = requests.put(f'{api_url}{module}', data=json.dumps(ospf_config), auth=basicauth, headers=headers, verify=False)
    if resp.status_code == 204:
        print("Configuración de OSPF exitosa")
    else:
        print(f"Error, no se puede realizar la configuración en el módulo {module}")

def delete_ospf():
    idproc = int(input("Ingresa el id del proceso OSPF que deseas eliminar: "))
    module = f"data/Cisco-IOS-XE-native:native/router/ospf/process-id={idproc}"
    resp = requests.delete(f'{api_url}{module}', auth=basicauth, headers=headers, verify=False)
    if resp.status_code == 204:
        print(f"Proceso OSPF {idproc} eliminado exitosamente")
    else:
        print(f"Error al eliminar el proceso OSPF {idproc}")

def show_ospf():
    module = "data/Cisco-IOS-XE-native:native/router/ospf"
    resp = requests.get(f'{api_url}{module}', auth=basicauth, headers=headers, verify=False)
    if resp.status_code == 200:
        print(json.dumps(resp.json(), indent=4))
    else:
        print(f"Error al obtener la configuración OSPF")

if __name__ == '__main__':
    menu()
