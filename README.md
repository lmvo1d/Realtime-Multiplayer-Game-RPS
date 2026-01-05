# Multiplayer Rock-Paper-Scissors (Python)

A simple and fun **multiplayer Rock-Paper-Scissors game** built in Python using sockets. One player hosts the server and others can join as clients using the host's IP address.

---

## 🚀 Features

* Multiplayer gameplay over LAN
* Simple client-server architecture
* Real-time communication using Python sockets
* Lightweight and easy to run

---

## 📂 Project Structure

```
project-folder/
│
├── server.py
├── client.py
├── config.py
└── README.md
```

---

## ⚙️ Setup Instructions

Follow the steps below to run the game:

### **1. Get Your IP Address**

On the machine running the server:

* Open **Command Prompt**
* Run:

  ```bash
  ipconfig
  ```
* Copy the **IPv4 Address** (e.g., `192.168.1.5`)

### **2. Update the Config File**

Edit `config.py` and set the server IP address:

```python
SERVER_IP = "your_ipv4_here"
PORT = 5050  # or whichever port you choose
```

Make sure both server and clients use the same config.

### **3. Start the Server**

On the host machine:

```bash
python server.py
```

The server will start listening for client connections.

### **4. Start the Client(s)**

On each player’s machine:

```bash
python client.py
```

The game will connect to the server using the IP set in `config.py`.

---

## 🎮 How to Play

1. The server waits for players to join.
2. Each client enters their move (Rock, Paper, or Scissors).
3. The server compares moves and displays the result to all players.
4. Play continues until players exit.

---

## 📝 Requirements

* Python 3.8+

Install dependencies (if any):

```bash
pip install -r requirements.txt
```

(If your project doesn't use external libraries, you can remove this section.)

---

## 🤝 Contributing

Feel free to open issues or submit pull requests to improve the game.

---

## 📜 License

This project is licensed under the MIT License (or whichever license you choose).
