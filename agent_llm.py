import json
import asyncio
import os

from spade import wait_until_finished
from spade_llm.agent import LLMAgent
from spade_llm.providers import LLMProvider
from spade_llm import LLMTool

MEDIU_PATH = os.path.join(os.path.dirname(__file__), "mediu.json")


async def main():
    def return_mediu_state():
        with open(MEDIU_PATH, 'r', encoding='utf-8') as f:
            mediu_state = f.read()
        print(f"Starea curenta a mediului: {mediu_state}")
        return mediu_state

    ALLOWED_TOOLS = {
        "controleaza_bec": {"type": "str", "values": ["on", "off"]},
        "controleaza_boxa": {"type": "str", "values": ["on", "off"]},
        "controleaza_temperatura": {"type": "number", "min": 5, "max": 35},
    }

    with open(MEDIU_PATH, 'r', encoding='utf-8') as f:
            mediu_curent = json.load(f)

    SYSTEM_INSTRUCTIONS = """
    Ești un agent care decide ce tool-uri trebuie folosite intr-un mediu smart. Vei primi o cerere de la utilizator în limbaj natural. Alege EXACT un singur instrument (tool) care sa satisfaca cererea.

    Instrumente disponibile si ce fac (la acestea nu ai acces):
    - controleaza_bec: porneste sau opreste lumina din camera. Parametru: "on" sau "off".
    - controleaza_boxa: porneste sau opreste boxa (redarea de sunet). Parametru: "on" sau "off".
    - controleaza_temperatura: seteaza temperatura dorita în camera (un grade Celsius). Parametru: un numar (de exemplu 21). Daca temperatura dorita nu este specificata, modifica temperatura cu 2 grade fata de cea curenta in functie de cerinta utilzatorului.

    Instrument la care ai acces:
    - check_mediu: returneaza starea curenta a mediului. Foloseste-l mereu inainte de a decide ce instrument sa dai ca raspuns.
    Reguli stricte de iesire:
    - Raspunsul trebuie sa fie EXACT apelul unui singur instrument din cele disponibile (controleaza_bec, controleaza_boxa, controleaza_temperatura), cu parametrul corect.
    - Daca starea mediului satisfice cererea, returnează pass.

    - Daca cererea nu poate fi satisfacuta cu instrumentele disponibile, returneaza pass.
    - Nu inventa instrumente noi.
    - Nu oferi explicatii sau alte texte.
      Exemple valide:
        controleaza_bec("on")
        controleaza_boxa("off")
        controleaza_temperatura(22)
    """

    api_key = os.environ.get("OPENAI_API_KEY")
    provider = LLMProvider.create_openai(api_key, model='gpt-4o')

    mediu_tool = LLMTool(
        name='return_mediu_state',
        description='Returnează starea curentă a mediului în format JSON',
        func=return_mediu_state,
        parameters={
            'type': 'object',
            'properties': {},
            'required': [],
        },
    )

    agent_llm = LLMAgent(
        jid='llm_agent@localhost',
        password='pass',
        provider=provider,
        system_prompt=SYSTEM_INSTRUCTIONS,
        reply_to='simple_agent@localhost',
        tools=[mediu_tool],
    )

    await agent_llm.start()
    print("Agentul LLM este pornit")
    await wait_until_finished(agent_llm)


if __name__ == "__main__":
    asyncio.run(main())
