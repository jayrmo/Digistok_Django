from django import template

register = template.Library()

@register.simple_tag
def qr_code(produto):
    """
    Gera URL do QR code para um produto usando API externa
    """
    if not produto:
        return ""
    
    # Dados do produto para o QR code
    qr_data = f"Produto: {produto.descricao} | Código: {produto.codigo}"
    
    # URL da API do QR Server (gratuita)
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={qr_data}"
    
    return qr_url

@register.simple_tag
def qr_code_modal(produto):
    """
    Gera URL do QR code maior para modal
    """
    if not produto:
        return ""
    
    qr_data = f"Produto: {produto.descricao} | Código: {produto.codigo}"
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={qr_data}"
    
    return qr_url
