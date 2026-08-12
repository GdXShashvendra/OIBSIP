import socket
import threading
import json
import tkinter as tk
from tkinter import messagebox, simpledialog

from emoji_utils import convert_emojis


HOST = "127.0.0.1"
PORT = 5555


class ChatClient:

    def __init__(self):

        self.username = None

        self.current_room = "General"

        self.client = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        try:

            self.client.connect(
                (HOST, PORT)
            )

        except:

            messagebox.showerror(
                "Connection Error",
                "Could not connect to server."
            )

            return

        self.root = tk.Tk()

        self.root.title(
            "Chat Application"
        )

        self.root.geometry(
            "900x600"
        )

        self.show_login_screen()

        thread = threading.Thread(
            target=self.receive_messages,
            daemon=True
        )

        thread.start()

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.close
        )

        self.root.mainloop()


    # ========================================================
    # SEND DATA
    # ========================================================

    def send_data(self, data):

        try:

            message = json.dumps(data)

            self.client.send(
                message.encode("utf-8")
            )

        except:

            pass


    # ========================================================
    # LOGIN SCREEN
    # ========================================================

    def show_login_screen(self):

        self.clear_window()

        frame = tk.Frame(
            self.root
        )

        frame.pack(
            expand=True
        )

        tk.Label(
            frame,
            text="💬 Chat Application",
            font=(
                "Arial",
                25,
                "bold"
            )
        ).pack(
            pady=20
        )

        tk.Label(
            frame,
            text="Username"
        ).pack()

        self.username_entry = tk.Entry(
            frame,
            width=30
        )

        self.username_entry.pack(
            pady=5
        )

        tk.Label(
            frame,
            text="Password"
        ).pack()

        self.password_entry = tk.Entry(
            frame,
            width=30,
            show="*"
        )

        self.password_entry.pack(
            pady=5
        )

        tk.Button(
            frame,
            text="Login",
            width=20,
            command=self.login
        ).pack(
            pady=10
        )

        tk.Button(
            frame,
            text="Register",
            width=20,
            command=self.register
        ).pack()


    # ========================================================
    # LOGIN
    # ========================================================

    def login(self):

        username = (
            self.username_entry
            .get()
            .strip()
        )

        password = (
            self.password_entry
            .get()
        )

        if not username or not password:

            messagebox.showwarning(
                "Warning",
                "Enter username and password."
            )

            return

        self.send_data({

            "action": "login",

            "username": username,

            "password": password
        })


    # ========================================================
    # REGISTER
    # ========================================================

    def register(self):

        username = (
            self.username_entry
            .get()
            .strip()
        )

        password = (
            self.password_entry
            .get()
        )

        if not username or not password:

            messagebox.showwarning(
                "Warning",
                "Enter username and password."
            )

            return

        self.send_data({

            "action": "register",

            "username": username,

            "password": password
        })


    # ========================================================
    # CHAT SCREEN
    # ========================================================

    def show_chat_screen(self):

        self.clear_window()

        # ----------------------------------------------------
        # TOP BAR
        # ----------------------------------------------------

        top_frame = tk.Frame(
            self.root
        )

        top_frame.pack(
            fill="x",
            padx=10,
            pady=10
        )

        self.room_label = tk.Label(
            top_frame,
            text=f"Room: {self.current_room}",
            font=(
                "Arial",
                15,
                "bold"
            )
        )

        self.room_label.pack(
            side="left"
        )

        tk.Button(
            top_frame,
            text="Create Room",
            command=self.create_room
        ).pack(
            side="right"
        )

        # ----------------------------------------------------
        # MAIN FRAME
        # ----------------------------------------------------

        main_frame = tk.Frame(
            self.root
        )

        main_frame.pack(
            fill="both",
            expand=True
        )

        # ----------------------------------------------------
        # ROOM LIST
        # ----------------------------------------------------

        room_frame = tk.Frame(
            main_frame,
            width=150
        )

        room_frame.pack(
            side="left",
            fill="y",
            padx=5
        )

        tk.Label(
            room_frame,
            text="Rooms",
            font=(
                "Arial",
                12,
                "bold"
            )
        ).pack()

        self.room_list = tk.Listbox(
            room_frame,
            width=20
        )

        self.room_list.pack(
            fill="y",
            expand=True
        )

        self.room_list.bind(
            "<Double-Button-1>",
            self.join_selected_room
        )

        # ----------------------------------------------------
        # CHAT AREA
        # ----------------------------------------------------

        chat_frame = tk.Frame(
            main_frame
        )

        chat_frame.pack(
            side="right",
            fill="both",
            expand=True
        )

        self.chat_box = tk.Text(
            chat_frame,
            state="disabled",
            wrap="word",
            font=(
                "Arial",
                11
            )
        )

        self.chat_box.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

        # ----------------------------------------------------
        # MESSAGE AREA
        # ----------------------------------------------------

        input_frame = tk.Frame(
            chat_frame
        )

        input_frame.pack(
            fill="x"
        )

        self.message_entry = tk.Entry(
            input_frame,
            font=(
                "Arial",
                12
            )
        )

        self.message_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=5,
            pady=5
        )

        self.message_entry.bind(
            "<Return>",
            lambda event:
            self.send_message()
        )

        tk.Button(
            input_frame,
            text="Send",
            command=self.send_message
        ).pack(
            side="right",
            padx=5
        )


    # ========================================================
    # SEND MESSAGE
    # ========================================================

    def send_message(self):

        message = (
            self.message_entry
            .get()
            .strip()
        )

        if not message:

            return

        self.send_data({

            "action": "message",

            "message":
            message
        })

        self.message_entry.delete(
            0,
            tk.END
        )


    # ========================================================
    # CREATE ROOM
    # ========================================================

    def create_room(self):

        room = simpledialog.askstring(
            "Create Room",
            "Enter room name:"
        )

        if room:

            self.send_data({

                "action": "create_room",

                "room":
                room.strip()
            })


    # ========================================================
    # JOIN ROOM
    # ========================================================

    def join_selected_room(self, event=None):

        selection = (
            self.room_list
            .curselection()
        )

        if not selection:

            return

        room = self.room_list.get(
            selection[0]
        )

        self.current_room = room

        self.room_label.config(
            text=f"Room: {room}"
        )

        self.clear_chat()

        self.send_data({

            "action": "join_room",

            "room": room
        })


    # ========================================================
    # RECEIVE MESSAGES
    # ========================================================

    def receive_messages(self):

        while True:

            try:

                data = self.client.recv(
                    4096
                )

                if not data:

                    break

                message = json.loads(
                    data.decode("utf-8")
                )

                self.root.after(
                    0,
                    self.process_message,
                    message
                )

            except:

                break


    # ========================================================
    # PROCESS SERVER MESSAGE
    # ========================================================

    def process_message(self, data):

        message_type = data.get(
            "type"
        )

        # ----------------------------------------------------
        # LOGIN RESPONSE
        # ----------------------------------------------------

        if message_type == "login_response":

            if data["success"]:

                self.username = (
                    self.username_entry
                    .get()
                    .strip()
                )

                self.show_chat_screen()

            else:

                messagebox.showerror(
                    "Login Failed",
                    data.get(
                        "message",
                        "Login failed."
                    )
                )

        # ----------------------------------------------------
        # REGISTER RESPONSE
        # ----------------------------------------------------

        elif message_type == "register_response":

            if data["success"]:

                messagebox.showinfo(
                    "Success",
                    data["message"]
                )

            else:

                messagebox.showerror(
                    "Registration Failed",
                    data["message"]
                )

        # ----------------------------------------------------
        # ROOMS
        # ----------------------------------------------------

        elif message_type == "rooms":

            self.room_list.delete(
                0,
                tk.END
            )

            for room in data["rooms"]:

                self.room_list.insert(
                    tk.END,
                    room
                )

        # ----------------------------------------------------
        # HISTORY
        # ----------------------------------------------------

        elif message_type == "history":

            self.clear_chat()

            for message in data[
                "messages"
            ]:

                self.display_message(
                    message["timestamp"],
                    message["username"],
                    message["message"]
                )

        # ----------------------------------------------------
        # CHAT MESSAGE
        # ----------------------------------------------------

        elif message_type == "message":

            self.display_message(
                data["timestamp"],
                data["username"],
                data["message"]
            )

        # ----------------------------------------------------
        # SYSTEM MESSAGE
        # ----------------------------------------------------

        elif message_type == "system":

            self.display_system_message(
                data["message"]
            )

        # ----------------------------------------------------
        # ROOM CREATED
        # ----------------------------------------------------

        elif message_type == "room_created":

            if not data["success"]:

                messagebox.showerror(
                    "Room",
                    "Room already exists."
                )


    # ========================================================
    # DISPLAY MESSAGE
    # ========================================================

    def display_message(
        self,
        timestamp,
        username,
        message
    ):

        message = convert_emojis(
            message
        )

        formatted = (
            f"[{timestamp}] "
            f"{username}: "
            f"{message}\n"
        )

        self.chat_box.config(
            state="normal"
        )

        self.chat_box.insert(
            tk.END,
            formatted
        )

        self.chat_box.see(
            tk.END
        )

        self.chat_box.config(
            state="disabled"
        )


    # ========================================================
    # SYSTEM MESSAGE
    # ========================================================

    def display_system_message(
        self,
        message
    ):

        self.chat_box.config(
            state="normal"
        )

        self.chat_box.insert(
            tk.END,
            f"--- {message} ---\n"
        )

        self.chat_box.see(
            tk.END
        )

        self.chat_box.config(
            state="disabled"
        )


    # ========================================================
    # CLEAR CHAT
    # ========================================================

    def clear_chat(self):

        if hasattr(
            self,
            "chat_box"
        ):

            self.chat_box.config(
                state="normal"
            )

            self.chat_box.delete(
                "1.0",
                tk.END
            )

            self.chat_box.config(
                state="disabled"
            )


    # ========================================================
    # CLEAR WINDOW
    # ========================================================

    def clear_window(self):

        for widget in (
            self.root
            .winfo_children()
        ):

            widget.destroy()


    # ========================================================
    # CLOSE
    # ========================================================

    def close(self):

        try:

            self.client.close()

        except:

            pass

        self.root.destroy()


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    ChatClient()