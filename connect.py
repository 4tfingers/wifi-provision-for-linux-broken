import re
from wifi import Cell, Scheme
import wifi.subprocess_compat as subprocess
from wifi.utils import ensure_file_exists

# might be useful in editing the wpa_supplicant file but is unused atm
#from wpasupplicantconf import WpaSupplicantConf
# for this must run...
# pip install wpasupplicantconf


class SchemeWPA(Scheme):

    def __init__(self, interface, name, country, options=None):
        self.interface = interface
        self.interfaces = "/etc/wpa_supplicant/wpa_supplicant-" + interface + ".conf.bak"
        self.name = name
        self.options = options or {}

    def __stra__(self):
        options = ''.join("\n    {k}=\"{v}\"".format(k=k, v=v) for k, v in self.options.items())
        return "country=" + country + "\n" + "update_config=1" + "\n" + "ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev" + "\n" + "network={" +" + options + "\n    mode=0" + "\n}\n"

    def __str__(self):
        for option_name, option_value in self.options.items():
               if option_name == 'ssid':
                   ssid = option_value
               if option_name == 'psk':
                   psk = option_value

        config_lines = [
            '\n',
            'network={',
            f'\tssid="{ssid}"',
            '\tscan_ssid=1',
            '\tkey_mgmt=WPA-PSK',
            f'\tpsk={psk}'
            '}'
        ]
        # print(config_lines) # for debug
        return "\n".join(config_lines)

    def __repr__(self):
        return 'Scheme(interface={interface!r}, name={name!r}, options={options!r}'.format(**vars(self))

    def save(self):
        """
        OverWrites the configuration to the :attr:`interfaces` file.
        """
        if not self.find(self.interface, self.name):
            with open(self.interfaces, 'w') as f:
                f.write('\n')
                f.write(str(self))

    def append(self):
        """
        OverWrites the configuration to the :attr:`interfaces` file.
        """
        try:
            if not self.find(self.interface, self.name):
                with open(self.interfaces, 'a') as f:
                    f.write('\n')
                    f.write(str(self))
            else:
                # Code to execute if the item IS found
                print(f"{self.name} already exists.") # need code for removing existing networks in wpa_supplicant!!!!!
        except:
            # print(f"start// \n" + str(self) + "\n" + str(self.interface) + "\n" + str(self.name) + "\n //end")
            print("A find open or write exception occurred")
    def debugin(self):
        """
        Output the file contents to console
        """
        print(f"start// \n" + str(self) + "\n //end")

    def old_get_wifi_networks(self):
        try:
            with open(self.interfaces, 'r') as file:
                lines = file.readlines()
            wpa_conf = WpaSupplicantConf(lines)
            networks = wpa_conf.networks()
            return list(networks.values())
        except Exception as e:
            print(f"Error parsing file: {e}")
            return None
