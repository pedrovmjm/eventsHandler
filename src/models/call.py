from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, conint
from datetime import datetime

class Step(BaseModel):
    step_id:int
    description:str
    steps_status:str
    status_evidence:str
    customer_tone:str
    tone_explanation:str
    
class SentimentScore(BaseModel):
    sentiment:str
    score:int
    explanation:Optional[str]
    evidence:Optional[str]

class Sentiment(BaseModel):
    sentiment_scores:List[SentimentScore]
    
class SummarizeGeneral(BaseModel):
    ResumoChamanda: str
    ProblemasDuranteChamada: Optional[str]
    Insights:Optional[str]
    
class Summarize(BaseModel):
    summarize_general:List[SummarizeGeneral]

class Resolubilidade(BaseModel):
    Resolubilidade:str
    InsightsResolubilidade:str

class Solubility(BaseModel):
    resolubilidade:List[Resolubilidade]
    
class Call(BaseModel):
    data_criacao:datetime
    sn_id:str
    interation_id_talkdesk:str
    central:str
    unidade:str
    tipo:str
    nome_operador:str
    id_operador:str
    matriz_temas:str
    nota_talkdesk_csat: Optional[conint(gt=0, lt=5)]
    demanda_atendida: Optional[int]
    nome_instituicao:str
    nome_client:str
    descricao_resumida:str
    incidente:Optional[str]
    status_ligacao:str
    numero_destino:str
    numero_originador:str
    hora_inicio_chamada:datetime
    hora_termino_chamada:datetime
    nomes_csq:Optional[str]
    tempo_conversa:int
    tempo_toque:int
    tempo_fila:int
    agente_desligou:str
    transferencia:bool
    tipo_transferencia:Optional[str]
    tempo_total_s:int
    tempo_total:int
    id_chamada:str
    num_long_silence_s:float
    total_cliente_speech_s:float
    total_agent_speech_s:float
    steps:List[Step]
    sentiment:List[Sentiment]
    summarize:List[Summarize]
    solubility:List[Solubility]
    inferred_solubility:bool
    transcription:str
    inset_timestamp:int
    rn:int
    step_score:float
    num_issues:int
    issues_list:List[Any]
    