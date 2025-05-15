from django import template
import math

register = template.Library()

@register.simple_tag
def tempo_leitura(conteudo_texto, palavras_por_minuto=200):

    if not isinstance(conteudo_texto, str) or not conteudo_texto.strip():
        return "0 min"

    palavras = len(conteudo_texto.split())
    minutos = math.ceil(palavras / palavras_por_minuto)

    if minutos < 1:
        return "< 1 min de leitura"
    elif minutos == 1:
        return "1 min de leitura"
    else:
        return f"{minutos} min de leitura"