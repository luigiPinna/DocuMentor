"""
DocuMentor - Assistente documentale basato su AI
Modulo principale dell'applicazione che gestisce l'inizializzazione e il flusso dell'applicazione.
"""

import sys
import logging
from typing import Optional
from config.config_manager import ConfigManager
from logger import Logger
from ai_service import AIService


def validate_question(question: str) -> bool:
    """
    Valida l'input dell'utente

    Args:
        question: Domanda inserita dall'utente

    Returns:
        True se la domanda è valida, False altrimenti
    """
    if not question or not question.strip():
        return False

    # Rimuove spazi e controlla lunghezza minima
    cleaned_question = question.strip()
    if len(cleaned_question) < 2:
        return False

    return True


def initialize_system() -> tuple[Optional[ConfigManager], Optional[logging.Logger]]:
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

    except FileNotFoundError as e:
        print(f"Errore file di configurazione: {e}")
        return None, None
    except ValueError as e:
        print(f"Errore configurazione: {e}")
        return None, None
    except Exception as e:
        print(f"Errore imprevisto durante l'inizializzazione: {e}")
        return None, None


def initialize_ai_service(logger: logging.Logger, config_manager: ConfigManager) -> Optional[AIService]:
    """
    Inizializza il servizio AI

    Args:
        logger: Logger dell'applicazione
        config_manager: Config manager dell'applicazione

    Returns:
        AIService se l'inizializzazione ha successo, None altrimenti
    """
    try:
        return AIService(logger, config_manager)

    except FileNotFoundError as e:
        logger.error(f"File non trovati per AI service: {e}")
        print("Errore: Assicurati che i documenti siano presenti nella directory configurata.")
        return None
    except ValueError as e:
        logger.error(f"Errore configurazione AI: {e}")
        print(f"Errore configurazione AI: {e}")
        return None
    except Exception as e:
        logger.error(f"Errore imprevisto nell'inizializzazione AI: {e}")
        print(f"Errore imprevisto nell'inizializzazione AI: {e}")
        return None


def handle_user_input() -> str:
    """
    Gestisce l'input dell'utente con validazione

    Returns:
        Domanda validata dell'utente
    """
    while True:
        question = input("\nInserisci la tua domanda (o 'exit' per uscire): ").strip()

        # Controllo per uscire
        if question.lower() in ['exit', 'quit', 'q', 'esci']:
            return question

        # Validazione
        if validate_question(question):
            return question
        else:
            print("Per favore inserisci una domanda valida (almeno 2 caratteri).")


def process_query(ai_service: AIService, question: str, logger: logging.Logger) -> None:
    """
    Elabora una query dell'utente

    Args:
        ai_service: Servizio AI
        question: Domanda dell'utente
        logger: Logger dell'applicazione
    """
    logger.info(f"Domanda ricevuta: {question}")

    try:
        print("Elaborazione in corso...")
        response = ai_service.perform_query(question)
        print("\nRisposta:")
        print(response)

    except ValueError as e:
        logger.warning(f"Domanda non valida: {e}")
        print(f"Domanda non valida: {e}")
    except ConnectionError as e:
        logger.error(f"Errore di connessione: {e}")
        print("Errore di connessione. Verifica la connessione internet e riprova.")
    except Exception as e:
        logger.error(f"Errore durante l'elaborazione: {e}")
        print(f"Si è verificato un errore durante l'elaborazione: {e}")


def main():
    """Funzione principale dell'applicazione DocuMentor."""

    # Inizializzazione del sistema
    config_manager, logger = initialize_system()
    if not config_manager or not logger:
        print("Impossibile inizializzare il sistema. Verifica la configurazione.")
        sys.exit(1)

    # Inizializzazione del servizio AI
    ai_service = initialize_ai_service(logger, config_manager)
    if not ai_service:
        logger.critical("Impossibile inizializzare il servizio AI")
        print("Impossibile inizializzare il servizio AI. Applicazione terminata.")
        sys.exit(1)

    logger.info("Sistema inizializzato correttamente")
    print("DocuMentor è pronto! Puoi iniziare a fare domande.")

    try:
        # Loop principale per gestire più domande
        while True:
            question = handle_user_input()

            # Controllo per uscire dal programma
            if question.lower() in ['exit', 'quit', 'q', 'esci']:
                logger.info("Uscita richiesta dall'utente")
                print("Grazie per aver usato DocuMentor. Arrivederci!")
                break

            # Elabora la query
            process_query(ai_service, question, logger)

    except KeyboardInterrupt:
        print("\nOperazione interrotta dall'utente.")
        logger.info("Interruzione da tastiera rilevata")
    except Exception as e:
        error_msg = f"Errore imprevisto nel loop principale: {e}"
        logger.critical(error_msg)
        print(f"Errore critico: {e}")
        sys.exit(1)
    finally:
        logger.info("DocuMentor terminato")
        print("\nDocuMentor chiuso correttamente.")


if __name__ == "__main__":
    main()