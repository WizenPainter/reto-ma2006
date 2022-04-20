# img_viewer.py

# hello_psg.py

import PySimpleGUI as sg

sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
layout = [  [sg.Text('Escribir mail del destinatario')],
            [sg.Text('Mail: '), sg.InputText()],
            [sg.Button('Ok'), sg.Button('Cancel')],
            [sg.FileBrowse(key="-IN-")] ]

# Create the Window
window = sg.Window('Verificación Schnorr', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    print('You entered ', values[0])
    print(values["-IN-"])

window.close()