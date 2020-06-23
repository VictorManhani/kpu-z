__author__ = 'Victor Gomes Manhani'

from kivy.clock import Clock
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.core.window import Window
Window.size = [500, 500]

import subprocess
import sys

class Home(Factory.MDBoxLayout):
    md_bg_color = [.2,.5,.9,1]

    def __init__(self, *args, **kwargs):
        super(Home, self).__init__(*args, **kwargs)
        Clock.schedule_once(self.start, 1)
    
    # get the command and sanitize the return
    def get_command(self, text):
        text = subprocess.check_output(text).decode().split('\n')[1].strip()
        if text == None:
            text = ''
        return text

    def start(self, evt):
        container = self.ids.container
        plat = sys.platform.lower()

        if 'win' in plat:
            # current_machine_id = subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip()
            manufacturer = self.get_command('wmic baseboard get Manufacturer')
            product = self.get_command('wmic baseboard get product')
            version = self.get_command('wmic baseboard get version')
            serialnumber = self.get_command('wmic baseboard get serialnumber')
            cpu_name = self.get_command('wmic cpu get name')
            max_clock_speed = self.get_command('wmic cpu get MaxClockSpeed')
            socket_designation = self.get_command('wmic cpu get SocketDesignation')
            caption = self.get_command('wmic cpu get Caption')
            ram = self.get_command('wmic MEMPHYSICAL get MaxCapacity')
            vga = self.get_command('wmic path win32_VideoController get name')
            resolution = self.get_command('wmic path win32_VideoController get VideoModeDescription')
            hardrive = self.get_command('wmic DISKDRIVE get Caption')
            system_type = self.get_command('wmic OS get Caption')
            os_architecture = self.get_command('wmic OS get OSArchitecture')
            version = self.get_command('wmic OS get Version')
        elif 'lin' in plat:
            manufacturer = self.get_command('dmidecode -t baseboard | grep manufacturer')
            product = self.get_command('dmidecode -t baseboard | grep product')
            version = self.get_command('dmidecode -t baseboard | grep version')
            serialnumber = self.get_command('dmidecode -t baseboard | grep serialnumber')
            # cpu_name = self.get_command('lscpu | grep processor')

        infos = {
            'Manufacturer': manufacturer, 
            'Product': product, 'Version': version, 
            'Serial Number': serialnumber, 'Cpu Name': cpu_name, 
            'Max Clock Speed': f'{float(max_clock_speed) / 1000:.2f} Ghz',
            'Socket Designation': socket_designation, 'Caption': caption, 
            'Ram': ram, 'Vga': vga, 'Resolution': resolution, 
            'Hardrive': hardrive, 'OS': system_type, 
            'Os Architeture': os_architecture, 'Version': version}

        for info in infos:
            label = f"""
BoxLayout:
    size_hint: [1, None]
    height: 60
    spacing: dp(10)
    Label:
        text: '{info}'
        size_hint: [.2, 1]
        font_size: sp(self.size[0] / 9 + 3)
        text_size: self.size
        halign: 'center'
        valign: 'middle'
        color: [.9,.9,.9,1]
        canvas.before:
            Color:
                rgba: [.4,.4,.4,1]
            RoundedRectangle:
                pos: self.pos
                size: self.size
    TextInput:   
        hint_text: '{info}'
        text: '{infos[info]}'
        text_color: [1,0,0,1]
        color: [1,1,1,1]
        halign: 'center'
        size_hint: [.7, 1]
        font_size: sp(self.size[0] / 22 + 3)
        readonly: True
    Button:
        text: 'c'
        font_size: sp(self.size[0] / 3 + 3)
        select: False
        size_hint: [.1, 1]
        background_normal: ''
        background_color: [.4,.4,.4,1] if not self.select else [.2,.5,.2,1]
        on_release:
            Clipboard.copy(self.parent.children[1].text)
            self.select = True
"""

            label = Builder.load_string(label)
            container.add_widget(label)

# get all in the cmd
# echo --------------- & wmic cpu get name & wmic MEMPHYSICAL get MaxCapacity & wmic baseboard get product & wmic baseboard get version & wmic bios get SMBIOSBIOSVersion & wmic path win32_VideoController get name & wmic path win32_VideoController get DriverVersion & wmic path win32_VideoController get VideoModeDescription & wmic OS get Caption,OSArchitecture,Version & wmic DISKDRIVE get Caption && echo ---------------

class MainApp(MDApp):
    def build(self):
        self.title = "KPU-Z"
        self.theme_cls.theme_style = "Light"

        return Builder.load_string("""
#:import Clipboard kivy.core.clipboard.Clipboard

Home:
    ScrollView:
        MDBoxLayout:
            id: container
            orientation: "vertical"
            padding: dp(10)
            spacing: dp(10)
            size_hint: [1, None]
            height: self.minimum_height
""")

MainApp().run()