# SPEC MSX - Operacao Sideral

Documento vivo de execucao para a versao MSX de **Operacao Sideral - RPG
Matematico**, baseado no `GDD.md` v3.0.

O GDD e a fonte das regras. Este arquivo traduz essas regras para requisitos,
arquitetura e tarefas da versao MSX. Propostas do GDD permanecem marcadas como
`[PROPOSTA]` e nao devem ser implementadas como regras definitivas antes de
confirmacao.

Ao concluir uma tarefa, marque sua caixa com `[x]`. Quando uma decisao mudar,
atualize a secao correspondente e registre a alteracao no Historico de
decisoes.

## Estado atual

- **Fase atual:** Fase 1 - Adequacao da prova tecnica ao MSX2+
- **Ultimo marco concluido:** Bootstrap SCREEN 5 validado no MSX-DOS 2 com a
  configuracao anterior `Machine = "2"`
- **Proximo passo recomendado:** Alterar para `Machine = "2P"` e revalidar o
  `.COM` antes de criar a tela experimental
- **Bloqueios conhecidos:** As lacunas L1-L7 do GDD bloqueiam apenas as partes
  correspondentes; o Core comum e o Duelo podem avancar
- **Ultima atualizacao:** 2026-10-03

### Legenda

- `[ ]` Nao iniciado
- `[~]` Em andamento
- `[x]` Concluido
- `[!]` Bloqueado ou aguardando decisao

> Markdown nao possui um estado intermediario padrao para checkboxes. Os
> marcadores `[~]` e `[!]` sao convencoes deste documento.

## Objetivo

Criar a versao MSX de Operacao Sideral como um jogo educacional de combate por
turnos, usando C, SDCC e MSXgl, com separacao rigida entre:

1. **Core portatil:** regras, turnos, dados, RNG, cronometro, validacao
   matematica, atributos e condicoes de vitoria.
2. **Plataforma MSX:** video, entrada, audio, tempo, arquivos, Memory Mapper,
   bankswitching e integracao com MSXgl.
3. **Apresentacao:** telas, HUD, animacoes, efeitos e feedback educativo.

O Core nao pode depender de funcoes ou tipos exclusivos da MSXgl, nem armazenar
ponteiros para segmentos temporariamente mapeados.

## Plataforma-alvo

### Configuracao obrigatoria

- **Maquina:** MSX2+.
- **CPU:** Z80 a 3,58 MHz.
- **RAM:** 256 KB em Memory Mapper.
- **VRAM:** 128 KB.
- **VDP:** V9958.
- **Modo grafico inicial:** SCREEN 5, 256x212, 16 cores configuraveis.
- **Sistema:** MSX-DOS 2; Nextor deve ser aceito quando oferecer ambiente
  compativel.
- **Distribuicao:** executavel `.COM` acompanhado por arquivos de dados.
- **Target MSXgl:** `DOS2`.
- **Uso do Mapper:** segmentos alocados pela API `dos_mapper` e acessados por
  bankswitching em runtime.
- **Entrada:** teclado, teclado numerico e joysticks.
- **Audio-base:** PSG.
- **Sincronizacao:** PAL 50 Hz e NTSC 60 Hz.

### Melhorias opcionais

- MSX-MUSIC pode melhorar a trilha, mantendo PSG como fallback.
- Recursos adicionais de armazenamento podem reduzir trocas de arquivo, sem
  elevar o requisito minimo de 256 KB.
- Uma edicao futura em cartucho ROM exigira outro plano de memoria e nao faz
  parte desta especificacao.

### Justificativa tecnica

O MSX2+ preserva o VDP bitmap e acrescenta os recursos do V9958 como plataforma
minima desta versao. Os 256 KB do Memory Mapper permitem separar codigo, estado,
buffers, cache e dados carregados do disco. SCREEN 5 favorece os paineis e
ilustracoes bitmap da batalha. O formato MSX-DOS 2 `.COM` facilita atualizacoes,
arquivos de dados e saves sem reconstruir uma ROM.

O executavel deve manter residentes somente o loop principal, a infraestrutura
de plataforma e o Core necessario ao estado atual. Apresentacao, assets e dados
volumosos devem ocupar segmentos do Mapper substituiveis. Toda troca de segmento
deve passar por uma API unica, com restauracao explicita do mapeamento anterior.

## Regras confirmadas

### Atributos e limites

