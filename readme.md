# Projeto de Captura de E-mails e Vazamentos 🚨

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-2.3-green?logo=flask)
![Pyshark](https://img.shields.io/badge/Pyshark-1.0-orange)

Este projeto tem como objetivo **capturar e analisar tráfego de e-mails** para identificar possíveis vazamentos de dados. Foi desenvolvido utilizando Python, Flask, IBM Watsonx AI Studio e Pyshark.

---

## 🗂 Estrutura do Projeto

```
backend/
  └── app.py            # Backend da aplicação (API Flask)
frontend/
  └── public/           # Front-end (iniciar servidor aqui)
sniffer/
  ├── capture.py        # Script para captura de pacotes
  └── capturas/         # Logs de captura
```

---

## ⚙️ Pré-requisitos

* **Python 3.11**
* **Wireshark** (incluindo o **TShark**) [Download Wireshark](https://www.wireshark.org/download.html)
* Instalar dependências:

```bash
pip install -r requirements.txt
```

---

## 🚀 Como Rodar

### 1️⃣ Iniciar o front-end

```bash
cd frontend/public
python -m http.server 8000
```

> O front-end principal para enviar e-mails será acessível em `http://127.0.0.1:8000/`
> O front-end de análise estará acessível em `http://127.0.0.1:8000/analise.html`

### 2️⃣ Iniciar o back-end

```bash
cd backend
python app.py
```

> O back-end ficará escutando na porta definida no `app.py`.

### 3️⃣ Iniciar o sniffer

```bash
cd sniffer
python capture.py
```

> Ao iniciar, o script pedirá a placa de rede a ser monitorada. **Sempre selecione a loopback** (`localhost`).

---

## 📌 Observações

* Logs capturados pelo sniffer ficam em `sniffer/capturas`.
* Mantenha front-end e back-end rodando para a aplicação funcionar corretamente.
* É normal que o Pyshark solicite permissões ou placas de rede ao iniciar o capture.

---

## 🛠 Tecnologias Utilizadas

| Tecnologia            | Versão / Detalhes |
| --------------------- | ----------------- |
| Python                | 3.11              |
| Flask                 | 2.3               |
| Pyshark               | 1.0               |
| IBM Watsonx AI Studio | N/A               |
| HTML/CSS/JS           | Front-end         |
| TShark/Wireshark      | 4.x               |

---

## ✍️ Autores

* Erick Pereira Bastos
* Eliel Andrade Matos Godoy
* Edward Mevis da Silva
* Victor Rafael Ferreira de Roma
* Ana Luisa Augusto do Val
* Sarah Jandozza Laurindo