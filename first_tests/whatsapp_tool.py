import pywhatkit
from typing import Optional, Type
from pydantic import BaseModel, Field

# LangChain / LangGraph
from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.tools import BaseTool

import os
from dotenv import load_dotenv

load_dotenv()


# 1) Définir un schéma Pydantic pour les arguments
class WhatsAppToolInput(BaseModel):
    """Schéma d'entrée pour l'outil WhatsApp."""

    method: str = Field(
        ...,
        description="Which method to call, e.g. 'send_msg_to_brother' or 'send_msg_to_number'",
    )
    content: str = Field(..., description="The text message to be sent")
    phone_number: Optional[str] = Field(
        None,
        description="If method='send_msg_to_number', this is the E.164 phone number (e.g. +33612345678)",
    )


# 2) Définir l’outil WhatsApp (hérite de BaseTool)
class WhatsAppTool(BaseTool):
    """
    Outil pour envoyer un message WhatsApp via pywhatkit.
    """

    name: str = "whatsapp_tool"
    description: str = (
        "Allows sending messages to WhatsApp. "
        "Methods available: 'send_msg_to_brother', 'send_msg_to_number'."
    )
    args_schema: Type[BaseModel] = WhatsAppToolInput

    # Exemple : numéro "Frère" en dur.
    brother_number: str = os.getenv("BROTHER_NUMBER")

    def _run(
        self,
        method: str,
        content: str,
        phone_number: Optional[str] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """
        Méthode synchrone appelée quand un LLM invoque l'outil.
        """
        try:
            if method == "send_msg_to_brother":
                return self.send_msg_to_brother(content)
            elif method == "send_msg_to_number":
                if not phone_number:
                    return "Error: phone_number is required for method='send_msg_to_number'."
                return self.send_msg_to_number(phone_number, content)
            else:
                return (
                    "Error: Unknown method. "
                    "Use 'send_msg_to_brother' or 'send_msg_to_number'."
                )
        except Exception as e:
            return f"Error while sending WhatsApp message: {str(e)}"

    async def _arun(
        self,
        method: str,
        content: str,
        phone_number: Optional[str] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Version asynchrone, si besoin."""
        # Pour simplifier, on réutilise la logique synchrone
        return self._run(method, content, phone_number, run_manager)

    # 3) Méthodes internes à la classe
    def send_msg_to_brother(self, content: str) -> str:
        """
        Envoie un message au numéro "Frère" (self.brother_number).
        """
        pywhatkit.sendwhatmsg_instantly(self.brother_number, content)
        return f"Message envoyé au Frère: {content}"

    def send_msg_to_number(self, phone_number: str, content: str) -> str:
        """
        Envoie un message au numéro spécifié.
        """
        pywhatkit.sendwhatmsg_instantly(phone_number, content)
        return f"Message envoyé au numéro {phone_number}: {content}"
