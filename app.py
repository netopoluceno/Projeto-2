import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
from mensagens import mensagens
import os
import base64
import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText

class LoveApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Love App')
        
        self.label_nivel = tk.Label(root, text="Que tipo de mensagem vamos enviar hoje?", font=("Helvetica", 10, "bold"))
        self.label_nivel.pack(pady=10)
        
        self.niveis = ['Cantada', 'Romântica', 'Gif de Vó']
        self.nivel_var = tk.StringVar(value=self.niveis[0])
        self.combobox_nivel = ttk.Combobox(root, textvariable=self.nivel_var, values=self.niveis, state='readonly')
        self.combobox_nivel.pack(pady=10)
        
        # Botão para Enviar por WhatsApp
        self.botao_exportar = tk.Button(root, text="Enviar por WhatsApp", command=self.enviar_whatsapp)
        self.botao_exportar.pack(pady=20)

        # Botão para Enviar por E-mail
        self.botao_enviar_email = tk.Button(root, text="Enviar por E-mail", command=self.enviar_email)
        self.botao_enviar_email.pack(pady=20)

    def mostrar_mensagem(self):
        pass

    def enviar_whatsapp(self):
        pass

    def enviar_email(self):
        SCOPES = ['https://www.googleapis.com/auth/gmail.send']
        creds = None

        # O arquivo token.json armazena os tokens de acesso e atualização do usuário
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
        # Se não há credenciais válidas disponíveis, permita que o usuário faça login.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Salve as credenciais para a próxima execução
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        try:
            # Construa o serviço da API do Gmail
            service = build('gmail', 'v1', credentials=creds)

            destinatario = simpledialog.askstring("Destinatário", "Digite o endereço de e-mail do destinatário:")
            if not destinatario:
                return

            assunto = "Teste"
            corpo = "Testando"

            # Crie a mensagem de e-mail
            message = MIMEText(corpo)
            message['to'] = destinatario
            message['from'] = "edprojetospython@gmail.com"
            message['subject'] = assunto
            raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

            # Envie a mensagem
            message = service.users().messages().send(userId="me", body={'raw': raw}).execute()
            messagebox.showinfo("Sucesso", "E-mail enviado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível enviar o e-mail: {e}")
            print(f"Erro: {e}")

# Iniciar o aplicativo
if __name__ == "__main__":
    root = tk.Tk()
    app = LoveApp(root)
    root.mainloop()

