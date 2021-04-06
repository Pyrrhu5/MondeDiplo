# MondeDiplo

Download the last edition of _le monde diplomatique_ and add it to a Calibre's content server.

Calibre should be running with the content server enabled and a user set.

A legit subscription to the newspaper is required.

Only tested on Linux.

## Setup Calibre content server

```sh
sudo apt install -y calibre
```

**Setup users**
```sh
calibre-server --userdb <PATH TO USER DATABASE> --manage-users
```

**Service**

Replace the data in `< >`
```sh
echo"[Unit]
Description=Calibre Content Server
After=network.target

[Service]
Type=simple
User=<UNIX USER>
ExecStart=/usr/bin/calibre-server --userdb <PATH TO USER DATABASE> --enable-auth --port 8083 <EBOOKS LIBRARY PATH>
 
[Install]
WantedBy=default.target
" | sudo tee /etc/systemd/system/calibre-server.service 
```

```sh
sudo systemctl enable calibre-server 
sudo systemctl start calibre-server 
```

Calibre is now accessible from `localhost:8083`

## Installation

**Python**

Python version 3.6 or above

```bash
python3 --version
```

**Clone the repository**

Git is required
```bash
git --version
```

Clone it

**Virtual env**

Optional, but `Run.sh` assumes you have setup a virtual env as such:

```bash
python3 -m venv venv
```

**Dependencies**

Activate the virtual env first:
```bash
source ./venv/bin/activate
```

Install dependencies:

```bash
pip3 install -r requirements.txt
```

**Executable**

Allows execution of entry point (not needed for Windows)
```bash
chmod +x MondeDiplo.py
```
or, if using the virtual env
```bash
chmod +x Run.sh
```

**Crontab**

Get it every 5th of each month.
```
00 04 5 * * <install path>/mondediplo/Run.sh >> <where you want the logs>/mondediplo.log
```

## Update

```bash
git pull
```


## License
Unmodified [MIT license](https://opensource.org/licenses/MIT)

See `License.md`
