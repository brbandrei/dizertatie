import asyncio
import json

from spade import wait_until_finished
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.agent import Agent
from spade.template import Template
from spade.message import Message

def controleaza_bec(stare):
    with open("mediu.json", 'r', encoding='utf-8') as f:
        mediu = json.load(f)
    mediu['lumina'] = stare
    with open("mediu.json", 'w', encoding='utf-8') as f:
        json.dump(mediu, f, indent=4)
    return f"Becul a fost setat pe {stare}"

def controleaza_boxa(stare):
    with open("mediu.json", 'r', encoding='utf-8') as f:
        mediu = json.load(f)
    mediu['boxa'] = stare
    with open("mediu.json", 'w', encoding='utf-8') as f:
        json.dump(mediu, f, indent=4)
    return f"Boxa a fost setata pe {stare}"

def controleaza_temperatura(valoare):
    with open("mediu.json", 'r', encoding='utf-8') as f:
        mediu = json.load(f)
    mediu['temperatura'] = valoare
    with open("mediu.json", 'w', encoding='utf-8') as f:
        json.dump(mediu, f, indent=4)
    return f"Temperatura a fost setata pe {valoare} grade Celsius"

class ReceiverAgent(Agent):
    class RecvBehav(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)
            if msg:
                msg_type = msg.metadata.get("performative")
                if msg_type == 'request':
                    msg_llm = Message()
                    msg_llm.to = 'llm_agent@localhost'
                    msg_llm.set_metadata("message_type", "llm")  # required by LLMAgent
                    msg_llm.set_metadata("performative", "request")  # expected performative
                    msg_llm.thread = "conversation-123"  # optional conversation id
                    msg_llm.body = msg.body
                    msg_llm.sender = str(self.agent.jid)
                    await self.send(msg_llm)
                    print(f'Am trimis mesajul catre llm_agent: {msg_llm.body}')
                else:
                    print(f'Mesaj de la LLM Agent primit: {msg.body}')
                    exec(msg.body)
            else:
                print(f"Niciun mesaj primit in ultimele 10 de secunde.")

    async def setup(self):
        print(f"Agentul Receiver {self.jid} porneste.")
        self.add_behaviour(self.RecvBehav())

async def main():
    receiver = ReceiverAgent("simple_agent@localhost", "pass")
    await receiver.start(auto_register=True)
    print("Agentul Receiver este pornit")
    await wait_until_finished(receiver)


if __name__ == "__main__":
    asyncio.run(main())