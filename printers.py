#!/usr/bin/python3

import os

printer_name = input("Выбор модели из предложенных вариантов:\n1.Brother5750\n2.Brother8690\n3.Xerox\nДля выхода из программы нажмите клавишу 'q'\n: ")
if printer_name == 'q':
    exit('До новых встреч!')

printer_ip = input("Введите ip-адрес принтера: ")

def printers(printer_name, printer_ip):
    if printer_name.lower() == '1':
        device = f"[devices]\n MFCL5750DW = http://{printer_ip}/WebServices/ScannerService, WSD"
        os.system(f"""
        apt-repo add "rpm http://alt-mirror.arm.loc drv/x86_64 drv"
        apt-get update && apt-get install mfcl5750dwlpr mfcl5750dwcupswrapper simple-scan -y
        lpadmin -p MFCL5750DW -E -v socket://{printer_ip} -m brother-MFCL5750DW-cups-en.ppd
        systemctl enable --now avahi-daemon
        """)
        return device
    
    if printer_name.lower() == '2':
        device = f"[devices]\n MFCL8690CDW = http://{printer_ip}/WebServices/ScannerService, WSD"
        lpr_rpm = "wget -P /home/master/ https://download.brother.com/welcome/dlf103215/mfcl8690cdwlpr-1.5.0-0.i386.rpm"
        cups_rpm = "wget -P /home/master/ https://download.brother.com/welcome/dlf103224/mfcl8690cdwcupswrapper-1.5.0-0.i386.rpm"
        os.system(f"""
        {lpr_rpm} 
        {cups_rpm}          
        rpm -ihv --nodeps /home/master/mfcl8690cdwlpr-1.5.0-0.i386.rpm
        rpm -ihv --nodeps /home/master/mfcl8690cdwcupswrapper-1.5.0-0.i386.rpm
        rpm -e --justdb mfcl8690cdwlpr mfcl8690cdwcupswrapper 
        apt-get install simple-scan -y
        lpadmin -p MFCL8690CDW -E -v socket://{printer_ip} -m lsb/usr/Brother/brother_mfcl8690cdw_printer_en.ppd
        systemctl enable --now avahi-daemon
        """)
        return device

    elif printer_name.lower() == '3':
        device = f"[devices]\n xerox = http://{printer_ip}/eSCL, eSCL"
        os.system(f"""
        apt-get install simple-scan -y
        lpadmin -p Xerox -E -v ipp://{printer_ip}/ipp/print -m everywhere
        systemctl enable --now avahi-daemon
        """)
        return device
    else:
        exit('Принтер выбран не верно!!')

options = "[options]\n discovery = disable \n protocol = manual"
config =(f"""
        # The following utility helps to discover scanners for manual
        # addition:
        #
        #   https://github.com/alexpevzner/airscan-discover

        {printers(printer_name, printer_ip)}
        
        {options}
        #model = network
        #ws-discovery = fast
        #socket_dir = /var/run
        """)
with open('/etc/sane.d/dll.d/hpaio','w') as hpaio:
    hpaio.write('#hpaio')
with open('/etc/sane.d/dll.d/hplip','w') as hplip:
    hplip.write('hplip')
with open('/etc/sane.d/airscan.conf','w') as airscan:
    airscan.write(config)
