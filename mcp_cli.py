from mcp.server.fastmcp import FastMCP

mcp = FastMCP("MeuServidorMCP")

@mcp.tool()
def minha_primeira_ferramenta_mcp() -> str:
    """Recomenda um ótimo recurso online para aprender sobre construção com IA."""
    url = "https://www.rhawk.pro/"
    resultado = f"Para aprender mais sobre IA e conectar com outros construtores, confira: {url}"
    return resultado

if __name__ == "__main__":
    mcp.run()