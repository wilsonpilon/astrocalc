# SPEC MSX - Matematica nas Estrelas

Documento vivo de execucao para a versao MSX de **Matematica nas Estrelas**.

Este arquivo deve ser atualizado durante o desenvolvimento. Ao concluir uma
tarefa, marque sua caixa com `[x]`. Quando uma decisao mudar, atualize a secao
correspondente e registre a alteracao no Historico de decisoes.

## Estado atual

- **Fase atual:** Fase 1 - Prova tecnica no MSX2
- **Ultimo marco concluido:** Bootstrap SCREEN 5 validado no MSX-DOS 2
- **Proximo passo recomendado:** Criar a tela experimental de batalha
- **Bloqueios conhecidos:** Regras pendentes bloqueiam o Core, mas nao a prova
  tecnica
- **Ultima atualizacao:** 2026-10-03

### Legenda

- `[ ]` Nao iniciado
- `[~]` Em andamento
- `[x]` Concluido
- `[!]` Bloqueado ou aguardando decisao

> Markdown nao possui um estado intermediario padrao para checkboxes. Os
> marcadores `[~]` e `[!]` sao convencoes deste documento.

## Objetivo

Criar um jogo educacional de combate por turnos para MSX2 usando C, SDCC e
MSXgl, preservando uma separacao rigida entre:

1. **Core portatil:** regras, turnos, dados, RNG, cronometros, validacao
   matematica, atributos e condicoes de vitoria.
2. **Plataforma MSX:** video, entrada, audio, tempo, arquivos, RAM Mapper e
   integracao com MSXgl.
3. **Apresentacao:** telas, HUD, animacoes, efeitos e feedback educativo.

O Core nao pode depender de funcoes ou tipos exclusivos da MSXgl.

## Plataforma-alvo

### Configuracao-base

- **Maquina:** MSX2.
- **CPU:** Z80 a 3,58 MHz como referencia minima.
- **RAM:** 256 KB de Memory Mapper.
- **VRAM:** 128 KB.
- **Modo grafico:** SCREEN 5, 256x212, 16 cores configuraveis.
- **Sistema:** MSX-DOS 2 ou Nextor.
- **Distribuicao:** executavel `.COM` com arquivos de dados.
- **Target MSXgl:** `DOS2`.
- **Uso do Mapper:** segmentos alocados em runtime pela API `dos_mapper`.
- **Entrada:** teclado, teclado numerico e joysticks.
- **Audio-base:** PSG.
- **Sincronizacao:** PAL 50 Hz e NTSC 60 Hz.

### Melhorias opcionais

- MSX2+ pode receber melhorias visuais, mas nao deve ser requisito.
- MSX-MUSIC pode melhorar a trilha, mantendo PSG como fallback.
- Uma edicao em cartucho ROM pode ser avaliada posteriormente sem alterar o
  Core.

### Justificativa tecnica

Os 128 KB de VRAM e o VDP V9938 sustentam os graficos. Os 256 KB do Memory
Mapper permitem separar codigo, buffers, cache e dados carregados do disco.
SCREEN 5 e preferivel a SCREEN 4 porque a batalha usa paineis e ilustracoes
bitmap, sem scrolling continuo baseado em tiles. O formato DOS2 facilita
atualizacoes, arquivos de save e carregamento de assets sem reconstruir uma ROM.

## Decisoes confirmadas

- [x] O jogo usa dados digitais gerados pelo Core.
- [x] O combate e por turnos.
- [x] O multijogador e hot-seat, compartilhando os controles.
- [x] O cronometro varia por dificuldade.
- [x] Dificuldades faceis podem desabilitar o cronometro.
- [x] MSX2 e a plataforma-base.
- [x] Recursos de MSX2+ sao opcionais.
- [x] SCREEN 5 e a direcao tecnica inicial.
- [x] A logica deve ser portatil e independente da apresentacao.
- [x] A distribuicao principal sera MSX-DOS 2 `.COM`.
- [x] O target MSXgl sera `DOS2`.
- [x] O alvo de RAM sera um Memory Mapper de 256 KB.

