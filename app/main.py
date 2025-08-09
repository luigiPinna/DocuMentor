#!/usr/bin/env python3
"""
DocuMentor - Assistente documentale basato su AI
Modulo principale dell'applicazione che gestisce l'inizializzazione e il flusso dell'applicazione.
"""

import sys
from typing import Optional

from core.logging import logger
from config.config_manager import ConfigManager
from core.ai_service import AIService
from utils.input_validator import get_user_input, is_exit_command


def initialize_system() -> tuple[Optional[ConfigManager], bool]:
    """
    Inizializza il sistema configurando config manager e logger.

    Returns:
        tuple: (ConfigManager, success) - ConfigManager se successo, None se fallito
    """
    try:
        config_manager = ConfigManager()

        # Inizializza il logger singleton
        logger.initialize(
            name='DocuMentorLogger',
            log_file=config_manager.main_log_file_path
        )

        logger.info("DocuMentor starting...")
        return config_manager, True

    except FileNotFoundError as e:
        print(f"Errore file di configurazione: {e}")
        return None, False
    except ValueError as e:
        print(f"Errore configurazione: {e}")
        return None, False
    except Exception as e:
        print(f"Errore imprevisto durante l'inizializzazione: {e}")
        return None, False


def initialize_ai_service(config_manager: ConfigManager) -> Optional[AIService]:
    """
    Inizializza il servizio AI

    Args:
        config_manager: Config manager dell'applicazione

    Returns:
        AIService se l'inizializzazione ha successo, None altrimenti
    """
    try:
        return AIService(config_manager)

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


def process_query(ai_service: AIService, question: str) -> None:
    """
    Elabora una query dell'utente

    Args:
        ai_service: Servizio AI
        question: Domanda dell'utente
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
    config_manager, success = initialize_system()
    if not success or not config_manager:
        print("Impossibile inizializzare il sistema. Verifica la configurazione.")
        sys.exit(1)

    # Inizializzazione del servizio AI
    ai_service = initialize_ai_service(config_manager)
    if not ai_service:
        logger.critical("Impossibile inizializzare il servizio AI")
        print("Impossibile inizializzare il servizio AI. Applicazione terminata.")
        sys.exit(1)

    logger.info("Sistema inizializzato correttamente")
    print("DocuMentor è pronto! Puoi iniziare a fare domande.")

    try:
        # Loop principale per gestire più domande
        while True:
            question = get_user_input()

            # Controllo per uscire dal programma
            if is_exit_command(question):
                logger.info("Uscita richiesta dall'utente")
                print("Grazie per aver usato DocuMentor. Arrivederci!")
                break

            # Elabora la query
            process_query(ai_service, question)

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