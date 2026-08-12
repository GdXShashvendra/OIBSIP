import socket
import threading
import json

from database import (
    initialize_database,
    authenticate_user,
    register_user,
    create_room,
    get_rooms,
    save_message,
    get_message_history
)


HOST = "127.0.0.1"
PORT = 5555


clients = {}

clients_lock = threading.Lock()


# ============================================================
# SEND DATA
# ============================================================

def send_data(client, data):

    try:

        message = json.dumps(data)

        client.send(
            message.encode("utf-8")
        )

    except:

        pass


# ============================================================
# BROADCAST TO ROOM
# ============================================================

def broadcast_to_room(
    room,
    data,
    exclude=None
):

    with clients_lock:

        for client, info in list(
            clients.items()
        ):

            if info["room"] == room:

                if client != exclude:

                    send_data(
                        client,
                        data
                    )


# ============================================================
# HANDLE CLIENT
# ============================================================

def handle_client(client):

    username = None

    try:

        while True:

            data = client.recv(4096)

            if not data:

                break

            request = json.loads(
                data.decode("utf-8")
            )

            action = request.get(
                "action"
            )

            # ------------------------------------------------
            # REGISTER
            # ------------------------------------------------

            if action == "register":

                username = request[
                    "username"
                ]

                password = request[
                    "password"
                ]

                success, message = (
                    register_user(
                        username,
                        password
                    )
                )

                send_data(
                    client,
                    {
                        "type": "register_response",
                        "success": success,
                        "message": message
                    }
                )

            # ------------------------------------------------
            # LOGIN
            # ------------------------------------------------

            elif action == "login":

                username = request[
                    "username"
                ]

                password = request[
                    "password"
                ]

                success = authenticate_user(
                    username,
                    password
                )

                if success:

                    with clients_lock:

                        clients[
                            client
                        ] = {
                            "username": username,
                            "room": "General"
                        }

                    send_data(
                        client,
                        {
                            "type": "login_response",
                            "success": True
                        }
                    )

                    # Send rooms
                    send_data(
                        client,
                        {
                            "type": "rooms",
                            "rooms": get_rooms()
                        }
                    )

                    # Send General history
                    send_history(
                        client,
                        "General"
                    )

                    broadcast_to_room(
                        "General",
                        {
                            "type": "system",
                            "message":
                            f"{username} joined the chat."
                        },
                        exclude=client
                    )

                else:

                    send_data(
                        client,
                        {
                            "type": "login_response",
                            "success": False,
                            "message":
                            "Invalid username or password."
                        }
                    )

            # ------------------------------------------------
            # CREATE ROOM
            # ------------------------------------------------

            elif action == "create_room":

                room_name = request[
                    "room"
                ].strip()

                if room_name:

                    success = create_room(
                        room_name
                    )

                    send_data(
                        client,
                        {
                            "type":
                            "room_created",
                            "success":
                            success
                        }
                    )

                    send_data(
                        client,
                        {
                            "type": "rooms",
                            "rooms":
                            get_rooms()
                        }
                    )

            # ------------------------------------------------
            # JOIN ROOM
            # ------------------------------------------------

            elif action == "join_room":

                room = request[
                    "room"
                ]

                if client in clients:

                    old_room = clients[
                        client
                    ]["room"]

                    clients[
                        client
                    ]["room"] = room

                    send_history(
                        client,
                        room
                    )

                    broadcast_to_room(
                        room,
                        {
                            "type": "system",
                            "message":
                            f"{username} joined {room}."
                        },
                        exclude=client
                    )

            # ------------------------------------------------
            # SEND MESSAGE
            # ------------------------------------------------

            elif action == "message":

                message = request[
                    "message"
                ].strip()

                if not message:
                    continue

                if client not in clients:
                    continue

                room = clients[
                    client
                ]["room"]

                username = clients[
                    client
                ]["username"]

                timestamp = save_message(
                    room,
                    username,
                    message
                )

                data = {
                    "type": "message",
                    "username":
                    username,
                    "message":
                    message,
                    "timestamp":
                    timestamp
                }

                broadcast_to_room(
                    room,
                    data
                )

    except Exception as e:

        print(
            f"Client error: {e}"
        )

    finally:

        if client in clients:

            username = clients[
                client
            ]["username"]

            room = clients[
                client
            ]["room"]

            del clients[
                client
            ]

            broadcast_to_room(
                room,
                {
                    "type": "system",
                    "message":
                    f"{username} disconnected."
                }
            )

        client.close()


# ============================================================
# SEND HISTORY
# ============================================================

def send_history(
    client,
    room
):

    history = get_message_history(
        room
    )

    messages = []

    for username, message, timestamp in history:

        messages.append({

            "username": username,

            "message": message,

            "timestamp": timestamp
        })

    send_data(
        client,
        {
            "type": "history",
            "room": room,
            "messages": messages
        }
    )


# ============================================================
# START SERVER
# ============================================================

def start_server():

    initialize_database()

    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    server.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    server.bind(
        (HOST, PORT)
    )

    server.listen()

    print(
        "================================="
    )

    print(
        "Chat server started"
    )

    print(
        f"Listening on {HOST}:{PORT}"
    )

    print(
        "================================="
    )

    while True:

        client, address = server.accept()

        print(
            f"New connection: {address}"
        )

        thread = threading.Thread(
            target=handle_client,
            args=(client,),
            daemon=True
        )

        thread.start()


if __name__ == "__main__":

    start_server()