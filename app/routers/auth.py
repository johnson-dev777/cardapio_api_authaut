# app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.database import obter_sessao
from app.dependencies import verificar_logista
from app.models.cliente import Cliente, UserRole, ClienteResponse

router = APIRouter(prefix='/auth', tags=["Autenticação"])

@router.get('/me')
def me():
    return 'Sou Rogério'

@router.post('/login')
def login():
    return 'Autenticado com sucesso!'

# =====================================================================
# NOVO: Rota de Promoção a Logista via Auth
# =====================================================================
@router.patch(
    "/clientes/{cliente_id}/promover-logista", 
    response_model=ClienteResponse,
    summary="Promover um cliente para Logista (Admin)"
)
def promover_logista(
    cliente_id: int,
    sessao: Session = Depends(obter_sessao),
    admin_atual: Cliente = Depends(verificar_logista)
):
    cliente_alvo = sessao.get(Cliente, cliente_id)
    if not cliente_alvo:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")
    
    if cliente_alvo.role == UserRole.LOGISTA:
        raise HTTPException(status_code=400, detail="Este cliente já é um logista.")

    cliente_alvo.role = UserRole.LOGISTA
    sessao.add(cliente_alvo)
    sessao.commit()
    sessao.refresh(cliente_alvo)
    return cliente_alvo