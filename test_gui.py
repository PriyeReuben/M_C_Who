from workhorse import Workhorse
# import PySimpleGUI as sg
#
# layout =[
#         [sg.Text('Enter Something:'), sg.Input(key = '-IN-')],
#         [sg.Text('Our output will go here:', key = '-OUT-')],
#         [sg.Button('OK'), sg.Button('Exit')]
#         ]
#
# window = sg.Window('Title Here', layout)
#
# while True:
#     event, values = window.read()
#     if event is None or event == 'Exit':
#         break
#     window['-OUT-'].update(values['-IN-'])
#
# window.close()

# import PySimpleGUI as sg
#
# sg.theme('DarkAmber')   # Add a touch of color
# # All the stuff inside your window.
# layout = [  [sg.Text('Some text on Row 1')],
#             [sg.Text('Enter something on Row 2'), sg.InputText()],
#             [sg.Button('Ok'), sg.Button('Cancel')],
#             [sg.Text('This is some text', font='Courier 12', text_color='blue', background_color='green')]]
#
# # Create the Window
# window = sg.Window('Window Title', layout)
# # Event Loop to process "events" and get the "values" of the inputs
# while True:
#     event, values = window.read()
#     if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
#         break
#     print('You entered ', values[0])
#
# window.close()
import PySimpleGUI as sg

#sg.theme('Topanga')
#sg.Titlebar("Custom Title")
use_custom_titlebar = True

layout = [
            [sg.Image(r'D:\Images\memes\yell at cloud.png')],
            [sg.Text()],
            [sg.Button(i) for i in range(1,7)]
        ]

window = sg.Window('M-C-Who?', layout)

events, values = window.read()
#window.close()
