"""Utility per validazione input utente"""

from core.logging import logger


def validate_question(question: str) -> bool:
    """
    Valida l'input dell'utente

    Args:
        question: Domanda inserita dall'utente

    Returns:
        True se la domanda è valida, False altrimenti
    """
    if not question or not question.strip():
        logger.debug("Domanda vuota o solo spazi")
        return False

    # Rimuove spazi e controlla lunghezza minima
    cleaned_question = question.strip()
    if len(cleaned_question) < 2:
        logger.debug(f"Domanda troppo corta: {len(cleaned_question)} caratteri")
        return False

    logger.debug(f"Domanda validata: {len(cleaned_question)} caratteri")
    return True


def is_exit_command(question: str) -> bool:
    """
    Controlla se il comando è per uscire dall'applicazione

    Args:
        question: Input dell'utente

    Returns:
        True se è un comando di uscita
    """
    exit_commands = ['exit', 'quit', 'q', 'esci']
    return question.lower().strip() in exit_commands


def get_user_input() -> str:
    """
    Gestisce l'input dell'utente con validazione

    Returns:
        Domanda validata dell'utente o comando di uscita
    """
    while True:
        question = input("\nInserisci la tua domanda (o 'exit' per uscire): ").strip()

        # Controllo per uscire
        if is_exit_command(question):
            logger.info("Comando di uscita rilevato")
            return question

        # Validazione
        if validate_question(question):
            return question
        else:
            print("Per favore inserisci una domanda valida (almeno 2 caratteri).")