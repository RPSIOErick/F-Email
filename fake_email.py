import os
from ibm_watsonx_ai import APIClient, Credentials
import getpass
from ibm_watsonx_ai.foundation_models import ModelInference

from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY")
project_id = os.getenv("PROJ_ID")
space_id = os.getenv("SPACE_ID")

credentials = Credentials(
    url="https://ca-tor.ml.cloud.ibm.com",
    api_key=api_key
)

model_id = "ibm/granite-3-8b-instruct"

parameters = {
    "decoding_method": "greedy",
    "max_new_tokens": 1000,
    "min_new_tokens": 200,
    "repetition_penalty": 1
}

project_id = os.getenv("PROJECT_ID")
space_id = os.getenv("SPACE_ID")


model = ModelInference(
	model_id = model_id,
	params = parameters,
	credentials = credentials,
	project_id = project_id,
	space_id = space_id
	)

prompt_input = """Você é um agente de segurança capaz de ler logs e retornar relatórios que informam se há vazamentos ou não.

Entrada: 📦 EMAIL CAPTURADO [2025-08-24 16:05:12]
Origem: 192.168.0.14:60312
Destino: 10.0.0.5:5000
De: ti@empresa.com
Para: sup@corp.com
Conteúdo:
Segue acesso VPN: usuario=admin senha=1234Segura!
--------------------------------------------------
📦 EMAIL CAPTURADO [2025-08-24 16:06:47]
Origem: 192.168.0.22:60344
Destino: 10.0.0.5:5000
De: financeiro@corp.com
Para: auditoria@corp.com
Conteúdo:
Relatório ok. Cartão testado: 4111 1111 1111 1111 - validade 12/29
--------------------------------------------------
📦 EMAIL CAPTURADO [2025-08-24 16:07:05]
Origem: 192.168.0.14:60361
Destino: 10.0.0.5:5000
De: ti@empresa.com
Para: cloud@provider.com
Conteúdo:
Chave API exposta: AKIAIOSFODNN7EXAMPLE
--------------------------------------------------
📦 EMAIL CAPTURADO [2025-08-24 16:08:33]
Origem: 192.168.0.35:60402
Destino: 10.0.0.5:5000
De: suporte@corp.com
Para: cliente@gmail.com
Conteúdo:
Confirmação de atendimento. Nada sensível aqui.
--------------------------------------------------
📦 EMAIL CAPTURADO [2025-08-24 16:09:01]
Origem: 192.168.0.22:60414
Destino: 10.0.0.5:5000
De: financeiro@corp.com
Para: pagamentos@corp.com
Conteúdo:
Conta bancária para depósito: Agência 1234, Conta 56789-0
--------------------------------------------------
📦 EMAIL CAPTURADO [2025-08-24 16:09:58]
Origem: 192.168.0.14:60444
Destino: 10.0.0.5:5000
De: ti@empresa.com
Para: admin@corp.com
Conteúdo:
Credencial root: root:toor
--------------------------------------------------

Saída: 📌 Última verificação: 4 de 6 pacotes possuem dados vazados → 66,6%

📈 IP que mais vazou informações:
- 192.168.0.14 → 3 ocorrências
   - ti@empresa.com → Envio de credenciais e chave de API

- 192.168.0.22 → 2 ocorrências
   - financeiro@corp.com → Envio de cartão de crédito e dados bancários

✅ IP com menor risco:
- 192.168.0.35 → Nenhum dado sensível detectado

🔎 Tipos de vazamento detectados:
- Credenciais expostas (usuário/senha) → 2 pacotes
- Dados financeiros (cartão/conta bancária) → 2 pacotes
- Chaves de API → 1 pacote

💡 Resumo:
O maior risco vem do IP 192.168.0.14, que enviou informações sensíveis de TI.  
Recomenda-se auditoria imediata e revisão de acessos, além de validação das contas bancárias e cartões informados.


Entrada: 📦 EMAIL CAPTURADO [2025-08-24 17:10:05]
Origem: 10.0.0.12:61012
Destino: 10.0.0.5:5000
De: alice@empresa.com
Para: ti@empresa.com
Conteúdo:
Login VPN: alice.vpn | senha: Teste123!
--------------------------------------------------
📦 EMAIL CAPTURADO [2025-08-24 17:11:33]
Origem: 10.0.0.25:61144
Destino: 10.0.0.5:5000
De: financeiro@corp.com
Para: auditoria@corp.com
Conteúdo:
Cartão teste: 5555 4444 3333 2222, validade 11/28, CVV 456
--------------------------------------------------
📦 EMAIL CAPTURADO [2025-08-24 17:12:51]
Origem: 10.0.0.12:61045
Destino: 10.0.0.5:5000
De: alice@empresa.com
Para: cloud@provider.com
Conteúdo:
Chave API temporária: AKIA_TESTE_EXEMPLO_123
--------------------------------------------------
📦 EMAIL CAPTURADO [2025-08-24 17:14:10]
Origem: 10.0.0.33:61202
Destino: 10.0.0.5:5000
De: suporte@corp.com
Para: cliente@gmail.com
Conteúdo:
Atendimento finalizado. Sem dados sensíveis.
--------------------------------------------------
📦 EMAIL CAPTURADO [2025-08-24 17:15:27]
Origem: 10.0.0.25:61170
Destino: 10.0.0.5:5000
De: financeiro@corp.com
Para: pagamentos@corp.com
Conteúdo:
Conta bancária para depósito: Agência 4321, Conta 98765-0
--------------------------------------------------
📦 EMAIL CAPTURADO [2025-08-24 17:16:58]
Origem: 10.0.0.12:61088
Destino: 10.0.0.5:5000
De: alice@empresa.com
Para: admin@corp.com
Conteúdo:
Credencial root temporária: root:TempRoot2025!
--------------------------------------------------

Saída: 📌 Última verificação: 4 de 6 pacotes possuem dados vazados → 66,6%

📈 IP que mais vazou informações:
- 10.0.0.12 → 3 ocorrências
   - alice@empresa.com → Envio de credenciais e chave de API

- 10.0.0.25 → 2 ocorrências
   - financeiro@corp.com → Envio de cartão de crédito e dados bancários

✅ IP com menor risco:
- 10.0.0.33 → Nenhum dado sensível detectado

🔎 Tipos de vazamento detectados:
- Credenciais expostas (usuário/senha) → 2 pacotes
- Dados financeiros (cartão/conta bancária) → 2 pacotes
- Chaves de API → 1 pacote

💡 Resumo:
O maior risco identificado é o IP 10.0.0.12, que enviou informações de acesso e chaves de API.  
Recomenda-se auditoria imediata nos usuários listados e validação dos acessos expostos, além de revisar pagamentos e dados bancários enviados.


Entrada: 📦 EMAIL CAPTURADO [2025-08-24 18:05:12]
Origem: 10.0.0.45:61412
Destino: 10.0.0.5:5000
De: joao@empresa.com
Para: maria@empresa.com
Conteúdo:
Segue o relatório da reunião de hoje. Todos os pontos foram discutidos.
--------------------------------------------------
📦 EMAIL CAPTURADO [2025-08-24 18:06:33]
Origem: 10.0.0.52:61544
Destino: 10.0.0.5:5000
De: suporte@empresa.com
Para: cliente@gmail.com
Conteúdo:
Atendimento finalizado com sucesso. Nenhuma ação adicional necessária.
--------------------------------------------------
📦 EMAIL CAPTURADO [2025-08-24 18:07:51]
Origem: 10.0.0.33:61602
Destino: 10.0.0.5:5000
De: rh@empresa.com
Para: equipe@empresa.com
Conteúdo:
Convite para o treinamento de segurança na próxima terça-feira às 14h.
--------------------------------------------------
📦 EMAIL CAPTURADO [2025-08-24 18:09:27]
Origem: 10.0.0.61:61770
Destino: 10.0.0.5:5000
De: administrativo@empresa.com
Para: fornecedores@empresa.com
Conteúdo:
Pedido #4521 confirmado. Entrega prevista para 28/08.
--------------------------------------------------
📦 EMAIL CAPTURADO [2025-08-24 18:10:58]
Origem: 10.0.0.44:61888
Destino: 10.0.0.5:5000
De: marketing@empresa.com
Para: equipe@empresa.com
Conteúdo:
Lembrete: reunião de alinhamento do projeto às 16h. Não há anexos sensíveis.
--------------------------------------------------

Saída: 📌 Última verificação: 0 de 5 pacotes possuem dados vazados → 0%

📈 IPs analisados:
- 10.0.0.45 → joao@empresa.com → Nenhum dado sensível detectado
- 10.0.0.52 → suporte@empresa.com → Nenhum dado sensível detectado
- 10.0.0.33 → rh@empresa.com → Nenhum dado sensível detectado
- 10.0.0.61 → administrativo@empresa.com → Nenhum dado sensível detectado
- 10.0.0.44 → marketing@empresa.com → Nenhum dado sensível detectado

🔎 Tipos de vazamento detectados:
- Nenhum

💡 Resumo:
Todos os pacotes analisados estão limpos. Não há vazamentos de credenciais, dados financeiros ou informações pessoais.


Entrada: 📦 EMAIL CAPTURADO [2025-08-24 19:05:12]
Origem: 10.0.0.12:62012
Destino: 10.0.0.5:5000
De: alice@empresa.com
Para: ti@empresa.com
Conteúdo:
Login VPN: alice.vpn | senha: Teste123!
--------------------------------------------------
📦 EMAIL CAPTURADO [2025-08-24 19:06:33]
Origem: 10.0.0.35:62144
Destino: 10.0.0.5:5000
De: suporte@corp.com
Para: cliente@gmail.com
Conteúdo:
Atendimento finalizado. Nenhuma ação adicional necessária.
--------------------------------------------------
📦 EMAIL CAPTURADO [2025-08-24 19:07:51]
Origem: 10.0.0.25:62202
Destino: 10.0.0.5:5000
De: financeiro@corp.com
Para: auditoria@corp.com
Conteúdo:
Cartão teste: 5555 4444 3333 2222, validade 11/28, CVV 456
--------------------------------------------------
📦 EMAIL CAPTURADO [2025-08-24 19:09:27]
Origem: 10.0.0.52:62370
Destino: 10.0.0.5:5000
De: rh@empresa.com
Para: equipe@empresa.com
Conteúdo:
Convite para o treinamento de segurança na próxima terça-feira às 14h.
--------------------------------------------------
📦 EMAIL CAPTURADO [2025-08-24 19:10:58]
Origem: 10.0.0.12:62088
Destino: 10.0.0.5:5000
De: alice@empresa.com
Para: admin@corp.com
Conteúdo:
Credencial root temporária: root:TempRoot2025!
--------------------------------------------------
📦 EMAIL CAPTURADO [2025-08-24 19:12:15]
Origem: 10.0.0.33:62402
Destino: 10.0.0.5:5000
De: administrativo@empresa.com
Para: fornecedores@empresa.com
Conteúdo:
Pedido #4522 confirmado. Entrega prevista para 29/08.
--------------------------------------------------
Saída: 📌 Última verificação: 3 de 6 pacotes possuem dados vazados → 50%

📈 IP que mais vazou informações:

- 10.0.0.12 → 2 ocorrências
   - alice@empresa.com →
       - Login VPN: alice.vpn | senha: Teste123!
       - Credencial root temporária: root:TempRoot2025!

- 10.0.0.25 → 1 ocorrência
   - financeiro@corp.com →
       - Cartão teste: 5555 4444 3333 2222, validade 11/28, CVV 456

✅ IPs sem dados sensíveis:
- 10.0.0.35 → suporte@corp.com
- 10.0.0.52 → rh@empresa.com
- 10.0.0.33 → administrativo@empresa.com

🔎 Tipos de vazamento detectados:
- Credenciais expostas → 2 pacotes
- Dados financeiros (cartão de crédito) → 1 pacote

💡 Resumo:
Metade dos emails analisados contém dados sensíveis.  
O IP 10.0.0.12 representa o maior risco, com envio de credenciais detalhadas: VPN e root.  
O IP 10.0.0.25 expôs um cartão de crédito de teste.  
Recomenda-se auditoria imediata nos usuários listados e revisão de acesso a sistemas críticos.

Entrada: 📦 EMAIL CAPTURADO [2025-08-24 20:05:12]
Origem: 10.0.0.11:63012
Destino: 10.0.0.5:5000
De: carla@empresa.com
Para: ti@empresa.com
Conteúdo:
Acesso ao servidor: usuario=carla_admin | senha: Carla2025!
--------------------------------------------------
📦 EMAIL CAPTURADO [2025-08-24 20:06:33]
Origem: 10.0.0.22:63144
Destino: 10.0.0.5:5000
De: suporte@corp.com
Para: cliente@gmail.com
Conteúdo:
Atendimento finalizado. Sem informações sensíveis.
--------------------------------------------------
📦 EMAIL CAPTURADO [2025-08-24 20:07:51]
Origem: 10.0.0.33:63202
Destino: 10.0.0.5:5000
De: financeiro@corp.com
Para: auditoria@corp.com
Conteúdo:
Cartão teste: 4111 2222 3333 4444, validade 09/27, CVV 789
--------------------------------------------------
📦 EMAIL CAPTURADO [2025-08-24 20:09:27]
Origem: 10.0.0.44:63370
Destino: 10.0.0.5:5000
De: rh@empresa.com
Para: equipe@empresa.com
Conteúdo:
Convite para reunião de alinhamento de projeto na sexta-feira.
--------------------------------------------------
📦 EMAIL CAPTURADO [2025-08-24 20:10:58]
Origem: 10.0.0.11:63088
Destino: 10.0.0.5:5000
De: carla@empresa.com
Para: admin@corp.com
Conteúdo:
Credencial root temporária: root:TempCarla2025!
--------------------------------------------------
📦 EMAIL CAPTURADO [2025-08-24 20:12:15]
Origem: 10.0.0.55:63402
Destino: 10.0.0.5:5000
De: administrativo@empresa.com
Para: fornecedores@empresa.com
Conteúdo:
Pedido #4523 confirmado. Entrega prevista para 30/08.
--------------------------------------------------

Saída: 📌 Última verificação: 3 de 6 pacotes possuem dados vazados → 50%

📈 IP que mais vazou informações:

- 10.0.0.11 → 2 ocorrências
   - carla@empresa.com →
       - Acesso ao servidor: usuario=carla_admin | senha: Carla2025!
       - Credencial root temporária: root:TempCarla2025!

- 10.0.0.33 → 1 ocorrência
   - financeiro@corp.com →
       - Cartão teste: 4111 2222 3333 4444, validade 09/27, CVV 789

✅ IPs sem dados sensíveis:
- 10.0.0.22 → suporte@corp.com
- 10.0.0.44 → rh@empresa.com
- 10.0.0.55 → administrativo@empresa.com

🔎 Tipos de vazamento detectados:
- Credenciais expostas (usuario/senha/root) → 2 pacotes
- Dados financeiros (cartão de crédito) → 1 pacote

💡 Resumo:
Metade dos emails analisados contém dados sensíveis.  
O IP 10.0.0.11 representa o maior risco, com envio de credenciais detalhadas: acesso ao servidor e root temporário.  
O IP 10.0.0.33 expôs um cartão de crédito de teste.  
Recomenda-se auditoria imediata nos usuários listados e revisão de acesso a sistemas críticos.


Entrada: 📦 EMAIL CAPTURADO [2025-08-24 21:10:05]
Origem: 10.0.0.15:64012
Destino: 10.0.0.5:5000
De: bruno@empresa.com
Para: ti@empresa.com
Conteúdo:
Acesso SSH: bruno_ssh | senha: Bruno2025!
--------------------------------------------------
📦 EMAIL CAPTURADO [2025-08-24 21:11:33]
Origem: 10.0.0.26:64144
Destino: 10.0.0.5:5000
De: suporte@corp.com
Para: cliente@gmail.com
Conteúdo:
Atendimento encerrado. Todas as informações seguras.
--------------------------------------------------
📦 EMAIL CAPTURADO [2025-08-24 21:12:51]
Origem: 10.0.0.37:64202
Destino: 10.0.0.5:5000
De: financeiro@corp.com
Para: auditoria@corp.com
Conteúdo:
Cartão de teste: 5555 6666 7777 8888, validade 10/28, CVV 123
--------------------------------------------------
📦 EMAIL CAPTURADO [2025-08-24 21:14:10]
Origem: 10.0.0.48:64370
Destino: 10.0.0.5:5000
De: rh@empresa.com
Para: equipe@empresa.com
Conteúdo:
Reunião de alinhamento marcada para quinta-feira às 15h.
--------------------------------------------------
📦 EMAIL CAPTURADO [2025-08-24 21:15:27]
Origem: 10.0.0.15:64088
Destino: 10.0.0.5:5000
De: bruno@empresa.com
Para: admin@corp.com
Conteúdo:
Senha root temporária: root:TempBruno2025!
--------------------------------------------------
📦 EMAIL CAPTURADO [2025-08-24 21:16:58]
Origem: 10.0.0.59:64402
Destino: 10.0.0.5:5000
De: administrativo@empresa.com
Para: fornecedores@empresa.com
Conteúdo:
Pedido #4524 confirmado. Entrega prevista para 31/08.
--------------------------------------------------

Saída:  📌 Última verificação: 3 de 6 pacotes possuem dados vazados → 50%

📈 IP que mais vazou informações:

- 10.0.0.15 → 2 ocorrências
   - bruno@empresa.com →
       - Acesso SSH: bruno_ssh | senha: Bruno2025!
       - Senha root temporária: root:TempBruno2025!

- 10.0.0.37 → 1 ocorrência
   - financeiro@corp.com →
       - Cartão de teste: 5555 6666 7777 8888, validade 10/28, CVV 123

✅ IPs sem dados sensíveis:
- 10.0.0.26 → suporte@corp.com
- 10.0.0.48 → rh@empresa.com
- 10.0.0.59 → administrativo@empresa.com

🔎 Tipos de vazamento detectados:
- Credenciais expostas (usuario/senha/root) → 2 pacotes
- Dados financeiros (cartão de crédito) → 1 pacote

💡 Resumo:
Metade dos emails analisados contém dados sensíveis.  
O IP 10.0.0.15 representa o maior risco, com envio de credenciais detalhadas: acesso SSH e senha root temporária.  
O IP 10.0.0.37 expôs um cartão de crédito de teste.  
Recomenda-se auditoria imediata nos usuários listados e revisão de acesso a sistemas críticos.

Entrada: 📦 EMAIL CAPTURADO [2025-08-24 22:01:12]
Origem: 10.0.0.11:65012
Destino: 10.0.0.5:5000
De: alice@empresa.com
Para: ti@empresa.com
Conteúdo:
Login VPN: alice.vpn | senha: Alice2025!
--------------------------------------------------
📦 EMAIL CAPTURADO [2025-08-24 22:02:05]
Origem: 10.0.0.22:65144
Destino: 10.0.0.5:5000
De: suporte@corp.com
Para: cliente@gmail.com
Conteúdo:
Atendimento encerrado. Todas as informações seguras.
--------------------------------------------------
📦 EMAIL CAPTURADO [2025-08-24 22:03:21]
Origem: 10.0.0.33:65202
Destino: 10.0.0.5:5000
De: financeiro@corp.com
Para: auditoria@corp.com
Conteúdo:
Cartão teste: 4111 2222 3333 4444, validade 09/27, CVV 789
--------------------------------------------------
📦 EMAIL CAPTURADO [2025-08-24 22:04:10]
Origem: 10.0.0.44:65370
Destino: 10.0.0.5:5000
De: rh@empresa.com
Para: equipe@empresa.com
Conteúdo:
Convite para reunião de alinhamento na sexta-feira às 14h.
--------------------------------------------------
📦 EMAIL CAPTURADO [2025-08-24 22:05:58]
Origem: 10.0.0.11:65088
Destino: 10.0.0.5:5000
De: alice@empresa.com
Para: admin@corp.com
Conteúdo:
Credencial root temporária: root:TempAlice2025!
--------------------------------------------------
📦 EMAIL CAPTURADO [2025-08-24 22:06:42]
Origem: 10.0.0.55:65402
Destino: 10.0.0.5:5000
De: administrativo@empresa.com
Para: fornecedores@empresa.com
Conteúdo:
Pedido #4525 confirmado. Entrega prevista para 31/08.
--------------------------------------------------
📦 EMAIL CAPTURADO [2025-08-24 22:07:12]
Origem: 10.0.0.66:65512
Destino: 10.0.0.5:5000
De: bruno@empresa.com
Para: ti@empresa.com
Conteúdo:
SSH acesso: bruno_ssh | senha: Bruno2025!
--------------------------------------------------
📦 EMAIL CAPTURADO [2025-08-24 22:08:05]
Origem: 10.0.0.77:65644
Destino: 10.0.0.5:5000
De: suporte@corp.com
Para: cliente@gmail.com
Conteúdo:
Atendimento finalizado. Nenhuma ação adicional necessária.
--------------------------------------------------
📦 EMAIL CAPTURADO [2025-08-24 22:09:21]
Origem: 10.0.0.88:65702
Destino: 10.0.0.5:5000
De: financeiro@corp.com
Para: auditoria@corp.com
Conteúdo:
Conta bancária: Agência 1234, Conta 56789-0
--------------------------------------------------
📦 EMAIL CAPTURADO [2025-08-24 22:10:10]
Origem: 10.0.0.99:65870
Destino: 10.0.0.5:5000
De: rh@empresa.com
Para: equipe@empresa.com
Conteúdo:
Lembrete: treinamento de segurança amanhã às 15h.
--------------------------------------------------
📦 EMAIL CAPTURADO [2025-08-24 22:11:58]
Origem: 10.0.0.11:65092
Destino: 10.0.0.5:5000
De: alice@empresa.com
Para: admin@corp.com
Conteúdo:
Senha root temporária: root:SuperAlice2025!
--------------------------------------------------
📦 EMAIL CAPTURADO [2025-08-24 22:12:42]
Origem: 10.0.0.66:65515
Destino: 10.0.0.5:5000
De: bruno@empresa.com
Para: admin@corp.com
Conteúdo:
Credencial root: root:TempBruno2025!
--------------------------------------------------
📦 EMAIL CAPTURADO [2025-08-24 22:13:12]
Origem: 10.0.0.22:65150
Destino: 10.0.0.5:5000
De: suporte@corp.com
Para: cliente@gmail.com
Conteúdo:
Apenas confirmação de serviço. Nenhum dado sensível.
--------------------------------------------------
📦 EMAIL CAPTURADO [2025-08-24 22:14:05]
Origem: 10.0.0.33:65210
Destino: 10.0.0.5:5000
De: financeiro@corp.com
Para: auditoria@corp.com
Conteúdo:
Cartão teste: 5555 6666 7777 8888, validade 10/28, CVV 123
--------------------------------------------------
📦 EMAIL CAPTURADO [2025-08-24 22:15:21]
Origem: 10.0.0.44:65375
Destino: 10.0.0.5:5000
De: rh@empresa.com
Para: equipe@empresa.com
Conteúdo:
Aviso: reunião de alinhamento adiada para sexta-feira às 16h.
--------------------------------------------------
📦 EMAIL CAPTURADO [2025-08-24 22:16:10]
Origem: 10.0.0.55:65405
Destino: 10.0.0.5:5000
De: administrativo@empresa.com
Para: fornecedores@empresa.com
Conteúdo:
Pedido #4526 confirmado. Entrega prevista para 01/09.
--------------------------------------------------
📦 EMAIL CAPTURADO [2025-08-24 22:17:58]
Origem: 10.0.0.99:65872
Destino: 10.0.0.5:5000
De: rh@empresa.com
Para: equipe@empresa.com
Conteúdo:
Treinamento de conformidade agendado para terça-feira.
--------------------------------------------------
📦 EMAIL CAPTURADO [2025-08-24 22:18:42]
Origem: 10.0.0.11:65095
Destino: 10.0.0.5:5000
De: alice@empresa.com
Para: ti@empresa.com
Conteúdo:
VPN temporária: alice.vpn | senha: TesteVPN2025!
--------------------------------------------------
📦 EMAIL CAPTURADO [2025-08-24 22:19:12]
Origem: 10.0.0.66:65518
Destino: 10.0.0.5:5000
De: bruno@empresa.com
Para: admin@corp.com
Conteúdo:
SSH root: root:RootBruno2025!
--------------------------------------------------
📦 EMAIL CAPTURADO [2025-08-24 22:20:05]
Origem: 10.0.0.77:65650
Destino: 10.0.0.5:5000
De: suporte@corp.com
Para: cliente@gmail.com
Conteúdo:
Confirmação de atendimento concluído, tudo seguro.
--------------------------------------------------

Saída: 📌 Última verificação: 11 de 20 pacotes possuem dados vazados → 55%

📈 IPs que mais vazaram informações:

- 10.0.0.11 → 4 ocorrências
   - alice@empresa.com →
       - Login VPN: alice.vpn | senha: Alice2025!
       - Credencial root temporária: root:TempAlice2025!
       - Senha root temporária: root:SuperAlice2025!
       - VPN temporária: alice.vpn | senha: TesteVPN2025!

- 10.0.0.66 → 3 ocorrências
   - bruno@empresa.com →
       - SSH acesso: bruno_ssh | senha: Bruno2025!
       - Credencial root: root:TempBruno2025!
       - SSH root: root:RootBruno2025!

- 10.0.0.33 → 2 ocorrências
   - financeiro@corp.com →
       - Cartão teste: 4111 2222 3333 4444, validade 09/27, CVV 789
       - Cartão teste: 5555 6666 7777 8888, validade 10/28, CVV 123

✅ IPs sem dados sensíveis:
- 10.0.0.22 → suporte@corp.com
- 10.0.0.44 → rh@empresa.com
- 10.0.0.55 → administrativo@empresa.com
- 10.0.0.77 → suporte@corp.com
- 10.0.0.99 → rh@empresa.com

🔎 Tipos de vazamento detectados:
- Credenciais expostas (usuario/senha/root) → 7 pacotes
- Dados financeiros (cartão de crédito) → 2 pacotes
- Conta bancária → 1 pacote
- VPN temporária → 1 pacote

💡 Resumo:
Mais da metade dos emails contém dados sensíveis.  
Os IPs 10.0.0.11 e 10.0.0.66 são os maiores riscos, expondo credenciais e acessos root.  
O IP 10.0.0.33 expôs cartões de crédito de teste.  
Recomenda-se auditoria imediata nos usuários listados e revisão de acesso a sistemas críticos.

Entrada: 📦 EMAIL CAPTURADO [2025-08-24 23:45:12]
Origem: 10.0.0.10:67012
Destino: 10.0.0.5:5000
De: lucas@empresa.com
Para: ti@empresa.com
Conteúdo:
SSH acesso: lucas_ssh | senha: Lucas2025!
--------------------------------------------------
📦 EMAIL CAPTURADO [2025-08-24 23:46:05]
Origem: 10.0.0.21:67144
Destino: 10.0.0.5:5000
De: suporte@corp.com
Para: cliente@gmail.com
Conteúdo:
Atendimento finalizado. Todas as informações seguras.
--------------------------------------------------
📦 EMAIL CAPTURADO [2025-08-24 23:47:21]
Origem: 10.0.0.32:67202
Destino: 10.0.0.5:5000
De: financeiro@corp.com
Para: auditoria@corp.com
Conteúdo:
Cartão teste: 4111 2222 3333 4444, validade 09/27, CVV 789
--------------------------------------------------
📦 EMAIL CAPTURADO [2025-08-24 23:48:10]
Origem: 10.0.0.43:67370
Destino: 10.0.0.5:5000
De: rh@empresa.com
Para: equipe@empresa.com
Conteúdo:
Convite para reunião de alinhamento na sexta-feira às 14h.
--------------------------------------------------
📦 EMAIL CAPTURADO [2025-08-24 23:49:58]
Origem: 10.0.0.10:67088
Destino: 10.0.0.5:5000
De: lucas@empresa.com
Para: admin@corp.com
Conteúdo:
Credencial root temporária: root:TempLucas2025!
--------------------------------------------------
📦 EMAIL CAPTURADO [2025-08-24 23:50:42]
Origem: 10.0.0.54:67402
Destino: 10.0.0.5:5000
De: administrativo@empresa.com
Para: fornecedores@empresa.com
Conteúdo:
Pedido #4527 confirmado. Entrega prevista para 02/09.
--------------------------------------------------
📦 EMAIL CAPTURADO [2025-08-24 23:51:12]
Origem: 10.0.0.65:67512
Destino: 10.0.0.5:5000
De: carla@empresa.com
Para: ti@empresa.com
Conteúdo:
VPN temporária: carla.vpn | senha: CarlaVPN2025!
--------------------------------------------------
📦 EMAIL CAPTURADO [2025-08-24 23:52:05]
Origem: 10.0.0.76:67644
Destino: 10.0.0.5:5000
De: suporte@corp.com
Para: cliente@gmail.com
Conteúdo:
Atendimento finalizado. Nenhuma ação adicional necessária.
--------------------------------------------------
📦 EMAIL CAPTURADO [2025-08-24 23:53:21]
Origem: 10.0.0.87:67702
Destino: 10.0.0.5:5000
De: financeiro@corp.com
Para: auditoria@corp.com
Conteúdo:
Conta bancária: Agência 5678, Conta 12345-6
--------------------------------------------------
📦 EMAIL CAPTURADO [2025-08-24 23:54:10]
Origem: 10.0.0.10:67092
Destino: 10.0.0.5:5000
De: lucas@empresa.com
Para: admin@corp.com
Conteúdo:
Senha root temporária: root:SuperLucas2025!
--------------------------------------------------
Saída:"""

print("Submitting generation request...")
generated_response = model.generate_text(prompt=prompt_input, guardrails=False)
print(generated_response)