- [x] `HP <= 0` elimina a entidade.
- [x] Herois iniciam com 200 HP e nao podem ultrapassar 200 HP.
- [x] Chefes nao podem ultrapassar o HP inicial.
- [x] Escudo reduz o dano bruto, com dano real minimo igual a zero.
- [x] Sorte participa da esquiva: `d6 + Sorte >= 8`.
- [x] Cura modifica o Suporte Vital dos Herois e a Cura Automatica dos Chefes.
- [x] Cura excedente e descartada.

### Herois

| ID | Heroi | HP | Escudo | Sorte | Cura |
|---|---|---:|---:|---:|---:|
| `astro` | Astro-Enlatado | 200 | 15 | 1 | 2 |
| `ninja` | Ninja Sideral | 200 | 2 | 3 | 2 |
| `mago` | Mago Quantico | 200 | 5 | 2 | 8 |
| `barbaro` | Barbaro de Marte | 200 | 8 | 2 | 4 |
| `capitao` | Capitao Estelar | 200 | 10 | 1 | 6 |
| `rastreador` | Rastreador Cometa | 200 | 4 | 4 | 5 |

### Chefes

| ID | Chefe | HP | Escudo | Sorte | Cura |
|---|---|---:|---:|---:|---:|
| `nebulosa` | Nebulosa Fantasma | 300 | 10 | 3 | 15 |
| `tita` | Tita Cibernetico | 400 | 15 | 2 | 15 |
| `devorador` | O Devorador | 450 | 18 | 1 | 10 |
| `singularidade` | Singularidade Sombria | 600 | 5 | 1 | 20 |

### Penalidades e feedback

- [x] Resposta correta no tempo permite resolver o ataque.
- [x] Resposta errada causa Sobrecarga: ataque cancelado e 10 HP de dano direto
  no atacante, ignorando Escudo.
- [x] Tempo esgotado causa Falha de Mira: ataque cancelado e 5 HP de dano direto
  no atacante, ignorando Escudo.
- [x] Depois de erro ou timeout, mostrar a operacao e a resposta corretas antes
  de continuar.
- [x] O sistema atua como arbitro e valida resposta e tempo.

### Turno basico dos Herois

1. **Suporte Vital, 1d20**
   - 11-20: `HP = min(HPMax, HP + d20 + Cura)`.
   - 6-10: estabilidade, sem alteracao.
   - 1-5: `HP = HP - d20`.
2. **Canhao Principal, 2d12**
   - Gerar operandos de 1 a 12.
   - Solicitar `D1 x D2`.
   - Em acerto, `DanoBruto = D1 * D2`.
   - Em erro ou timeout, aplicar a penalidade e cancelar o ataque.
3. **Defesa / Esquiva, 1d6**
   - Se `d6 + Sorte >= 8`, o alvo evita todo o dano.
   - Caso contrario, `DanoReal = max(0, DanoBruto - EscudoAlvo)`.

Depois de qualquer alteracao de HP, o Core deve verificar eliminacao e condicao
de fim antes de iniciar a proxima fase.

### Modos da versao

#### Duelo

- Dois Herois em hot-seat.
- A ordem inicial e sorteada.
- Cada jogador executa o Turno Basico completo.
- O defensor realiza a fase de Defesa / Esquiva.
- Vence quem reduzir o HP do oponente a zero.

#### Co-op contra Chefe

- Dois Herois enfrentam um Chefe.
- Cada Heroi executa Suporte Vital e Canhao Principal.
- O Chefe testa Sorte Ativada contra cada ataque e aplica seu Escudo quando nao
  esquiva.
- No inicio do proprio turno, o Chefe recebe Cura Automatica limitada ao HP
  inicial.
- Ataque, ordem completa, controle e derrota dependem das lacunas L1-L5.

### Fora do escopo da v3.0

- Torneio.
- Mestre ou Chefe controlado por humano.
- Variante de Juiz.
- Protocolo de Emergencia.
- Ricochete Laser.
- Ataque sincronizado.
- Modos antigos A, B e C.

Esses itens nao devem deixar estados, eventos, telas ou codigo morto no Core
v3.0.

## Questoes em aberto do GDD

| ID | Questao | Estado no SPEC |
|---|---|---|
| L1 | Como o Chefe ataca | `[!]` Nao implementar ate confirmacao |
| L2 | Ordem da rodada Co-op | `[!]` Nao implementar ate confirmacao |
| L3 | Quem controla o Chefe | `[!]` Nao implementar ate confirmacao |
| L4 | Condicao de derrota no Co-op | `[!]` Nao implementar ate confirmacao |
| L5 | Numero de Herois no Co-op | `[!]` Estruturar dados para 2 sem cristalizar a regra |
| L6 | Duracao por dificuldade | `[!]` Timer configuravel; valores ainda sao proposta |
| L7 | Equilibrio do Rastreador Cometa | `[!]` Preservar atributos atuais e medir |
| L8 | Modos extras dos manuais antigos | Resolvido para v3.0: fora do escopo |

