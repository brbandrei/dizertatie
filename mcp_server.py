from fastmcp import FastMCP
import json
mcp = FastMCP("Demo 🚀")


@mcp.tool
def controleaza_bec(stare: str):
    """Controleaza starea becului: 'on' sau 'off'"""
    with open("mediu.json", 'r', encoding='utf-8') as f:
        mediu = json.load(f)
    mediu['lumina'] = stare
    with open("mediu.json", 'w', encoding='utf-8') as f:
        json.dump(mediu, f, indent=4)
    return f"Becul a fost setat pe {stare}"

@mcp.tool
def controleaza_boxa(stare: str):
    """Controleaza starea boxei: 'on' sau 'off'"""
    with open("mediu.json", 'r', encoding='utf-8') as f:
        mediu = json.load(f)
    mediu['boxa'] = stare
    with open("mediu.json", 'w', encoding='utf-8') as f:
        json.dump(mediu, f, indent=4)
    return f"Boxa a fost setata pe {stare}"

@mcp.tool
def controleaza_temperatura(valoare: int):
    """Seteaza temperatura dorita in grade Celsius"""
    with open("mediu.json", 'r', encoding='utf-8') as f:
        mediu = json.load(f)
    mediu['temperatura'] = valoare
    with open("mediu.json", 'w', encoding='utf-8') as f:
        json.dump(mediu, f, indent=4)
    return f"Temperatura a fost setata pe {valoare} grade Celsius"


if __name__ == "__main__":
    mcp.run()