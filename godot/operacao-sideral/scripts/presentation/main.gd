extends Control

const HP_MAX := 200
const PENALIDADE_ERRO := 10      # Sobrecarga (manual v2.1)
const PENALIDADE_TEMPO := 5      # Falha de Mira
const TEMPO_MS := 30_000         # dificuldade "Capitão" (proposta)
const ALERTA_MS := 5_000         # barra fica vermelha


@onready var pergunta: Label = %Pergunta
@onready var resposta: LineEdit = %Resposta
@onready var tempo: ProgressBar = %Tempo
@onready var rolar: Button = %Rolar
@onready var status: Label = %Status

var hp := HP_MAX
var d1 := 0
var d2 := 0
var mirando := false
var restante_ms := 0
var _sobra := 0.0

func _ready() -> void:
	rolar.pressed.connect(_on_rolar)
	resposta.text_submitted.connect(_on_resposta)   # Enter no LineEdit
	resposta.editable = false
	tempo.value = TEMPO_MS
	tempo.max_value = TEMPO_MS
	tempo.show_percentage = false
	_encerrar_mira()
	_mostrar_status("Aperte Rolar 2d12")

func _on_rolar() -> void:
	d1 = randi_range(1, 12)
	d2 = randi_range(1, 12)
	pergunta.text = "%d × %d = ?" % [d1, d2]
	resposta.text = ""
	resposta.editable = true
	resposta.grab_focus()            # cursor direto no campo
	
	# 1. DESABILITA o botão para impedir nova rolagem sem responder
	rolar.disabled = true
	restante_ms = TEMPO_MS
	_sobra = 0.0
	_atualizar_barra()
	mirando = true
	set_process(true)                # liga o relógio
	
	
func _on_resposta(texto: String) -> void:
	
	# Limpa espaços em branco ANTES de testar se é número
	var texto_digitado = texto.strip_edges()
	
	# Verifica se deu <ENTER> vazio (pune, limpa o campo e aborta a função)
	if texto_digitado.is_empty():
		hp -= PENALIDADE_ERRO
		_mostrar_status("Não pode fugir! -%d HP" % [PENALIDADE_ERRO])
		resposta.text = "" 
		return 
		
	# Verifica se tem letras (pune, limpa o campo e aborta a função)
	if not mirando or not texto_digitado.is_valid_int():
		hp -= PENALIDADE_ERRO
		_mostrar_status("Digite apenas números! -%d HP" % [PENALIDADE_ERRO])
		resposta.text = "" 
		return 
	_encerrar_mira()
		
	# Se chegou aqui, o jogador digitou um número válido!
	resposta.editable = false
	var correto := d1 * d2

	# Verifica se acertou a conta
	if texto_digitado.to_int() == correto:
		_mostrar_status("Acertou! Dano Bruto: %d" % correto)
	else:
		hp -= PENALIDADE_ERRO
		_mostrar_status("Sobrecarga! Era %d. -%d HP" % [correto, PENALIDADE_ERRO])

	if hp <= 0:
		rolar.disabled = true
	else :
		# 2. REABILITA o botão de rolar porque um valor válido foi inserido
		rolar.disabled = false
	
	# 3. (Opcional) Passa o foco de volta para o botão para facilitar
	# jogar apenas usando o teclado (digita -> enter -> enter pra rolar de novo)
	rolar.grab_focus()

func _process(delta: float) -> void:
	_sobra += delta * 1000.0
	var passo := int(_sobra)
	_sobra -= passo
	restante_ms = maxi(0, restante_ms - passo)
	_atualizar_barra()
	if restante_ms == 0:
		_encerrar_mira()
		_aplicar_dano(PENALIDADE_TEMPO, "Falha de Mira! Era %d." % (d1 * d2))



func _encerrar_mira() -> void:
	mirando = false
	set_process(false)               # desliga o relógio
	resposta.editable = false
	rolar.disabled = false

# Único ponto onde o HP muda.
func _aplicar_dano(valor: int, motivo: String) -> void:
	hp = maxi(0, hp - valor)
	if hp == 0:
		rolar.disabled = true
		_mostrar_status(motivo + " Nave destruída!")
	else:
		_mostrar_status("%s -%d HP" % [motivo, valor])

func _atualizar_barra() -> void:
	tempo.value = restante_ms
	tempo.modulate = Color.RED if restante_ms <= ALERTA_MS else Color.WHITE

func _mostrar_status(msg: String) -> void:
	status.text = "%s   |   HP %d/%d" % [msg, hp, HP_MAX]