As propostas atuais do GDD podem orientar prototipos descartaveis, mas nao
testes normativos nem dados finais.

---

# Fase 0 - Consolidacao das regras

## 0.1. Converter regras confirmadas em dados

- [ ] Criar tabela dos seis Herois.
- [ ] Criar tabela dos quatro Chefes.
- [ ] Criar tabela de resultados do Suporte Vital.
- [ ] Criar tabela de penalidades de resposta.
- [ ] Criar tabela de fases do Duelo.
- [ ] Criar tabela das fases confirmadas do Co-op.
- [ ] Criar tabela de eliminacao, vitoria e derrota confirmadas.
- [ ] Identificar dados ajustaveis sem duplicar regras no codigo.

## 0.2. Isolar lacunas

- [ ] Representar duracao do timer como dado configuravel.
- [ ] Impedir que L1-L5 contaminem a maquina de estados comum.
- [ ] Reservar extensao explicita para o turno do Chefe.
- [ ] Documentar qualquer prototipo baseado em `[PROPOSTA]`.
- [ ] Remover do plano todos os mecanismos substituidos pelo GDD v3.0.

## Criterio de conclusao

- [ ] Toda regra confirmada do GDD tem representacao inequivoca.
- [ ] Nenhuma proposta e tratada como regra final.

---

# Fase 1 - Prova tecnica no MSX2+

## 1.1. Projeto MSXgl

- [x] Copiar a estrutura de `MSXgl\projects\template_msx2`.
- [!] Trocar `Machine = "2"` por `Machine = "2P"` no projeto existente.
- [x] Configurar `Target = "DOS2"`.
- [x] Habilitar as APIs de MSX-DOS 2 e Memory Mapper necessarias.
- [x] Habilitar somente os modulos MSXgl necessarios.
- [x] Configurar SCREEN 5.
- [x] Configurar build SDCC no Windows via WSL.
- [x] Configurar Emulicious.
- [x] Gerar o primeiro `.COM`.
- [x] Executar o `.COM` e validar o retorno ao DOS com ESC.
- [ ] Recompilar e repetir a validacao depois de selecionar `Machine = "2P"`.

Modulos iniciais previstos:

```text
system
bios
vdp
print
input
memory
math
game
fsm
dos_mapper
```

## 1.2. Tela experimental

- [ ] Desenhar fundo de painel espacial.
- [ ] Exibir uma nave aliada.
- [ ] Exibir um Chefe.
- [ ] Exibir HUD com HP, Escudo, Sorte e Cura.
- [ ] Exibir d20, 2d12 e d6.
- [ ] Exibir campo de resposta.
- [ ] Exibir barra ou contador de tempo.
- [ ] Exibir efeitos simples de ataque, esquiva e impacto.

## 1.3. VRAM e V9958

Plano inicial:

- **Pagina 0:** imagem visivel.
- **Pagina 1:** composicao da proxima imagem.
- **Pagina 2:** atlas de personagens e animacoes.
- **Pagina 3:** efeitos, dados, janelas e elementos temporarios.

Tarefas:

- [ ] Confirmar a divisao real das paginas em SCREEN 5.
- [ ] Testar copias de retangulos com comandos do VDP.
- [ ] Testar page flipping sem rasgos.
- [ ] Testar atualizacao parcial do HUD.
- [ ] Verificar espaco para tabelas e padroes de sprites.
- [ ] Registrar quais recursos do V9958 serao usados.

## 1.4. Memory Mapper e bankswitching

- [ ] Detectar e validar pelo menos 256 KB no Mapper.
- [ ] Alocar segmentos com `dos_mapper`.
- [ ] Mapear e restaurar um segmento de teste.
- [ ] Implementar guardas contra segmento invalido ou indisponivel.
- [ ] Medir custo de uma troca de segmento.
- [ ] Confirmar que interrupcoes nao observam um banco temporario incorreto.
- [ ] Validar acesso a arquivo durante o ciclo de carga de um segmento.

## 1.5. Desempenho

- [ ] Medir o tempo das copias principais do VDP.
- [ ] Validar entrada durante animacoes.
- [ ] Validar execucao em 50 Hz.
- [ ] Validar execucao em 60 Hz.
- [ ] Validar musica e efeitos durante animacoes.
- [ ] Validar bankswitching do Memory Mapper durante a apresentacao.
- [ ] Registrar limites encontrados.

