import random

import spade
from spade.behaviour import PeriodicBehaviour
from spade.message import Message
import asyncio

class Sender(spade.agent.Agent):
    tools = ['Este prea intuneric in camera',
             'Imi este frig',
             'Vreau sa ascult muzica',
             'Imi este cald',
             'Inchide becul',
             'Opreste muzica']
    class Send(PeriodicBehaviour):
        async def run(self):
            chosen_tool = random.choice(self.agent.tools)
            msg = Message(to="simple_agent@localhost")
            msg.set_metadata("performative", "request")
            msg.body = chosen_tool
            await self.send(msg)
            print(f'Mesaj trimis: {chosen_tool}')

    async def setup(self):
        print('Agentul a pornit')
        await asyncio.sleep(2)
        b = self.Send(period=30)
        self.add_behaviour(b)


async def main():
    sender = Sender("client@localhost", "pass")
    await sender.start(auto_register=True)
    await spade.wait_until_finished(sender)
    print("Agentul Client s-a oprit.")

if __name__ == "__main__":
    asyncio.run(main())