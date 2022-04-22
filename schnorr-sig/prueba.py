import PySimpleGUI as sg
import create_keypair as ckp
import schnorr_lib as sl
import os
import json

def hashPDF(file, BLOCK_SIZE):
    # hash=sha256()
    with open(file, 'rb') as f: # Open the file to read it's bytes
        fb = f.read(BLOCK_SIZE) # Read from the file. Take in the amount declared above
        M = sl.sha256(fb)
    return M


sg.theme("DarkTeal2")
# layout = [[sg.Text('Escribir mail del destinatario')],
#         [sg.Text('Mail: '), sg.InputText()],#[sg.T("")], 
#         [sg.Text("Elegir el archivo: "), sg.Input(change_submits=True), sg.FileBrowse(key="-Archivo-")],
#         [sg.Button("Generar firmas Schnorr")],[sg.T("")],
#         [sg.Text('Inserta la Clave Pública (o agregada si se utilizó el esquema MuSig):')],
#         [sg.Input(key='-Clave-', enable_events=True)],
#         [sg.Text('Inserta la Firma Generada:')],
#         [sg.Input(key='-Firma-', enable_events=True)],
#         [sg.Button("Verificar Firma"), sg.Button("Salir")]]

layout = [[sg.Text('Escribir mail del destinatario')],
        [sg.Text('Mail: '), sg.InputText()],#[sg.T("")], 
        [sg.Text("Elegir el archivo: "), sg.Input(change_submits=True), sg.FileBrowse(key="-Archivo-")],
        [sg.Button("Generar firmas Schnorr")],[sg.T("")],
        [sg.Button("Verificar Firma"), sg.Button("Salir")]]

###Building Window
window = sg.Window('', layout, size=(800,350))

    
while True:
    event, values = window.read()
   
    if event in (sg.WIN_CLOSED, "Salir"):
        break
    elif event == "Generar firmas Schnorr":
        size = os.path.getsize(values["-Archivo-"]) 
        user = ckp.create_keypair(1)["users"]
        M = hashPDF(values["-Archivo-"], size)
        sig = sl.schnorr_sign(M, user[0]["privateKey"])
        PubPublicKey = user[0]["publicKey"]
        Signature = sig.hex()

        sg.Popup("Clave Pública: ", PubPublicKey, "Firma: ", Signature)
        datos = {'clave publica' : PubPublicKey,'firma' : Signature}
        # with open("mydocument.txt", mode = "w") as f:
        #     f.write("Clave Publica: " + PubPublicKey + "\nFirma: " + Signature)
        with open('json_data.json', 'w') as outfile:
            json.dump(datos, outfile, indent=2)

    elif event == "Verificar Firma":
        print(values['-Archivo-'])
        size = os.path.getsize(values['-Archivo-']) 
        M = hashPDF(values['-Archivo-'], size)
        # pubkey_bytes = bytes.fromhex(values["-Clave-"])
        # sig_bytes = bytes.fromhex(values["-Firma-"])
        with open('json_data.json', 'r') as f:
            data = json.load(f)
        pubkey_bytes = bytes.fromhex(data['clave publica'])
        sig_bytes = bytes.fromhex(data['firma'])
        result = sl.schnorr_verify(M, pubkey_bytes, sig_bytes)

        if result:
            sg.Popup("La firma es VALIDA para este mensaje y clave pública")
        else:
            sg.Popup("La firma no es VALIDA para este mensaje y clave pública")