## Criterio de conclusao

- [ ] A tela experimental funciona com resposta fluida em MSX2+, 256 KB de
  Memory Mapper e 128 KB de VRAM.
- [ ] O `.COM` aloca, troca e libera segmentos sem corromper o DOS ou o Core.
- [ ] O build usa `Machine = "2P"`, `Target = "DOS2"` e o modulo `dos_mapper`.

---

# Fase 2 - Arquitetura portatil

## 2.1. Estrutura inicial

```text
src/
  core/
    battle.c
    battle.h
    combatant.c
    combatant.h
    rules.c
    rules.h
    dice.c
    dice.h
    timer.c
    timer.h
    answer.c
    answer.h
    events.c
    events.h

  platform/
    msx/
      msx_main.c
      msx_input.c
      msx_video.c
      msx_audio.c
      msx_clock.c
      msx_mapper.c
      msx_assets.c

  presentation/
    screen_title.c
    screen_setup.c
    screen_battle.c
    screen_result.c
    hud.c
    animation.c
    dice_view.c
    answer_view.c

  data/
    heroes.c
    bosses.c
    difficulties.c
```

Tarefas:

- [ ] Criar diretorios.
- [ ] Criar headers publicos minimos.
- [ ] Definir tipos de largura fixa compativeis com SDCC e compilador nativo.
- [ ] Proibir includes da MSXgl dentro de `src\core`.
- [ ] Proibir ponteiros de Mapper nas estruturas do Core.

## 2.2. Comandos recebidos pelo Core

```text
COMMAND_CONFIRM
COMMAND_CANCEL
COMMAND_DIGIT
COMMAND_BACKSPACE
COMMAND_PAUSE
COMMAND_TICK
```

- [ ] Definir estrutura e dados associados a cada comando.
- [ ] Definir validacao de comandos por estado.
- [ ] Ignorar confirmacao duplicada sem duplicar resolucao.

## 2.3. Eventos produzidos pelo Core

```text
EVENT_DICE_ROLLED
EVENT_TIMER_STARTED
EVENT_ANSWER_CORRECT
EVENT_ANSWER_WRONG
EVENT_TIMEOUT
EVENT_DAMAGE
EVENT_HEAL
EVENT_DODGE
EVENT_ENTITY_DEFEATED
EVENT_BATTLE_FINISHED
```

- [ ] Definir a estrutura de evento.
- [ ] Implementar fila de capacidade fixa.
- [ ] Definir comportamento explicito para fila cheia.
- [ ] Garantir que eventos nao armazenem ponteiros dependentes de segmentos.

## 2.4. Tempo portatil

- [ ] Definir unidade inteira de tempo.
- [ ] Converter VBlanks PAL e NTSC para a unidade do Core.
- [ ] Pausar tempo durante transicoes e animacoes bloqueantes.
- [ ] Iniciar o tempo somente quando a entrada estiver liberada.
- [ ] Suportar limite configuravel e modo sem limite para validar L6.
- [ ] Testar duracao real equivalente em 50 e 60 Hz.

## 2.5. RNG deterministico

- [ ] Definir a interface de semente.
- [ ] Definir `Dice_Roll(sides)`.
- [ ] Garantir resultados inclusivos de 1 ate o numero de faces.
- [ ] Separar rolagem logica da animacao.
- [ ] Permitir repeticao de batalha com a mesma semente.

## Criterio de conclusao

- [ ] O Core compila sem MSXgl no SDCC e em compilador nativo.

---

# Fase 3 - Implementacao e testes do Core

## 3.1. Entidades

- [ ] Implementar identificador e tipo Heroi ou Chefe.
- [ ] Implementar `HPAtual`, `HPMax`, Escudo, Sorte e Cura.
- [ ] Implementar estado ativo ou eliminado.
- [ ] Implementar cura limitada a `HPMax`.
- [ ] Implementar dano mitigado por Escudo.
- [ ] Implementar dano direto que ignora Escudo.
- [ ] Verificar eliminacao depois de toda alteracao de HP.

## 3.2. Dados digitais

- [ ] Implementar d6.
- [ ] Implementar d12.
- [ ] Implementar d20.
- [ ] Testar limites e distribuicao.
- [ ] Registrar o resultado logico antes da animacao.

## 3.3. Validacao matematica

