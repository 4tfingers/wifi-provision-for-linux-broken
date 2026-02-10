import os, subprocess, connect, re
import time
import sys
import hashlib
import binascii
from flask import Flask, render_template, request, jsonify

app = Flask(__name__, static_url_path='/static')

def reconfigure_wifi(interface='wlan1'):
    """
    Make wpa_supplicant reload its configuration file and reconnect.
    """
    # print(f"Attempting to reconfigure {interface}...") # for debug
    try:
        # Execute the wpa_cli command as root
        result = subprocess.run(
            ['sudo', 'wpa_cli', '-i', interface, 'reconfigure'],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        #print(f"wpa_cli reconfigure output: {result.stdout.strip()}") # for debug
        #print(f"Reconfiguration command sent. The Pi should connect to the new network shortly.") # for debug

        # Optional: Wait a few seconds and check the connection status maybe reducable
        time.sleep(5)

        """
        Checking the current IP address to verify connectivity.
        """
        try:
            # Use hostname -I or ip addr command to check IP (hostname -I is often simpler)
            ip_addr_result = subprocess.run(
                ['hostname', '-I'],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            ip_address = ip_addr_result.stdout.strip()
            if ip_address:
                # print(f"Successfully connected! IP Address: {ip_address}") # only uncomment for console debugging
                return "SSID Successfully set and connected!"
            else:
                # print("Connection status uncertain. No IP address found yet.") # for debug
                return "Connection status uncertain. No IP address found yet. Reboot Now"
        except subprocess.CalledProcessError:
            # print("Could not verify IP address.") # for debug
            return "Could not verify IP address."

    except subprocess.CalledProcessError as e:
        # print(f"Error executing wpa_cli: {e.stderr.strip()}") # for debug
        return "Error executing wpa_cli: {e.stderr.strip()}"
    except FileNotFoundError:
        # print("Error: wpa_cli command not found. Ensure wpasupplicant is installed.") # for debug
        return "Error: wpa_cli command not found. Ensure wpasupplicant is installed."
def get_ssids_manual(file_path='/etc/wpa_supplicant/wpa_supplicant-wlan1.conf.bak'):
    """
    Get a text list of all the SSIDS in the wpa_spplicant config file
    """
    ssids = []
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        # Use a regular expression to find all ssid entries
        ssids = re.findall(r'ssid\s*=\s*"([^"]+)"', content)
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.") # for debug
    except Exception as e:
        print(f"An error occurred: {e}") # for debug
    return ssids

def get_active_wifi_connection():
    """
    Scan for an active Wi-Fi connection and return the SSID.
    """
    connected_network = "Not Connected"
    # Get the currently connected network
    try:
        connected_response = subprocess.check_output(['/usr/sbin/iwgetid/iwgetid', '-r'], text=True)
        connected_network = connected_response.strip()
    except subprocess.CalledProcessError:
        print(f"An error occured running 'iwgetid' for active connection") # for debug
        pass

    return connected_network

def get_ssids(interface="wlan1"):
    """
    Runs the 'sudo iw dev <interface> scan' command, filters for SSIDs, and returns a list of unique SSIDs.
    """
    # The command to execute, using shell=True to handle the pipe
    command = f"sudo iw dev {interface} scan | grep SSID:"
    try:
        # Run the command and capture the output.
        # text=True ensures output is a string (instead of bytes).
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            shell=True,
            check=True
        )
        output = result.stdout

    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e.stderr}", file=sys.stderr) # for debug
        return []
    except FileNotFoundError:
        print("The 'iw' command was not found. Please ensure it is installed.", file=sys.stderr) # for debug
        return []

    # Process the output to extract SSIDs
    ssids = []
    for line in output.splitlines():
        try:
            ssid_name = line.split("SSID:")[1].strip()
            if ssid_name and ssid_name not in ssids:
                ssids.append(ssid_name)
        except IndexError:
            # Handle lines that might match "SSID:" but have no name
            continue
    return ssids

def generate_psk_pbkdf2(ssid, passphrase):
    """
    Generates the 256-bit PSK (hex string) from SSID and passphrase using PBKDF2.
    """
    # WPA/WPA2 uses PBKDF2 with HMAC-SHA1, 4096 iterations, and a 256-bit key length
    psk_bytes = hashlib.pbkdf2_hmac(
        'sha1',                   # Hash algorithm
        passphrase.encode('utf-8'), # Passphrase must be bytes
        ssid.encode('utf-8'),     # Salt (SSID) must be bytes
        4096,                     # Iterations
        32                        # Key length in bytes (256 bits)
    )
    # Convert the bytes to a hexadecimal string
    psk_hex = binascii.hexlify(psk_bytes).decode('utf-8')
    return psk_hex


@app.route('/', methods=['GET', 'POST'])
def landing():
    if request.method == "GET":
        # Create a list of discoverable AP's to populate the HTML select box
        #  dont really need to remove!
        time.sleep(1)
        connection = get_active_wifi_connection()
        time.sleep(1)
        wifi_list = get_ssids(interface="wlan1")
        time.sleep(1)
        # removing ownAP from the list - in my situation it's APzone
        if 'APzone' in wifi_list:
            wifi_list.remove('APzone')
        # removing currently connected AP from the list
        if connection in wifi_list:
            wifi_list.remove(connection)
        # read the current entries in the wpa_supplicant file and remove them!
        ssids_in_file = get_ssids_manual()
        time.sleep(1)
        set_ssids_in_file = set(ssids_in_file)
        filtered_ssids = [item for item in wifi_list if item not in set_ssids_in_file]
        if filtered_ssids:
            is_available = True
        else:
            is_available = False
        # to blank the results <div> in the form on page open
        results = ""
        # Pass the list of available SSIDS, current connection to the HTML template
        return render_template("index.html", ssid_list=filtered_ssids, conn=connection, results=results, is_available=is_available)


@app.route('/content', methods=['GET', 'POST'])
def content():
    if request.method == "POST":
        # Handle the json UTF-8 form problem
        if request.is_json:
            data = request.get_json()
            ssid = data.get('essid')
            epassword = data.get('epass')
        else:
            # Assumes standard form data
            ssid = request.form.get('essid')
            epassword = request.form.get('epass')
        # print(f"ssid: {ssid} plain_text_pass: {epassword}") # for debug
        # encrypt the plain text password to store in the conf
        password = generate_psk_pbkdf2(ssid, epassword)
        # print(f" ssid: {ssid} encryted_pass: {password}") # for debug
        """
        Use the connect.py code to manipulate the wpa_supplicant file
        """
        iface = os.popen('sudo ls /run/wpa_supplicant/', 'r')
        iface = iface.read()
        iface = iface.split('\n')
        clean_iface = list(filter(None, iface))
        scheme = connect.SchemeWPA(
            clean_iface[0],
            ssid,
            {"ssid": ssid, "psk": password}
        )
        #connection = get_active_wifi_connection()
        # scheme.save() # remove to debug all but write file
        # scheme.debugin() # print to console

        scheme.append()
        # Wait a 5 seconds before reconfiguring the connection
        time.sleep(5)
        results = reconfigure_wifi()
        # notify the HTML of the results
        return jsonify({'results': results})

if __name__ == "__main__":
    # app.run(host="172.18.0.1",port=80)
    app.run(host="0.0.0.0", port=80, debug=True)
