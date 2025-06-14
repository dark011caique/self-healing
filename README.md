# Projeto de Self-Healing com Zabbix, Ansible e Python

Este projeto implementa uma solução de automação de self-healing para reiniciar o Nginx automaticamente quando ele cai, utilizando Zabbix para monitoramento, Ansible para correção e um webhook Flask como integração. Desenvolvido por Caique Silva Pereira para ambientes de laboratório, testes ou pequenas automações internas.

## 🔧 Pré-Requisitos

- **Python 3** (no host que roda o webhook)
- **Ansible** instalado no host do webhook
- **Zabbix** rodando em Docker ou bare metal
- **SSH** configurado entre o webhook e o host monitorado
- **Curl** instalado no container do Zabbix

## 🚀 Instalação e Configuração

### 1️⃣ Instale as dependências Python
    cd webhook
    pip install -r requirements.txt

### 2️⃣ Rode o webhook Flask
    python app.py --host=0.0.0.0 --port=5000

### 3️⃣ Configure o Ansible (ansible/hosts.ini)
    [linux_host]
    172.18.0.2 ansible_user=root ansible_ssh_private_key_file=~/.ssh/container_key

### 4️⃣ Playbook de restart (ansible/restart_nginx.yml)
    - name: Reiniciar nginx se estiver parado (compatível com container)
    hosts: all
    become: yes
    tasks:
        - name: Verifica se nginx está rodando via processo
        shell: pgrep nginx
        register: nginx_status
        ignore_errors: yes

        - name: Reinicia nginx se necessário
        shell: nginx
        when: nginx_status.rc != 0

### 5️⃣Configure o Script no Zabbix
    mkdir -p /usr/lib/zabbix/alertscripts/
    chmod +x /usr/lib/zabbix/alertscripts/webhook.sh

- **Conteúdo do webhook.sh:** 
    #!/bin/sh
    curl -X POST http://<IP_DO_WSL>:5000/self-healing

### 6️⃣ Configuração no Zabbix
- **Media Type:**
    * Nome: Webhook Self-Healing
    * Tipo: Script
    * Script name: webhook.sh
    * Message template: (⚠️ obrigatório)
        * Subject: Auto-Healing
        * Message: qualquer texto

- **User:**
    Configure o Admin ou outro usuário com esse Media Type na aba Media

- **Action:**
    Trigger: Nginx caiu (auto-reparo)
    Operation: Send message → Webhook Self-Healing

### 🛑 Testando o Self-Healing
    pkill nginx

O Zabbix detecta que o NGINX caiu
Dispara o webhook
O Flask recebe e executa o Ansible
O Ansible reinicia o NGINX automaticamente
O Zabbix detecta o processo subindo e fecha o problema
