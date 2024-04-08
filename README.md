##Problema:
Sviluppa uno script console che usando llamaindex e i concetti ad alto livello sopra descritti nella immagine (tecniche RAG) proceda a:
- Ricevere in input una domanda testuale (i.e cosa è owlise)
- Leggere il contenuto di un PDF (i.e l’allegato alla presente email)
- Effettui una chiamata a OpenAI o un altro servizio di LLM
- Risposta in linguaggio naturale

Utilizza Github e condividi un link al repository per procedere nella valutazione della soluzione implementata.

### Criteri di valutazione:
- Correttezza dell'implementazione.
- Pulizia e leggibilità del codice.
- Utilizzo efficace delle tecnologie richieste.
- Gestione degli errori e degli edge case.


## Prerequisiti

Prima di iniziare, assicurati di avere installato Python 3.11 sul tuo sistema.
Questa versione è necessaria per garantire la compatibilità con tutte le dipendenze e le funzionalità del progetto.

## Installazione

Per installare le dipendenze del progetto, naviga nella directory principale del progetto e esegui il seguente comando:

```bash
pip install -r requirements.txt
```

Questo installerà tutte le librerie necessarie elencate in `requirements.txt`.

## Struttura del Progetto

Il progetto è organizzato come segue:

- `data/`: Contiene il file Excel con i dati dei dipendenti.
- `app/`: Codice sorgente dell'applicazione, diviso in moduli funzionali.
- `tests/`: Test unitari e di integrazione per il progetto.
- `docs/`: File vari e documentazione del progetto
- `requirements.txt`: Elenco delle librerie necessarie per il progetto.
- `config.yml`: File di configurazione per l'applicazione.

## Utilizzo

Creare il file yml di configurazione `config.yml` nella directory principale del progetto.
Esempio di file di configurazione:

```yaml
[FILE]
file_password = xxx
input_data_file_path_EMEA = xxx
input_data_file_path_IT = xxx
```

Per avviare l'applicazione, naviga nella directory `app/` e esegui il file 
`main.py` con Python:

```bash
python main.py
```