- [ ] Armazenar os dois operandos d12.
- [ ] Calcular produto entre 1 e 144.
- [ ] Receber digitos individualmente.
- [ ] Implementar apagar e confirmar.
- [ ] Impedir overflow e entradas invalidas.
- [ ] Resolver acerto, erro e timeout uma unica vez.
- [ ] Aplicar Sobrecarga de 10 HP como dano direto.
- [ ] Aplicar Falha de Mira de 5 HP como dano direto.
- [ ] Emitir dados para o feedback da resposta correta.

## 3.4. Estados comuns de batalha

```text
BATTLE_SETUP
TURN_BEGIN
SUPPORT_ROLL
SUPPORT_RESOLVE
ATTACK_ROLL
QUESTION_BEGIN
QUESTION_INPUT
QUESTION_RESOLVE
DODGE_ROLL
DAMAGE_RESOLVE
TURN_END
VICTORY_CHECK
BATTLE_END
```

- [ ] Implementar transicoes comuns.
- [ ] Implementar verificacao de eliminacao apos cada alteracao de HP.
- [ ] Verificar fim da batalha antes de iniciar outra fase.
- [ ] Impedir acoes de entidades eliminadas.
- [ ] Impedir transicoes e penalidades duplicadas.
- [ ] Manter extensao isolada para estados Co-op ainda nao confirmados.

## 3.5. Testes nativos

- [ ] Testar limites de d6, d12 e d20.
- [ ] Testar as tres faixas do Suporte Vital.
- [ ] Testar cura e limites de HP de Herois e Chefes.
- [ ] Testar resposta correta e dano bruto de 1 a 144.
- [ ] Testar resposta errada e Sobrecarga.
- [ ] Testar timeout e Falha de Mira.
- [ ] Testar timer sem limite como configuracao, sem tornar L6 definitiva.
- [ ] Testar Escudo e dano minimo zero.
- [ ] Testar dano direto.
- [ ] Testar todos os valores de Sorte.
- [ ] Testar eliminacao em todas as alteracoes de HP.
- [ ] Testar vitoria e derrota do Duelo.
- [ ] Testar Cura Automatica e Sorte Ativada confirmadas.
- [ ] Executar simulacoes deterministicas de batalha.

## Criterio de conclusao

- [ ] Todas as regras confirmadas possuem testes independentes da apresentacao.
- [ ] Nenhum teste normativo depende de uma proposta L1-L7.

---

# Fase 4 - Infraestrutura visual e de assets

## 4.1. Paleta

- [ ] Definir fundo quase preto.
- [ ] Definir azuis dos aliados.
- [ ] Definir vermelhos das ameacas.
- [ ] Definir amarelo dos dados e alertas.
- [ ] Definir verde de cura.
- [ ] Definir branco e cinzas de texto.
- [ ] Reservar cores para flashes.
- [ ] Verificar legibilidade em CRT e emulador.

O valor `#161b22` e uma referencia artistica e sera aproximado pela paleta do
V9958.

## 4.2. Pipeline de assets

- [ ] Definir formato-fonte em PNG.
- [ ] Definir paleta compartilhada.
- [ ] Configurar conversao com MSXtk.
- [ ] Configurar exportacao para SCREEN 5.
- [ ] Avaliar ZX0 e Pletter.
- [ ] Definir atlas por personagem.
- [ ] Definir metadados de animacao.
- [ ] Definir pacotes de assets para arquivos e segmentos do Mapper.

## 4.3. Estrategia de desenho

Usar bitmap e comandos do VDP para naves, Chefes, paineis, dados, explosoes e
animacoes grandes. Reservar sprites para cursor, mira, brilhos, projeteis,
alertas e efeitos sobrepostos.

- [ ] Definir e respeitar limite de sprites por linha.
- [ ] Implementar fila de comandos graficos.
- [ ] Implementar atualizacao por regioes sujas.
- [ ] Sincronizar troca de pagina com VBlank.
- [ ] Manter operacoes de Mapper fora da rotina de interrupcao.

## Criterio de conclusao

- [ ] O compositor desenha batalha, HUD e efeitos sem artefatos ou perda
  perceptivel de resposta.

---

# Fase 5 - Entrada e hot-seat

## 5.1. Entrada unificada

- [ ] Mapear teclado principal e numerico.
- [ ] Mapear joysticks 1 e 2.
- [ ] Converter entradas em comandos abstratos.
- [ ] Implementar repeticao controlada de direcao.
- [ ] Impedir confirmacao repetida acidental.

## 5.2. Entrada numerica

