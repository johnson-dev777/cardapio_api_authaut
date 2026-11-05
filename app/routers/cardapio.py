# app/routers/cardapio.py
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select, or_

from app.database import obter_sessao
from app.dependencies import (
    verificar_permissao_cardapio,  # <-- Nova dependência específica
    obter_cliente_opcional,
)
from app.models.cliente import Cliente, UserRole
from app.models.item_cardapio import (
    ItemCardapio,
    ItemCardapioCreate,
    ItemCardapioUpdate,
    ItemCardapioResponse,
)

router = APIRouter(prefix="/cardapio", tags=["Cardápio"])


# =====================================================================
# GET: Filtro no banco para logista (vê apenas os seus)
# =====================================================================
@router.get("/", response_model=list[ItemCardapioResponse], status_code=status.HTTP_200_OK)
def listar_cardapio(
    categoria: str | None = Query(default=None),
    disponivel: bool | None = Query(default=None),
    busca: str | None = Query(default=None),
    preco_maximo: float | None = Query(default=None),
    sessao: Session = Depends(obter_sessao),
    usuario_logado: Cliente | None = Depends(obter_cliente_opcional),
):
    query = select(ItemCardapio)

    # Filtro no banco para logista
    if usuario_logado and usuario_logado.role == UserRole.LOGISTA:
        query = query.where(ItemCardapio.criador_id == usuario_logado.id)

    if preco_maximo:
        query = query.where(ItemCardapio.preco <= preco_maximo)
    if categoria:
        query = query.where(ItemCardapio.categoria == categoria)
    if disponivel is not None:
        query = query.where(ItemCardapio.disponivel == disponivel)
    if busca:
        termo = f"%{busca}%"
        query = query.where(
            or_(ItemCardapio.nome.ilike(termo), ItemCardapio.descricao.ilike(termo))
        )

    query = query.order_by(ItemCardapio.nome)
    return sessao.exec(query).all()


@router.get("/{item_id}", response_model=ItemCardapioResponse)
def obter_item(item_id: int, sessao: Session = Depends(obter_sessao)):
    item = sessao.get(ItemCardapio, item_id)
    if not item:
        raise HTTPException(status_code=404, detail=f"Item não localizado com id={item_id}.")
    return item


# =====================================================================
# POST: Vínculo automático do criador (usa a nova dependência)
# =====================================================================
@router.post(
    "/",
    response_model=ItemCardapioResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar novo item no cardápio (Apenas Logista)"
)
def criar_item(
    dados: ItemCardapioCreate,
    sessao: Session = Depends(obter_sessao),
    logista_logado: Cliente = Depends(verificar_permissao_cardapio),  # <-- TROCADO
):
    novo_item = ItemCardapio.model_validate(dados)
    novo_item.criador_id = logista_logado.id
    sessao.add(novo_item)
    sessao.commit()
    sessao.refresh(novo_item)
    return novo_item


# =====================================================================
# PUT: Apenas o dono do item (usa a nova dependência)
# =====================================================================
@router.put("/{item_id}", response_model=ItemCardapioResponse)
def atualizar_item(
    item_id: int,
    dados: ItemCardapioUpdate,
    sessao: Session = Depends(obter_sessao),
    logista_logado: Cliente = Depends(verificar_permissao_cardapio),  # <-- TROCADO
):
    item_banco = sessao.get(ItemCardapio, item_id)
    if not item_banco:
        raise HTTPException(status_code=404, detail=f"Item não localizado com id={item_id}.")
    if item_banco.criador_id != logista_logado.id:
        raise HTTPException(status_code=403, detail="Você só pode alterar itens que você mesmo criou.")

    dados_atualizados = dados.model_dump(exclude_unset=True)
    for campo, valor in dados_atualizados.items():
        setattr(item_banco, campo, valor)

    sessao.add(item_banco)
    sessao.commit()
    sessao.refresh(item_banco)
    return item_banco


# =====================================================================
# PATCH: Apenas o dono do item (usa a nova dependência)
# =====================================================================
@router.patch("/{item_id}/disponibilidade", response_model=ItemCardapioResponse)
def alternar_disponibilidade(
    item_id: int,
    sessao: Session = Depends(obter_sessao),
    logista_logado: Cliente = Depends(verificar_permissao_cardapio),  # <-- TROCADO
):
    item_banco = sessao.get(ItemCardapio, item_id)
    if not item_banco:
        raise HTTPException(status_code=404, detail=f"Item não localizado com id={item_id}.")
    if item_banco.criador_id != logista_logado.id:
        raise HTTPException(status_code=403, detail="Você só pode alterar itens que você mesmo criou.")

    item_banco.disponivel = not item_banco.disponivel
    sessao.add(item_banco)
    sessao.commit()
    sessao.refresh(item_banco)
    return item_banco


# =====================================================================
# DELETE: Apenas o dono do item (usa a nova dependência)
# =====================================================================
@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_item(
    item_id: int,
    sessao: Session = Depends(obter_sessao),
    logista_logado: Cliente = Depends(verificar_permissao_cardapio),  # <-- TROCADO
):
    item_banco = sessao.get(ItemCardapio, item_id)
    if not item_banco:
        raise HTTPException(status_code=404, detail=f"Item não localizado com id={item_id}.")
    if item_banco.criador_id != logista_logado.id:
        raise HTTPException(status_code=403, detail="Você só pode deletar itens que você mesmo criou.")

    sessao.delete(item_banco)
    sessao.commit()
    return None