<h1 id="wifi-provision-for-linux">wifi-provision-for-linux</h1>
<p>This wifi-provision-for-linux is specifically designed to dynamically connect to a WiFi AP using the browser. </p>

<img src="https://i.imgur.com/kJrQWY1.png" alt="screenshot"  style="width:600px;" />

<h2 id="usage">Usage</h2>
<ol>
<li>Connect to Access point created by the Raspberry Pi.</li>
<li>Open up a browser and navigate to <a href="http://raspberrypi.local">http://raspberrypi.local</a></li>
<li>Select an available SSID from the select List</li>
<li>Fill up the <code>SSID</code> and the <code>psk</code>
<li>Click the connect button. Wait for some time(2-3 minutes). Pi will reload the wpa_supplicant itself and now it is good to go!</li>
</ol>

<h2 id="dependencies">Dependencies</h2>
<ul>
<li>Permissions for the Flask service</li>
<li> See the permissions.txt file!</li>
<li>Python 3.x</li>
<li><a href="https://pypi.org/project/wifi/">wifi</a></li>
<li><a href="https://pypi.org/project/Flask/">flask</a></li>
</ul>

<h2 id="howto">How to use</h2>
<ul>
<li>Navigate to the directory using <code>cd wifi-provision-for-linux</code></li>
<li>Run the command <code>sudo python main.py</code> </li>
</ul>
<p>You can set the server to auto-start on boot using <code>systemd</code>
<ul>
<li>Create a file called <code>server.service</code> for eg: using <code>cd sudo nano /lib/systemd/system/server.service</code></li>
<li>Add the following contents to the file </li>

<pre class=" language-bash"><code>[Unit]
 Description=WiFi conf server
 After=multi-user.target

 [Service]
 Type=idle
 ExecStart=/usr/bin/python3 /home/pi/wifi-provision-for-linux/main.py

 [Install]
 WantedBy=multi-user.target
</code></pre>

<li>Enable the service using <code>sudo systemctl enable server</code></li>
<li>Start the service using <code>sudo systemctl start server</code></li>
</ul>
 
