# Casi d'uso PyChat v3

### Client

#### Messaggistica

- _Descrizione_: L'utente registrato invia e riceve messaggi
- _Attori_: Utente
- _Precondizioni_:
  - Essere connessi ad Internet
  - Avere l'applicazione aperta e connessa al server, che deve essere attivo
  - Avere un login valido
- _Scenario di successo_: L'utente riesce a mandare, ricevere e visualizzare correttamente messaggi testuali con altri utenti
- _Scenari di fallimento_:
  - Errore di esecuzione dell'applicazione
  - Server non attivo o errore di comunicazione
  - Non si ha un login valido, si apre finestra di login
- _Postcondizioni_: Viene mandato un segnale di chiusura al server

#### Login

- _Descrizione_: L'utente accede per utilizzare l'applicazione
- _Attori_: Utente
- _Precondizioni_:
  - Essere connessi ad Internet
  - Avere l'applicazione aperta e connessa al server, che deve essere attivo
  - Possedere un account creato in precedenza
- _Scenario di successo_: L'utente inserisce i suoi dati ed accedere all'applicazione con il suo account
- _Scenari di fallimento_:
  - Server non attivo o errore di comunicazione
  - Il login è invalido, per un errore di battitura o perché è inesistente
- _Postcondizioni_: Si salva il login localmente e si apre la finestra principale

#### Signup

- _Descrizione_: L'utente crea un account per utilizzare l'applicazione
- _Attori_: Utente
- _Precondizioni_:
  - Essere connessi ad Internet
  - Avere l'applicazione aperta e connessa al server, che deve essere attivo
- _Scenario di successo_: L'utente inserisce i suoi dati, l'account viene creato e si accede all'applicazione
- _Scenari di fallimento_:
  - Server non attivo o errore di comunicazione
  - Il nome utente è già utilizzato, non permettendo la creazione dell'account
- _Postcondizioni_: Si apre la finestra principale
