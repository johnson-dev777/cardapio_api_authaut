from fastapi import Header, HTTPException, Depends, status
from sqlmodel import Session
from app.database import obter_sessao
from app.models.cliente import Cliente, UserRole

def obter_cliente_autenticado(
    x_cliente_id: int = Header(..., alias="X-Cliente-Id"),
    sessao: Session = Depends(obter_sessao),
) -> Cliente:
    cliente = sessao.get(Cliente, x_cliente_id)
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Cliente não autorizado (X-Cliente-Id={x_cliente_id}).",
        )
    return cliente

def verificar_logista(
    cliente_logado: Cliente = Depends(obter_cliente_autenticado)
) -> Cliente:
    if cliente_logado.role != UserRole.LOGISTA:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Apenas logistas (admins) podem realizar esta ação."
        )
    return cliente_logado

def obter_cliente_opcional(
    x_cliente_id: int | None = Header(default=None, alias="X-Cliente-Id"),
    sessao: Session = Depends(obter_sessao),
) -> Cliente | None:
    """Retorna o cliente se o header for enviado, ou None se não for."""
    if x_cliente_id is None:
        return None
    return sessao.get(Cliente, x_cliente_id)

# app/dependencies.py
def verificar_permissao_cardapio(
    cliente_logado: Cliente = Depends(obter_cliente_autenticado)
) -> Cliente:
    if cliente_logado.role != UserRole.LOGISTA:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Clientes comuns não podem cadastrar itens. Apenas logistas têm essa permissão."
        )
    return cliente_logado