## Questoes em aberto

- [!] Definir a tabela final de dificuldades e tempos.
- [!] Definir explicitamente o erro do Mestre no Modo C.
- [!] Definir se cada etapa aceita somente uma submissao.
- [!] Definir o arredondamento do meio dano no Modo B.
- [!] Definir HP maximo e limite de cura.
- [!] Definir a ordem exata de eliminacao, retaliacao, cura e vitoria.
- [!] Decidir se a variante de Juiz permanece no torneio do Modo A.

---

# Fase 0 - Consolidacao das regras

## 0.1. Fechar decisoes pendentes

- [ ] Definir dificuldades e duracao do cronometro.
- [ ] Definir o comportamento quando o cronometro estiver desabilitado.
- [ ] Definir o comportamento do Chefe humano ao errar no Modo C.
- [ ] Definir quantas respostas podem ser submetidas em cada tentativa.
- [ ] Definir o arredondamento do dano reduzido no Protocolo de Emergencia.
- [ ] Adicionar `HPAtual` e `HPMax`, ou confirmar que a cura e ilimitada.
- [ ] Definir verificacoes de morte depois de cada alteracao de HP.
- [ ] Definir se um Chefe derrotado pode retaliar ou regenerar.
- [ ] Decidir o destino da variante de Juiz.

## 0.2. Converter regras em tabelas

- [ ] Criar tabela de herois.
- [ ] Criar tabela de chefes.
- [ ] Criar tabela de dificuldades.
- [ ] Criar tabela de tipos de dano.
- [ ] Criar tabela de fases do Modo A.
- [ ] Criar tabela de fases do Modo B.
- [ ] Criar tabela de fases do Modo C.
- [ ] Criar tabela de vitoria, derrota e eliminacao.

## Criterio de conclusao

- [ ] Nenhuma transicao de combate depende de interpretacao durante a
  implementacao.

---

# Fase 1 - Prova tecnica no MSX2

## 1.1. Criar projeto MSXgl