- [ ] Implementar digitos 0 a 9, apagar e confirmar.
- [ ] Implementar teclado numerico na tela.
- [ ] Permitir controle do teclado virtual por joystick.
- [ ] Exibir claramente a resposta atual.
- [ ] Aceitar respostas de 1 a 144.

## 5.3. Passagem hot-seat

- [ ] Mostrar o jogador atual.
- [ ] Criar tela curta de troca de jogador.
- [ ] Exigir confirmacao antes de liberar entrada.
- [ ] Iniciar o cronometro somente depois da confirmacao.
- [ ] Manter controles consistentes entre jogadores.

## Criterio de conclusao

- [ ] O Duelo pode ser controlado por uma pessoa de cada vez usando somente
  teclado ou somente joystick.

---

# Fase 6 - Vertical slice do Duelo

## 6.1. Telas minimas

- [ ] Abertura.
- [ ] Menu principal.
- [ ] Selecao de modo.
- [ ] Selecao de dificuldade.
- [ ] Selecao de dois Herois.
- [ ] Tela de batalha.
- [ ] Tela de resultado.
- [ ] Reiniciar ou voltar ao menu.

## 6.2. Turno completo

- [ ] Suporte Vital com d20.
- [ ] Cura, estabilidade ou curto-circuito.
- [ ] Canhao Principal com 2d12.
- [ ] Pergunta e cronometro.
- [ ] Resposta correta.
- [ ] Sobrecarga por resposta errada.
- [ ] Falha de Mira por timeout.
- [ ] Feedback educativo.
- [ ] Esquiva com d6.
- [ ] Calculo de dano e Escudo.
- [ ] Atualizacao do HUD.
- [ ] Troca de jogador.
- [ ] Vitoria e derrota.

## 6.3. Audiovisual inicial

- [ ] Duas naves aliadas representativas.
- [ ] Animacoes de d6, d12 e d20.
- [ ] Efeitos de ataque, impacto, esquiva e cura.
- [ ] Sons de rolagem, acerto, erro e dano.
- [ ] Musica provisoria.

## Criterio de conclusao

- [ ] Um Duelo completo pode ser jogado do menu ao resultado em MSX2+.

---

# Fase 7 - Co-op contra Chefe

## 7.1. Configuracao

- [ ] Selecionar dois Herois para o prototipo.
- [ ] Selecionar um dos quatro Chefes.
- [ ] Selecionar dificuldade.
- [ ] Identificar visualmente os dois jogadores.
- [!] Fixar quantidade final de Herois somente depois da decisao L5.

## 7.2. Fases confirmadas

- [ ] Executar o Turno Basico de cada Heroi.
- [ ] Rolar Sorte Ativada do Chefe para cada ataque.
- [ ] Aplicar Escudo do Chefe quando ele nao esquivar.
- [ ] Aplicar Cura Automatica no inicio do turno do Chefe.
- [ ] Limitar Cura Automatica ao HP inicial.
- [ ] Encerrar imediatamente se o Chefe for derrotado.

## 7.3. Fases bloqueadas

- [!] Implementar ataque do Chefe depois da decisao L1.
- [!] Fixar ordem da rodada depois da decisao L2.
- [!] Implementar controlador do Chefe depois da decisao L3.
- [!] Implementar derrota Co-op depois da decisao L4.

## 7.4. Balanceamento

- [ ] Simular duracao media por dupla e Chefe.
- [ ] Medir taxa de vitoria por dupla.
- [ ] Avaliar Cura, Escudo e Sorte dos quatro Chefes.
- [ ] Medir o Rastreador sem alterar atributos antes da decisao L7.
- [ ] Repetir as estatisticas quando L1-L7 forem resolvidas.

## Criterio de conclusao

- [ ] Partidas cooperativas completas funcionam contra os quatro Chefes, depois
  de L1-L5 serem confirmadas.

---

# Fase 8 - Arte, animacao e audio finais

## 8.1. Personagens

- [ ] Astro-Enlatado.
- [ ] Ninja Sideral.
- [ ] Mago Quantico.
- [ ] Barbaro de Marte.
- [ ] Capitao Estelar.
- [ ] Rastreador Cometa.
- [ ] Nebulosa Fantasma.
- [ ] Tita Cibernetico.
- [ ] O Devorador.
- [ ] Singularidade Sombria.
- [ ] Estados de dano, cura, esquiva e derrota.
- [ ] Icones ou retratos para selecao e HUD.

## 8.2. Dados

- [ ] Animacoes de d6, d12 e d20.
- [ ] Giro inicial, desaceleracao e resultado inequivoco.
- [ ] Som sincronizado.
- [ ] Opcao para acelerar animacoes.

