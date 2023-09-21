from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel


app = FastAPI()


class ComprarMilhas(BaseModel):
    milhas: int
    desconto: float
    bonus: float


valor_referencia = 70.0


def obter_desconto(desconto):
    return valor_referencia - (valor_referencia * (desconto / 100))

def obter_milhas_bonus(milhas_compradas, bonus):
    return milhas_compradas * (bonus / 100)


@app.post('/simulacao-compra')
def simulacao_compra(compra: ComprarMilhas):

    if (compra.milhas % 1000) != 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Só é possível comprar multiplos de 1000")
    
    if 0 > compra.desconto > 80:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="O descontos aceitos são somente de 0 a 80%")

    valor_com_desconto = obter_desconto(compra.desconto)
    milhas_bonus = obter_milhas_bonus(compra.milhas, compra.bonus)
    total_milhas = compra.milhas + milhas_bonus
    valor_total = (compra.milhas / 1000) * valor_com_desconto
    valor_final = valor_total / (total_milhas / 1000)

    return {
        "Valor Ref.": f"R$ {valor_referencia:.2f}/milheiro",
        "Milhas Comprar": compra.milhas,

        "Desconto": f"{compra.desconto:.0f}%",
        "Valor com desc.": f"R$ {valor_com_desconto:.2f}/milheiro",

        "Bônus": f"{compra.bonus:.0f}%",
        "Milhas de Bônus": f"{milhas_bonus:.0f}",

        "Milhas Totais": f"{total_milhas:.0f}",
        "Valor Total": f"R$ {valor_total:.2f}",

        "VALOR FINAL MILHEIRO": f">> R$ {valor_final:.2f} <<"
    }