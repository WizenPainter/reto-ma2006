import PySimpleGUI as sg
import create_keypair as ckp
import schnorr_lib as sl
import os

def hashPDF(file, BLOCK_SIZE):
    # hash=sha256()
    with open(file, 'rb') as f: # Open the file to read it's bytes
        fb = f.read(BLOCK_SIZE) # Read from the file. Take in the amount declared above
        M = sl.sha256(fb)
    return M

def make_win1():

    layout = [[sg.Text('Escribir mail del destinatario')],
        [sg.Text('Mail: '), sg.InputText()],#[sg.T("")], 
        [sg.Text("Elegir el archivo: "), sg.Input(change_submits=True), sg.FileBrowse(key="-Archivo-")],
        [sg.Button("Generar firmas Schnorr"),sg.Button("Verificar Firma"), sg.Button('Salir')]]
    return sg.Window('Programa de Firmas Schnorr', layout, finalize=True)

def make_win2():

    layout = [[sg.Text('The second window')],
              [sg.Input(key='-IN-', enable_events=True)],
              [sg.Text(size=(25,1), k='-OUTPUT-')],
              [sg.Button('Erase'), sg.Button('Popup'), sg.Button('Exit')]]
    return sg.Window('Second Window', layout, finalize=True)


window1, window2 = make_win1(), None        # start off with 1 window open
while True:             # Event Loop
    window, event, values = sg.read_all_windows()
    if event == sg.WIN_CLOSED or event == 'Salir':
        window.close()
        if window == window2:       # if closing win 2, mark as closed
            window2 = None
        elif window == window1:     # if closing win 1, exit program
            break
    elif event == "Generar firmas Schnorr":
        size = os.path.getsize(values["-Archivo-"]) 
        user = ckp.create_keypair(1)["users"]
        M = hashPDF(values["-Archivo-"], size)
        sig = sl.schnorr_sign(M, user[0]["privateKey"])
        PubPublicKey = user[0]["publicKey"]
        Signature = sig.hex()

        sg.Popup("Clave Pública: ", PubPublicKey, "Firma: ", Signature)

    elif event == 'Verificar Firma' and not window2:
        window2 = make_win2()
    elif event == '-IN-':
        window['-OUTPUT-'].update(f'You enetered {values["-IN-"]}')
    elif event == 'Erase':
        window['-OUTPUT-'].update('')
        window['-IN-'].update('')
window.close()