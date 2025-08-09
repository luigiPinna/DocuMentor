"""
DocuMentor - Assistente documentale basato su AI
Modulo principale dell'applicazione che gestisce l'inizializzazione e il flusso dell'applicazione.
"""

import sys
from typing import Optional
from config_manager import ConfigManager
from logger import Logger
from ai_service import AIService


def initialize_system() -> tuple[Optional[ConfigManager], Optional[Logger]]:
    """
    Inizializza il sistema configurando config manager e logger.

    Returns:
        tuple: (ConfigManager, Logger) se l'inizializzazione ha successo, altrimenti (None, None)
    """
    try:
        config_manager = ConfigManager()
        logger = Logger('DocuMentorLogger', log_file=config_manager.main_log_file_path).get_logger()
        logger.info("DocuMentor starting...")
        return config_manager, logger
    except Exception as e:
        print(f"Errore durante l'inizializzazione: {e}")
        return None, None


def main():
    """Funzione principale dell'applicazione DocuMentor."""

    # Inizializzazione del sistema
    config_manager, logger = initialize_system()
    if not config_manager or not logger:
        sys.exit(1)

    try:
        # Inizializzazione del servizio AI
        ai_service = AIService(logger, config_manager)

        # Loop principale per gestire più domande
        while True:
            # Input dell'utente
            question = input("\nInserisci la tua domanda (o 'exit' per uscire): ")

            # Controllo per uscire dal programma
            if question.lower() in ['exit', 'quit', 'q', 'esci']:
                logger.info("Uscita richiesta dall'utente")
                print("Grazie per aver usato DocuMentor. Arrivederci!")
                break

            if not question.strip():
                print("Per favore inserisci una domanda valida.")
                continue

            # Registrazione della domanda
            logger.info(f"Domanda ricevuta: {question}")

            # Esecuzione della query e gestione errori
            try:
                print("Elaborazione in corso...")
                response = ai_service.perform_query(question)
                print("\nRisposta:")
                print(response)
            except Exception as e:
                error_msg = f"Errore durante l'elaborazione della domanda: {e}"
                logger.error(error_msg)
                print(f"Si è verificato un errore: {e}")

    except KeyboardInterrupt:
        print("\nOperazione interrotta dall'utente.")
        logger.info("Interruzione da tastiera rilevata")
    except Exception as e:
        error_msg = f"Errore imprevisto: {e}"
        if logger:
            logger.critical(error_msg)
        print(error_msg)
    finally:
        # Pulizia finale
        if logger:
            logger.info("DocuMentor terminato")
        print("\nDocuMentor chiuso correttamente.")


if __name__ == "__main__":
    main()