## 8.3. Efeitos e audio

- [ ] Canhao Principal.
- [ ] Impacto no Escudo.
- [ ] Esquiva.
- [ ] Sobrecarga.
- [ ] Falha de Mira.
- [ ] Cura e Cura Automatica.
- [ ] Vitoria e derrota.
- [ ] Implementar musica e efeitos PSG.
- [ ] Atualizar audio durante VBlank.
- [ ] Avaliar MSX-MUSIC opcional.

## Criterio de conclusao

- [ ] Todo conteudo final cabe na distribuicao e pode ser carregado sem
  interromper animacoes, audio ou entrada.

---

# Fase 9 - Otimizacao

## 9.1. RAM

Manter residentes somente:

- Core e estado atual da batalha.
- Loop principal e infraestrutura de plataforma.
- Pilha e entrada matematica.
- Fila de eventos.
- Estado minimo das animacoes.
- Dados descomprimidos necessarios no momento.

Tarefas:

- [ ] Gerar mapa de memoria.
- [ ] Medir pilha maxima e dados globais.
- [ ] Remover buffers duplicados.
- [ ] Medir TPA usado pelo `.COM` e pelo MSX-DOS 2.
- [ ] Confirmar execucao com exatamente 256 KB de Memory Mapper.

## 9.2. Segmentos do Mapper e arquivos

Organizacao prevista:

- Segmentos residentes de Core e loop.
- Segmentos substituiveis de apresentacao.
- Segmentos reutilizaveis de descompressao e cache.
- Pacotes de interface, Herois, Chefes, musica e efeitos.

Tarefas:

- [ ] Definir mapa de segmentos e slots.
- [ ] Centralizar bankswitching em `msx_mapper`.
- [ ] Salvar e restaurar o segmento anterior em toda troca.
- [ ] Impedir ponteiros permanentes para segmentos substituiveis.
- [ ] Evitar troca de segmento em interrupcoes.
- [ ] Criar API unica para carregar assets.
- [ ] Criar formato indexado para pacotes de dados.
- [ ] Tratar explicitamente erros de arquivo e falta de memoria.
- [ ] Gerar relatorio de ocupacao por segmento e arquivo.

## 9.3. CPU e VDP

- [ ] Remover ponto flutuante.
- [ ] Evitar divisoes em loops de animacao.
- [ ] Pre-calcular tabelas pequenas.
- [ ] Usar comandos do VDP para copia e preenchimento.
- [ ] Atualizar somente regioes alteradas.
- [ ] Separar tick de logica e frame de apresentacao.
- [ ] Permitir animacoes a 25/30 Hz quando necessario.
- [ ] Manter entrada e audio a 50/60 Hz.

## 9.4. Compatibilidade

- [ ] Testar MSX2+ PAL.
- [ ] Testar MSX2+ NTSC.
- [ ] Testar MSX2+ com exatamente 256 KB de RAM.
- [ ] Testar MSX2+ com mais de 256 KB de RAM.
- [ ] Testar MSX-DOS 2.
- [ ] Testar Nextor compativel.
- [ ] Testar teclado e joystick reais ou equivalentes.

## Criterio de conclusao

- [ ] O jogo cumpre os limites de memoria e mantem interacao fluida no MSX2+
  minimo definido.

---

# Fase 10 - Qualidade e acessibilidade infantil

## 10.1. Clareza visual

- [ ] Usar fonte grande e legivel.
- [ ] Limitar texto por tela.
- [ ] Destacar claramente o jogador atual.
- [ ] Usar cores consistentes por evento.
- [ ] Avisar antes de iniciar o cronometro.
- [ ] Nao depender somente de cor.

## 10.2. Dificuldade

- [!] Fixar tempos somente depois da decisao L6.
- [ ] Permitir configuracao de ajuda visual.
- [ ] Configurar velocidade das animacoes.
- [ ] Avaliar grade de multiplicacao no nivel facil.
- [ ] Manter sempre operandos dentro da tabuada de 1 a 12.

## 10.3. Feedback educativo

- [ ] Mostrar operacao e resultado corretos depois de erro.
- [ ] Mostrar operacao e resultado corretos depois de timeout.
- [ ] Explicar a penalidade sem linguagem excessivamente punitiva.
- [ ] Dar tempo para a crianca ler.
- [ ] Permitir confirmacao antes de continuar.

## Criterio de conclusao

- [ ] Criancas entendem turno, pergunta, resultado e consequencia sem
  orientacao constante de um adulto.

