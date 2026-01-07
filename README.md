# 🏋️ Ginásio Virtual - Integração para Home Assistant

Esta é uma integração personalizada (Custom Component) para o Home Assistant que permite monitorizar os dados da tua conta no OnVirtualGym, como as presenças mensais no ginásio.

**Aviso**: Esta integração é um projeto comunitário e não é oficialmente suportada pelo OnVirtualGym.

## ✨ Funcionalidades

* Monitoriza o número de presenças no ginásio durante o mês atual.
* Autenticação via Nome de Utilizador e Palavra-passe.
* Obtém automaticamente o Token de acesso e o Número de Sócio.
* Atualização automática dos dados (por padrão, de hora em hora).
* Configuração fácil via interface gráfica (UI).

## 🚀 Instalação

### Instalação via HACS (Recomendado)

1.  Abre o **HACS** no teu Home Assistant.
2.  Vai a `Integrações` e clica nos `três pontos verticais` no canto superior direito.
3.  Seleciona `Custom repositories`.
4.  Copia o URL deste repositório (`https://github.com/patricncosta/ha_onvirtualgym`) e cola-o no campo `Repository`.
5.  Em `Category`, escolhe `Integration`.
6.  Clica em `ADD`.
7.  Procura pela integração `OnVirtualGym` na lista do HACS e clica em `INSTALL`.
8.  Reinicia o teu Home Assistant.

### Instalação Manual

1.  Navega até à pasta `custom_components` na tua configuração do Home Assistant.
2.  Cria uma nova pasta chamada `onvirtualgym
3.  Copia todos os ficheiros desta integração (do repositório) para a pasta `onvirtualgym` que acabaste de criar. A estrutura final deverá ser:
    ```
    config/custom_components/onvirtualgym/
    ├── __init__.py
    ├── config_flow.py
    ├── const.py
    ├── coordinator.py
    ├── manifest.json
    ├── sensor.py
    └── translations/
        ├── en.json
        └── pt.json
    ```
4.  Reinicia o teu Home Assistant.

## ⚙️ Configuração

Após a instalação (via HACS ou manual) e o reinício do Home Assistant:

1.  Vai a **Definições > Dispositivos e Serviços**.
2.  Clica em `+ ADICIONAR INTEGRAÇÃO` no canto inferior direito.
3.  Procura por `OnVirtualGym`.
4.  Introduz o teu `Nome de Utilizador` e `Palavra-passe` do OnVirtualGym.
5.  Clica em `ENVIAR`.

A integração irá automaticamente tentar fazer login, obter o teu número de sócio e criar a entidade `sensor.onvirtualgym_monthly_attendances`.

## 📊 Entidades Criadas

* `sensor.onvirtualgym_monthly_attendances`: Mostra o número de idas ao ginásio no mês atual. Possui um atributo `history` com a lista completa de entradas/saídas.

## 🤝 Contribuições

Contribuições são bem-vindas! Se encontrares um bug, tiveres uma ideia para uma nova funcionalidade ou quiseres ajudar a melhorar o código, por favor, abre uma `Issue` ou um `Pull Request` neste repositório.

## 📜 Licença

Este projeto é licenciado sob a licença MIT. Consulta o ficheiro `LICENSE` para mais detalhes.