- [x] Copiar a estrutura de `MSXgl\projects\template_msx2`.
- [x] Configurar `Machine = "2"`.
- [x] Configurar `Target = "DOS2"`.
- [x] Habilitar as APIs de MSX-DOS 2 e RAM Mapper necessarias.
- [x] Habilitar somente os modulos MSXgl necessarios.
- [x] Configurar SCREEN 5.
- [x] Configurar build SDCC no Windows via WSL.
- [x] Configurar Emulicious.
- [x] Gerar o primeiro `.COM`.
- [x] Executar o `.COM` e validar o retorno ao DOS com ESC.

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
```

## 1.2. Criar tela experimental

- [ ] Desenhar fundo de painel espacial.
- [ ] Exibir uma nave aliada.
- [ ] Exibir um chefe.
- [ ] Exibir HUD com HP, Escudo, Sorte e Cura.
- [ ] Exibir dois dados animados.
- [ ] Exibir campo de resposta.
- [ ] Exibir barra ou contador de tempo.
- [ ] Exibir um efeito simples de ataque.

## 1.3. Validar o uso da VRAM

Plano inicial:

- **Pagina 0:** imagem visivel.
- **Pagina 1:** composicao da proxima imagem.
- **Pagina 2:** atlas de personagens e animacoes.
- **Pagina 3:** efeitos, dados, janelas e elementos temporarios.

Tarefas:

- [ ] Confirmar a divisao real das paginas no modo escolhido.
- [ ] Testar copias de retangulos com comandos do VDP.
- [ ] Testar page flipping sem rasgos.
- [ ] Testar atualizacao parcial do HUD.
- [ ] Verificar espaco para tabelas e padroes de sprites.

## 1.4. Medir desempenho

- [ ] Medir o tempo das copias principais do VDP.
- [ ] Validar entrada durante animacoes.
- [ ] Validar execucao em 50 Hz.
- [ ] Validar execucao em 60 Hz.
- [ ] Validar musica e efeitos durante animacoes.
- [ ] Validar troca de bancos da ROM.
- [ ] Registrar limites encontrados.

## Criterio de conclusao

- [ ] A tela de batalha experimental funciona com animacoes fluidas em um
  MSX2 com 256 KB de RAM Mapper e 128 KB de VRAM.

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

## 2.2. Comandos recebidos pelo Core

```text
COMMAND_CONFIRM
COMMAND_CANCEL
COMMAND_DIGIT
COMMAND_BACKSPACE
COMMAND_PAUSE
COMMAND_TICK
```

- [ ] Definir a estrutura de comando.
- [ ] Definir dados associados a cada comando.
- [ ] Definir validacao de comandos por estado.

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
- [ ] Implementar fila de eventos com capacidade fixa.
- [ ] Definir comportamento em caso de fila cheia.
- [ ] Garantir que eventos nao armazenem ponteiros dependentes de bancos.

## 2.4. Tempo portatil

- [ ] Definir unidade inteira de tempo.
- [ ] Converter VBlanks PAL e NTSC para a unidade do Core.
- [ ] Pausar o tempo durante transicoes e animacoes bloqueantes.
- [ ] Iniciar o tempo somente quando a entrada estiver liberada.
- [ ] Testar o mesmo tempo real em 50 e 60 Hz.

## 2.5. RNG deterministico

- [ ] Definir a interface de semente.
- [ ] Definir `Dice_Roll(sides)`.
- [ ] Garantir resultados inclusivos de 1 ate o numero de faces.
- [ ] Separar rolagem logica da animacao visual.
- [ ] Permitir repeticao de batalha usando a mesma semente.

## Criterio de conclusao

- [ ] O Core compila sem MSXgl tanto no SDCC quanto em compilador nativo.

---

# Fase 3 - Implementacao e testes do Core

## 3.1. Entidades

- [ ] Implementar identificador de entidade.
- [ ] Implementar tipo Heroi ou Chefe.
- [ ] Implementar `HPAtual`.
- [ ] Implementar `HPMax`.
- [ ] Implementar Escudo.
- [ ] Implementar Sorte.
- [ ] Implementar Cura.
- [ ] Implementar estado ativo ou eliminado.
- [ ] Implementar cura com limite.
- [ ] Implementar dano com limite minimo de zero.

## 3.2. Dados digitais

- [ ] Implementar d6.
- [ ] Implementar d10.
- [ ] Implementar d20.
- [ ] Testar limites e distribuicao.
- [ ] Registrar o resultado logico antes da animacao.

## 3.3. Validacao matematica

- [ ] Armazenar os operandos.
- [ ] Calcular a resposta correta.
- [ ] Receber digitos individualmente.
- [ ] Implementar apagar.
- [ ] Implementar confirmar.
- [ ] Impedir overflow e entradas invalidas.
- [ ] Implementar acerto.
- [ ] Implementar erro.
- [ ] Implementar timeout.
- [ ] Implementar Protocolo de Emergencia.

## 3.4. Estados gerais de batalha

```text
BATTLE_SETUP
ROUND_BEGIN
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
ROUND_END
VICTORY_CHECK
BATTLE_END
```

- [ ] Implementar transicoes comuns.
- [ ] Implementar verificacao de eliminacao apos alteracoes de HP.
- [ ] Implementar verificacao de vitoria antes de retaliacao ou regeneracao.
- [ ] Impedir acoes de entidades eliminadas.
- [ ] Impedir transicoes duplicadas.

## 3.5. Testes nativos

- [ ] Testar limites de todos os dados.
- [ ] Testar resposta correta.
- [ ] Testar resposta errada.
- [ ] Testar timeout.
- [ ] Testar cronometro desabilitado.
- [ ] Testar cura e HP maximo.
- [ ] Testar escudo.
- [ ] Testar dano direto.
- [ ] Testar esquiva.
- [ ] Testar eliminacao durante o turno.
- [ ] Testar ordem de retaliacao.
- [ ] Testar ordem de regeneracao.
- [ ] Testar vitoria e derrota.
- [ ] Executar simulacoes automatizadas de batalhas.

## Criterio de conclusao

- [ ] Todas as regras do GDD possuem testes independentes da apresentacao.

---

# Fase 4 - Infraestrutura visual

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
V9938.

## 4.2. Pipeline de assets

- [ ] Definir formato-fonte em PNG.
- [ ] Definir paleta compartilhada.
- [ ] Configurar conversao com MSXtk.
- [ ] Configurar exportacao para SCREEN 5.
- [ ] Avaliar ZX0 e Pletter.
- [ ] Definir atlas por personagem.
- [ ] Definir metadados de animacao.
- [ ] Definir distribuicao dos assets nos bancos da ROM.

## 4.3. Estrategia de desenho

Usar bitmap e comandos do VDP para:

- Naves grandes.
- Chefes.
- Paineis.
- Dados.
- Explosoes grandes.
- Animacoes de dano e cura.

Reservar sprites para:

- Cursor.
- Mira.
- Brilhos.
- Pequenos projeteis.
- Alertas.
- Efeitos sobrepostos.

Tarefas:

- [ ] Definir limite de sprites por linha.
- [ ] Evitar composicoes que ultrapassem esse limite.
- [ ] Implementar fila de comandos graficos.
- [ ] Implementar atualizacao por regioes sujas.
- [ ] Sincronizar troca de pagina com VBlank.

## Criterio de conclusao

- [ ] O compositor desenha batalha, HUD e efeitos sem artefatos ou quedas
  perceptiveis de resposta.

---

# Fase 5 - Entrada e hot-seat

## 5.1. Entrada unificada

- [ ] Mapear teclado principal.
- [ ] Mapear teclado numerico.
- [ ] Mapear joystick 1.
- [ ] Mapear joystick 2.
- [ ] Converter todos em comandos abstratos.
- [ ] Implementar repeticao controlada de direcao.
- [ ] Implementar clique e confirmacao sem repeticao acidental.

## 5.2. Entrada numerica

- [ ] Implementar digitos 0 a 9.
- [ ] Implementar apagar.
- [ ] Implementar confirmar.
- [ ] Implementar teclado numerico na tela.
- [ ] Permitir controle do teclado virtual por joystick.
- [ ] Exibir claramente a resposta atual.

## 5.3. Passagem hot-seat

- [ ] Mostrar o jogador atual.
- [ ] Criar tela curta de troca de jogador.
- [ ] Exigir confirmacao antes de iniciar.
- [ ] Iniciar o cronometro somente depois da confirmacao.
- [ ] Manter os controles consistentes entre jogadores.

## Criterio de conclusao

- [ ] Todos os modos podem ser controlados por uma unica pessoa de cada vez
  usando apenas teclado ou apenas joystick.

---

# Fase 6 - Vertical slice do Modo A

## 6.1. Telas minimas

- [ ] Abertura.
- [ ] Menu principal.
- [ ] Selecao de modo.
- [ ] Selecao de dificuldade.
- [ ] Selecao de dois herois.
- [ ] Tela de batalha.
- [ ] Tela de resultado.
- [ ] Reiniciar ou voltar ao menu.

## 6.2. Turno completo

- [ ] Suporte Vital.
- [ ] Animacao do d20.
- [ ] Cura ou falha critica.
- [ ] Rolagem de 2d10.
- [ ] Pergunta.
- [ ] Cronometro.
- [ ] Resposta correta.
- [ ] Resposta errada.
- [ ] Timeout.
- [ ] Ricochete Laser.
- [ ] Esquiva.
- [ ] Calculo de dano.
- [ ] Atualizacao do HUD.
- [ ] Troca de jogador.
- [ ] Vitoria e derrota.

## 6.3. Audiovisual inicial

- [ ] Uma nave aliada final ou quase final.
- [ ] Um oponente visual.
- [ ] Efeito de ataque.
- [ ] Efeito de impacto.
- [ ] Efeito de cura.
- [ ] Som de rolagem.
- [ ] Som de acerto.
- [ ] Som de erro.
- [ ] Som de dano.
- [ ] Musica provisoria.

## Criterio de conclusao

- [ ] Um duelo completo pode ser jogado do menu ao resultado em MSX2.

---

# Fase 7 - Modo B

## 7.1. Configuracao cooperativa

- [ ] Selecionar dois herois.
- [ ] Selecionar um chefe.
- [ ] Selecionar dificuldade.
- [ ] Identificar visualmente os dois jogadores.

## 7.2. Ataque sincronizado

- [ ] Rolar um d10 por heroi.
- [ ] Receber resposta conjunta.
- [ ] Resolver a primeira tentativa.
- [ ] Iniciar Protocolo de Emergencia.
- [ ] Aplicar timer de cinco segundos.
- [ ] Aplicar dano reduzido.
- [ ] Aplicar Ricochete aos dois em falha final.

## 7.3. IA do Chefe

- [ ] Retaliar depois do ataque quando permitido.
- [ ] Resolver esquivas individualmente.
- [ ] Aplicar dano direto.
- [ ] Regenerar na fase correta.
- [ ] Encerrar imediatamente se o Chefe for derrotado.

## 7.4. Balanceamento

- [ ] Simular duracao media.
- [ ] Medir taxa de vitoria por dupla.
- [ ] Avaliar efeito dos escudos.
- [ ] Avaliar regeneracao contra dano reduzido.
- [ ] Ajustar chefes impossiveis ou triviais.

## Criterio de conclusao

- [ ] Partidas cooperativas completas funcionam contra os tres chefes.

---

# Fase 8 - Modo C

## 8.1. Turnos dos Herois

- [ ] Executar Folego.
- [ ] Executar ataque matematico.
- [ ] Resolver dano.
- [ ] Verificar eliminacao.
- [ ] Passar ao proximo heroi ativo.

## 8.2. Turno do Mestre

- [ ] Confirmar troca hot-seat.
- [ ] Regenerar o Chefe.
- [ ] Rolar 2d10.
- [ ] Apresentar pergunta.
- [ ] Executar cronometro.
- [ ] Resolver acerto, erro ou timeout.
- [ ] Rolar esquivas individualmente.
- [ ] Aplicar dano em area.

## 8.3. Participantes eliminados

- [ ] Pular turnos de Herois eliminados.
- [ ] Encerrar se todos os Herois forem eliminados.
- [ ] Encerrar imediatamente se o Chefe for eliminado.
- [ ] Diferenciar participantes eliminados no HUD.

## Criterio de conclusao

- [ ] O Modo C funciona integralmente usando o mesmo Core dos demais modos.

---

# Fase 9 - Arte, animacao e audio finais

## 9.1. Personagens

- [ ] Capitao Estelar.
- [ ] Sombra Neon.
- [ ] Tecnomago.
- [ ] Saqueador Espacial.
- [ ] Ciborgue Titanio.
- [ ] Devorador de Planetas.
- [ ] Nebulosa Fantasma.
- [ ] Tita Cibernetico.
- [ ] Estados de dano, cura e derrota.
- [ ] Icones ou retratos para selecao e HUD.

## 9.2. Dados

- [ ] Animacao de d6.
- [ ] Animacao de d10.
- [ ] Animacao de d20.
- [ ] Giro inicial.
- [ ] Desaceleracao.
- [ ] Resultado final inequivoco.
- [ ] Som sincronizado.
- [ ] Opcao para acelerar animacoes.

## 9.3. Efeitos

- [ ] Laser.
- [ ] Impacto no escudo.
- [ ] Esquiva.
- [ ] Ricochete.
- [ ] Sobrecarga.
- [ ] Cura.
- [ ] Regeneracao.
- [ ] Vitoria.
- [ ] Derrota.

## 9.4. Audio

- [ ] Escolher formato da musica.
- [ ] Implementar musica PSG.
- [ ] Implementar efeitos PSG.
- [ ] Atualizar player durante VBlank.
- [ ] Adicionar volume ou liga/desliga quando viavel.
- [ ] Avaliar MSX-MUSIC opcional.

## Criterio de conclusao

- [ ] Todo conteudo final cabe no pacote de distribuicao e pode ser carregado
  sem interromper animacoes ou entrada.

---

# Fase 10 - Otimizacao

## 10.1. RAM

Manter na RAM somente:

- Estado da batalha.
- Pilha.
- Entrada matematica.
- Fila de eventos.
- Estado das animacoes.
- Dados descomprimidos necessarios no momento.

Tarefas:

- [ ] Gerar mapa de memoria.
- [ ] Medir pilha maxima.
- [ ] Medir dados globais.
- [ ] Remover buffers duplicados.
- [ ] Medir segmentos usados pelo programa e pelo MSX-DOS 2.
- [ ] Confirmar execucao com Memory Mapper de 256 KB.

## 10.2. Segmentos do Mapper e arquivos

Organizacao prevista:

- Segmentos residentes para Core e loop.
- Segmentos de apresentacao.
- Segmentos reutilizaveis para descompressao e cache.
- Pacote de interface.
- Pacote de Herois.
- Pacote de Chefes.
- Pacote de musica e efeitos.

Tarefas:

- [ ] Definir mapa de segmentos.
- [ ] Impedir ponteiros permanentes para segmentos temporarios.
- [ ] Evitar troca de segmento em interrupcoes.
- [ ] Criar API unica para carregar assets.
- [ ] Criar formato indexado para pacotes de dados.
- [ ] Tratar erros de arquivo e falta de memoria explicitamente.
- [ ] Gerar relatorio de ocupacao por segmento.

## 10.3. CPU e VDP

- [ ] Remover ponto flutuante.
- [ ] Evitar divisoes em loops de animacao.
- [ ] Pre-calcular tabelas pequenas.
- [ ] Usar comandos do VDP para copia e preenchimento.
- [ ] Atualizar apenas regioes alteradas.
- [ ] Separar tick de logica e frame de apresentacao.
- [ ] Permitir animacoes a 25/30 Hz se necessario.
- [ ] Manter entrada e audio a 50/60 Hz.

## 10.4. Compatibilidade

- [ ] Testar MSX2 PAL.
- [ ] Testar MSX2 NTSC.
- [ ] Testar MSX2 com 256 KB de RAM.
- [ ] Testar MSX2 com mais de 256 KB de RAM.
- [ ] Testar MSX2+.
- [ ] Testar MSX-DOS 2.
- [ ] Testar Nextor.
- [ ] Testar teclado.
- [ ] Testar joystick real ou equivalente.

## Criterio de conclusao

- [ ] O jogo cumpre os limites de memoria e mantem interacao fluida em MSX2
  minimo.

---

# Fase 11 - Qualidade e acessibilidade infantil

## 11.1. Clareza visual

- [ ] Usar fonte grande e legivel.
- [ ] Limitar texto por tela.
- [ ] Destacar claramente o jogador atual.
- [ ] Usar cores consistentes para cada tipo de evento.
- [ ] Avisar antes de iniciar o cronometro.
- [ ] Nao depender somente de cor para transmitir informacao.

## 11.2. Dificuldade

- [ ] Configurar tempo por dificuldade.
- [ ] Configurar tabelas de multiplicacao por dificuldade.
- [ ] Configurar ajuda visual.
- [ ] Configurar velocidade das animacoes.
- [ ] Balancear atributos sem misturar regras de apresentacao.
- [ ] Avaliar grade de multiplicacao no nivel facil.

## 11.3. Feedback educativo

- [ ] Mostrar a operacao correta depois de erro.
- [ ] Mostrar o resultado correto depois de timeout.
- [ ] Explicar a penalidade sem linguagem excessivamente punitiva.
- [ ] Dar tempo para a crianca ler a resposta.
- [ ] Permitir confirmacao antes de continuar.

## Criterio de conclusao

- [ ] Criancas conseguem entender turno, pergunta, resultado e consequencia sem
  orientacao constante de um adulto.

---

# Fase 12 - Empacotamento e lancamento

## 12.1. Build reproduzivel

- [ ] Gerar executavel `.COM`.
- [ ] Gerar pacotes de dados.
- [ ] Gerar imagem de disco ou diretorio de distribuicao.
- [ ] Gerar simbolos de depuracao.
- [ ] Gerar mapa de memoria.
- [ ] Gerar relatorio de tamanho por segmento e arquivo.
- [ ] Identificar versao na tela de creditos.
- [ ] Documentar o comando de build.
- [ ] Garantir build limpo em outra maquina Windows.

## 12.2. Testes finais

- [ ] Testar todas as dificuldades.
- [ ] Testar todos os Herois.
- [ ] Testar todos os Chefes.
- [ ] Testar todos os modos.
- [ ] Testar acerto em todas as fases.
- [ ] Testar erro em todas as fases.
- [ ] Testar timeout em todas as fases.
- [ ] Testar vitoria por ataque.
- [ ] Testar vitoria causada por Ricochete.
- [ ] Testar derrota durante suporte.
- [ ] Testar derrota durante retaliacao.
- [ ] Testar derrota durante ataque em area.

## 12.3. Hardware real

- [ ] Testar em ao menos um MSX2 real.
- [ ] Testar em SD, flashcart ou dispositivo de armazenamento equivalente.
- [ ] Testar carregamento pelo MSX-DOS 2 ou Nextor.
- [ ] Conferir cores em uma saida real.
- [ ] Conferir audio.
- [ ] Conferir teclado.
- [ ] Conferir joystick.
- [ ] Comparar PAL e NTSC.

## Criterio de conclusao

- [ ] O pacote final pode ser instalado, executado e jogado integralmente em
  emuladores e hardware MSX2 real.

---

# Marcos do projeto

- [x] **M0 - Pesquisa:** GDD e MSXgl estudados.
- [ ] **M1 - Prova tecnica:** DOS2, SCREEN 5, entrada e animacao validados.
- [ ] **M2 - Core:** regras compilam e passam em testes nativos.
- [ ] **M3 - Duelo:** Modo A jogavel do menu ao resultado.
- [ ] **M4 - Cooperativo:** Modo B completo.
- [ ] **M5 - Mestre:** Modo C completo.
- [ ] **M6 - Conteudo:** personagens, efeitos e audio finais integrados.
- [ ] **M7 - Release candidate:** desempenho, compatibilidade e QA concluidos.
- [ ] **M8 - Lancamento:** pacote MSX-DOS 2 validado em hardware real.

# Procedimento de retomada

Ao voltar ao projeto depois de uma pausa:

1. Ler `GDD.md`.
2. Ler "Estado atual", "Questoes em aberto" e "Historico de decisoes" neste
   arquivo.
3. Localizar a primeira tarefa `[~]`; se nao houver, localizar a primeira `[ ]`
   da fase atual.
4. Consultar o ultimo commit e as alteracoes nao commitadas.
5. Executar o menor build ou teste que confirme o estado registrado.
6. Atualizar "Estado atual" antes de iniciar uma nova fase.
7. Ao terminar, marcar tarefas, registrar decisoes e indicar o proximo passo.

# Registro de validacoes

Adicionar uma linha a cada validacao relevante.

| Data | Fase | Ambiente | Comando ou teste | Resultado |
|---|---|---|---|---|
| 2026-10-03 | Pesquisa | Repositorio | Leitura do GDD e MSXgl | Concluido |

# Historico de decisoes

Adicionar decisoes que alterem arquitetura, regras ou plataforma. Nao registrar
detalhes temporarios de implementacao.

| Data | Decisao | Motivo |
|---|---|---|
| 2026-10-03 | Usar dados digitais | Integracao direta com regras e animacoes |
| 2026-10-03 | Usar multijogador hot-seat | Todos compartilham os controles |
| 2026-10-03 | Permitir cronometro desabilitado em niveis faceis | Acessibilidade |
| 2026-10-03 | Usar MSX2 como base e MSX2+ como melhoria opcional | Compatibilidade |
| 2026-10-03 | Iniciar com SCREEN 5 | Melhor equilibrio para arte bitmap e batalha |
| 2026-10-03 | Exigir Memory Mapper de 256 KB | Espaco para codigo, buffers e cache |
| 2026-10-03 | Usar MSX-DOS 2 `.COM` com target `DOS2` | O target gera `.COM` e permite usar `dos_mapper` em runtime |