---

# Fase 11 - Empacotamento e lancamento

## 11.1. Build reproduzivel

- [ ] Gerar executavel `.COM`.
- [ ] Gerar pacotes de dados.
- [ ] Gerar imagem de disco ou diretorio de distribuicao.
- [ ] Gerar simbolos de depuracao.
- [ ] Gerar mapa de memoria.
- [ ] Gerar relatorio por segmento e arquivo.
- [ ] Identificar versao na tela de creditos.
- [ ] Documentar o comando de build.
- [ ] Garantir build limpo em outra maquina Windows.

## 11.2. Testes finais

- [ ] Testar todas as dificuldades confirmadas.
- [ ] Testar os seis Herois.
- [ ] Testar os quatro Chefes.
- [ ] Testar Duelo e Co-op.
- [ ] Testar acerto, erro e timeout.
- [ ] Testar eliminacao por Suporte Vital, Sobrecarga e Falha de Mira.
- [ ] Testar esquiva e Escudo.
- [ ] Testar vitoria por ataque.
- [ ] Testar derrota conforme regras finais do Co-op.
- [ ] Testar todos os caminhos de erro de arquivo e Mapper.

## 11.3. Hardware real

- [ ] Testar em ao menos um MSX2+ real com 256 KB.
- [ ] Testar em SD, flashcart ou armazenamento equivalente.
- [ ] Testar carregamento pelo MSX-DOS 2.
- [ ] Testar em Nextor compativel.
- [ ] Conferir cores, audio, teclado e joystick.
- [ ] Comparar PAL e NTSC.

## Criterio de conclusao

- [ ] O pacote final pode ser instalado, executado e jogado integralmente em
  emuladores e hardware MSX2+ real.

---

# Marcos do projeto

- [x] **M0 - Pesquisa:** GDD e MSXgl estudados.
- [ ] **M1 - Prova tecnica:** DOS2, SCREEN 5, Mapper, entrada e animacao
  validados no MSX2+.
- [ ] **M2 - Core:** regras confirmadas compilam e passam em testes nativos.
- [ ] **M3 - Duelo:** modo jogavel do menu ao resultado.
- [ ] **M4 - Cooperativo:** Co-op completo depois da resolucao de L1-L5.
- [ ] **M5 - Conteudo:** personagens, efeitos e audio finais integrados.
- [ ] **M6 - Release candidate:** desempenho, compatibilidade e QA concluidos.
- [ ] **M7 - Lancamento:** pacote MSX-DOS 2 validado em MSX2+ real.

# Procedimento de retomada

1. Ler `GDD.md`.
2. Ler "Estado atual", "Questoes em aberto" e "Historico de decisoes".
3. Confirmar que nenhuma `[PROPOSTA]` virou regra sem atualizacao do GDD.
4. Localizar a primeira tarefa `[~]`; se nao houver, localizar a primeira `[ ]`
   da fase atual.
5. Consultar o ultimo commit e alteracoes nao commitadas.
6. Executar o menor build ou teste que confirme o estado registrado.
7. Atualizar "Estado atual" antes de iniciar nova fase.
8. Ao terminar, marcar tarefas, registrar decisoes e indicar o proximo passo.

# Registro de validacoes

| Data | Fase | Ambiente | Comando ou teste | Resultado |
|---|---|---|---|---|
| 2026-10-03 | Pesquisa | Repositorio | Leitura do GDD e MSXgl | Concluido |

# Historico de decisoes

| Data | Decisao | Motivo |
|---|---|---|
| 2026-10-03 | Usar dados digitais | Integracao direta com regras e animacoes |
| 2026-10-03 | Usar multijogador hot-seat | Todos compartilham os controles |
| 2026-10-03 | Manter timer configuravel, inclusive sem limite enquanto L6 estiver aberta | Acessibilidade sem cristalizar a proposta |
| 2026-10-03 | Exigir MSX2+ com 256 KB de Memory Mapper | Plataforma-alvo confirmada |
| 2026-10-03 | Iniciar com SCREEN 5 | Equilibrio para arte bitmap e batalha |
| 2026-10-03 | Distribuir como MSX-DOS 2 `.COM` com target `DOS2` | Permite arquivos e API `dos_mapper` |
| 2026-10-03 | Usar bankswitching do Memory Mapper, nao bancos de ROM | O produto principal e um `.COM`, nao cartucho |
| 2026-10-03 | Substituir regras antigas pelo GDD v3.0 | O GDD atual e a fonte unica para a versao MSX |
