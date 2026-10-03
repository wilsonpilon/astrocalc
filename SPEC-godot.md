# SPEC Godot - Matematica nas Estrelas

Documento vivo de execucao para a versao Godot de **Matematica nas Estrelas**.

Este arquivo deve ser atualizado durante o desenvolvimento. Ao concluir uma
tarefa, marque sua caixa com `[x]`. Quando uma decisao mudar, atualize a secao
correspondente e registre a alteracao no Historico de decisoes.

## Estado atual

- **Fase atual:** Fase 0 - Consolidacao das regras e decisoes de tecnologia
- **Ultimo marco concluido:** GDD analisado e plano geral definido
- **Proximo passo recomendado:** Fechar as regras pendentes e escolher a
  estrategia do Core
- **Bloqueios conhecidos:** Regras pendentes e linguagem do Core
- **Ultima atualizacao:** 2026-10-03

### Legenda

- `[ ]` Nao iniciado
- `[~]` Em andamento
- `[x]` Concluido
- `[!]` Bloqueado ou aguardando decisao

> Markdown nao possui um estado intermediario padrao para checkboxes. Os
> marcadores `[~]` e `[!]` sao convencoes deste documento.

## Objetivo

Criar uma versao moderna do jogo educacional de combate por turnos
**Matematica nas Estrelas** usando Godot, preservando as mesmas regras da versao
MSX e uma separacao rigida entre:

1. **Core:** regras, turnos, dados, RNG, cronometros, validacao matematica,
   atributos e condicoes de vitoria.
2. **Aplicacao Godot:** cenas, entrada, audio, persistencia e integracao com a
   engine.
3. **Apresentacao:** UI, animacoes, efeitos, feedback e acessibilidade.

A camada visual nao pode alterar diretamente HP, dados, turnos ou regras. Toda
alteracao de batalha deve passar pelo Core.

## Relacao com a versao MSX

As duas versoes devem compartilhar:

- Terminologia.
- Tabelas de personagens e dificuldades.
- Ordem das fases de batalha.
- Resultados para a mesma semente e os mesmos comandos, quando viavel.
- Casos de teste das regras.
- Versao do formato de dados.

Os documentos possuem objetivos diferentes:

- `GDD.md`: define o jogo e suas regras.
- `SPEC-msx.md`: define a implementacao para MSX.
- `SPEC-godot.md`: define a implementacao para Godot.

Quando houver conflito, o GDD atualizado e a fonte principal das regras. As
duas SPECs devem ser atualizadas depois dele.

## Plataforma e tecnologia recomendadas

### Configuracao-base

- **Engine:** Godot 4.x estavel.
- **Renderer inicial:** Compatibility.
- **Projeto:** 2D.
- **Resolucao interna:** 1280x720.
- **Aspecto:** 16:9 com preservacao da proporcao.
- **UI:** nos `Control` e `Container`.
- **Apresentacao:** GDScript.
- **Dados:** Resources ou JSON validado, conforme a finalidade.
- **Versionamento:** arquivos de texto e assets-fonte no Git.

### Estrategia recomendada para o Core

Usar um **Core em C portatil**, sem dependencias de Godot ou MSXgl:

- No MSX, o Core e compilado pelo SDCC.
- No desktop, o mesmo Core e compilado e testado nativamente.
- Na Godot, uma extensao GDExtension fornece uma interface segura para o Core.
- Godot recebe eventos e envia comandos, sem acessar estruturas internas.

Essa estrategia reduz o risco de regras diferentes entre as versoes. Entretanto,
ela exige uma pequena camada C++ de GDExtension.

### Alternativa de prototipo

Se a integracao nativa impedir o progresso inicial, o Core pode ser prototipado
em GDScript, desde que:

- Tenha zero dependencia de cenas e nos.
- Use os mesmos comandos, eventos e casos de teste do Core C.
- Nao use `Node`, `Timer`, `SceneTree` ou sinais internamente.
- Seja substituivel posteriormente pelo adaptador GDExtension.

Essa alternativa deve ser uma decisao consciente e registrada, pois cria duas
implementacoes das regras.

## Decisoes confirmadas

- [x] O jogo usa dados digitais.
- [x] O combate e por turnos.
- [x] O multijogador local e hot-seat.
- [x] O cronometro varia por dificuldade.
- [x] Dificuldades faceis podem desabilitar o cronometro.
- [x] A logica deve ser separada da apresentacao.
- [x] A versao Godot deve seguir as mesmas regras da versao MSX.
- [x] O projeto sera 2D.

## Questoes em aberto

- [!] Escolher Godot 4.x exata para travar durante o desenvolvimento.
- [!] Escolher Core C compartilhado ou prototipo inicial em GDScript.
- [!] Definir plataformas de lancamento: Windows, Linux, macOS, Web ou mobile.
- [!] Definir a tabela final de dificuldades e tempos.
- [!] Definir explicitamente o erro do Mestre no Modo C.
- [!] Definir se cada etapa aceita somente uma submissao.
- [!] Definir o arredondamento do meio dano no Modo B.
- [!] Definir HP maximo e limite de cura.
- [!] Definir a ordem exata de eliminacao, retaliacao, cura e vitoria.
- [!] Decidir se a variante de Juiz permanece no torneio do Modo A.
- [!] Definir se havera progresso persistente, conquistas ou apenas partidas.

---

# Fase 0 - Regras e decisoes de tecnologia

## 0.1. Fechar as regras

- [ ] Definir dificuldades e duracao do cronometro.
- [ ] Definir comportamento quando o cronometro estiver desabilitado.
- [ ] Definir comportamento do Chefe humano ao errar no Modo C.
- [ ] Definir quantidade de respostas por tentativa.
- [ ] Definir arredondamento do Protocolo de Emergencia.
- [ ] Definir `HPAtual` e `HPMax`.
- [ ] Definir verificacoes de eliminacao.
- [ ] Definir ordem de retaliacao, cura e vitoria.
- [ ] Decidir a variante de Juiz.
- [ ] Atualizar o GDD com todas as decisoes.

## 0.2. Escolher tecnologia

- [ ] Escolher e registrar a versao da Godot.
- [ ] Escolher Core C compartilhado ou Core GDScript substituivel.
- [ ] Escolher plataformas de exportacao.
- [ ] Confirmar se Web e requisito.
- [ ] Confirmar se controles por toque sao requisito.
- [ ] Escolher renderer Compatibility ou Mobile com base nos alvos.

## 0.3. Definir criterios de paridade

- [ ] Criar identificadores estaveis para herois e chefes.
- [ ] Criar identificadores estaveis para modos e dificuldades.
- [ ] Definir formato dos comandos do Core.
- [ ] Definir formato dos eventos do Core.
- [ ] Definir casos de teste compartilhados.
- [ ] Definir politica de versao dos dados.

## Criterio de conclusao

- [ ] Regras e tecnologia estao decididas sem impedir uma segunda plataforma.

---

# Fase 1 - Fundacao do projeto Godot

## 1.1. Criar o projeto

- [ ] Criar o diretorio `godot`.
- [ ] Criar projeto Godot 4.x.
- [ ] Configurar renderer.
- [ ] Configurar resolucao 1280x720.
- [ ] Configurar stretch e preservacao de aspecto.
- [ ] Configurar modo de janela.
- [ ] Criar `.gitignore` apropriado.
- [ ] Registrar a versao da Godot em arquivo ou documentacao.
- [ ] Executar a primeira cena vazia.

## 1.2. Estrutura inicial

```text
godot/
  project.godot
  addons/
  assets/
    audio/
    fonts/
    images/
    music/
    source/
  data/
    characters/
    difficulties/
    localization/
  scenes/
    app/
    battle/
    components/
    menus/
  scripts/
    adapters/
    application/
    presentation/
    services/
  tests/
    core/
    integration/
    fixtures/
```

- [ ] Criar diretorios.
- [ ] Definir convencao de nomes.
- [ ] Definir onde ficam assets-fonte e assets importados.
- [ ] Impedir referencias circulares entre camadas.

## 1.3. Autoloads minimos

Autoloads previstos:

```text
SceneRouter
GameSession
SettingsService
AudioService
```

- [ ] Criar `SceneRouter`.
- [ ] Criar `GameSession`.
- [ ] Criar `SettingsService`.
- [ ] Criar `AudioService`.
- [ ] Evitar transformar todo sistema em singleton.
- [ ] Documentar responsabilidade de cada Autoload.

## 1.4. Entrada

Acoes previstas:

```text
ui_confirm
ui_cancel
ui_up
ui_down
ui_left
ui_right
answer_0 ... answer_9
answer_backspace
pause
skip_animation
```

- [ ] Configurar teclado.
- [ ] Configurar teclado numerico.
- [ ] Configurar gamepad.
- [ ] Definir navegacao de foco.
- [ ] Testar troca automatica entre teclado e controle.

## Criterio de conclusao

- [ ] O projeto abre sem erros, troca entre duas cenas e recebe teclado e
  gamepad.

---

# Fase 2 - Core e contrato de integracao

## 2.1. Estrutura do Core

Estrutura logica prevista:

```text
core/
  include/
    battle.h
    combatant.h
    rules.h
    dice.h
    timer.h
    answer.h
    events.h
  src/
    battle.c
    combatant.c
    rules.c
    dice.c
    timer.c
    answer.c
    events.c
  tests/
```

- [ ] Criar estruturas de dados sem ponteiros da Godot.
- [ ] Usar inteiros de largura conhecida.
- [ ] Evitar alocacao dinamica no Core.
- [ ] Evitar ponto flutuante nas regras.
- [ ] Evitar leitura direta de arquivos.
- [ ] Evitar chamadas de audio, video ou entrada.

## 2.2. Comandos enviados ao Core

```text
COMMAND_CONFIRM
COMMAND_CANCEL
COMMAND_DIGIT
COMMAND_BACKSPACE
COMMAND_PAUSE
COMMAND_TICK
```

- [ ] Definir estrutura de comando.
- [ ] Definir dados associados.
- [ ] Validar comandos por estado.
- [ ] Ignorar ou rejeitar comandos invalidos de forma explicita.

## 2.3. Eventos recebidos pela Godot

```text
EVENT_DICE_ROLLED
EVENT_TIMER_STARTED
EVENT_TIMER_UPDATED
EVENT_ANSWER_CORRECT
EVENT_ANSWER_WRONG
EVENT_TIMEOUT
EVENT_DAMAGE
EVENT_HEAL
EVENT_DODGE
EVENT_ENTITY_DEFEATED
EVENT_TURN_CHANGED
EVENT_BATTLE_FINISHED
```

- [ ] Definir estrutura de evento.
- [ ] Implementar fila com capacidade fixa.
- [ ] Definir comportamento de overflow.
- [ ] Garantir ordem deterministica.
- [ ] Documentar o significado de cada campo.

## 2.4. Integracao GDExtension

Se o Core compartilhado for escolhido:

- [ ] Criar extensao C++ minima.
- [ ] Expor uma classe `BattleCore`.
- [ ] Implementar criacao e destruicao seguras.
- [ ] Converter comandos Godot para comandos C.
- [ ] Converter eventos C para Dictionaries ou objetos tipados.
- [ ] Expor snapshot somente para leitura.
- [ ] Compilar em modo Debug.
- [ ] Compilar em modo Release.
- [ ] Impedir acesso direto da UI a ponteiros do Core.

## 2.5. Adaptador GDScript

Independentemente da implementacao:

- [ ] Criar uma interface unica usada pela aplicacao.
- [ ] Implementar `start_battle(config)`.
- [ ] Implementar `submit_command(command)`.
- [ ] Implementar `advance_time(delta_ms)`.
- [ ] Implementar `poll_events()`.
- [ ] Implementar `get_snapshot()`.
- [ ] Garantir que UI nao saiba se o Core e C ou GDScript.

## 2.6. RNG e tempo

- [ ] Receber semente explicitamente.
- [ ] Implementar dados uniformes.
- [ ] Separar resultado logico de animacao.
- [ ] Usar tempo inteiro no Core.
- [ ] Converter `_process(delta)` em ticks inteiros.
- [ ] Nao contar tempo durante pausa ou animacao bloqueante.
- [ ] Testar comportamento com quedas de frame.

## Criterio de conclusao

- [ ] Uma cena de teste inicia uma batalha, envia comandos e mostra eventos sem
  conter regras de combate.

---

# Fase 3 - Dados e testes das regras

## 3.1. Dados dos personagens

- [ ] Criar esquema de Heroi.
- [ ] Criar esquema de Chefe.
- [ ] Adicionar HP inicial e maximo.
- [ ] Adicionar Escudo.
- [ ] Adicionar Sorte.
- [ ] Adicionar Cura.
- [ ] Adicionar identificadores de assets.
- [ ] Validar identificadores duplicados.
- [ ] Validar valores fora dos limites.

## 3.2. Dificuldades

- [ ] Criar esquema de dificuldade.
- [ ] Configurar cronometro.
- [ ] Configurar cronometro desabilitado.
- [ ] Configurar ajuda visual.
- [ ] Configurar tabelas de multiplicacao, se aplicavel.
- [ ] Manter regras de dano fora dos dados de apresentacao.

## 3.3. Testes unitarios

- [ ] Testar d6.
- [ ] Testar d10.
- [ ] Testar d20.
- [ ] Testar semente deterministica.
- [ ] Testar resposta correta.
- [ ] Testar resposta errada.
- [ ] Testar timeout.
- [ ] Testar cronometro desabilitado.
- [ ] Testar cura.
- [ ] Testar HP maximo.
- [ ] Testar escudo.
- [ ] Testar dano direto.
- [ ] Testar esquiva.
- [ ] Testar eliminacao.
- [ ] Testar vitoria.
- [ ] Testar derrota.

## 3.4. Testes de paridade

Criar fixtures independentes da engine contendo:

- Semente.
- Configuracao da batalha.
- Sequencia de comandos.
- Tempos transcorridos.
- Eventos esperados.
- Snapshot final esperado.

Tarefas:

- [ ] Definir formato das fixtures.
- [ ] Executar fixtures no Core nativo.
- [ ] Executar fixtures pela integracao Godot.
- [ ] Reservar execucao futura das mesmas fixtures no MSX.

## Criterio de conclusao

- [ ] Regras basicas sao deterministicas e testadas sem cenas visuais.

---

# Fase 4 - Navegacao e fluxo da aplicacao

## 4.1. Cenas principais

```text
Boot
MainMenu
ModeSelect
DifficultySelect
CharacterSelect
Battle
Results
Settings
Credits
```

- [ ] Criar cenas vazias.
- [ ] Implementar troca de cenas.
- [ ] Preservar configuracao da partida em `GameSession`.
- [ ] Impedir batalha com configuracao incompleta.
- [ ] Implementar retorno seguro ao menu.

## 4.2. Maquina de estados da aplicacao

- [ ] Definir estados de navegacao.
- [ ] Definir entradas permitidas em cada estado.
- [ ] Definir transicoes.
- [ ] Evitar que telas alterem diretamente outras telas.
- [ ] Tratar falhas de carregamento explicitamente.

## 4.3. Transicoes

- [ ] Criar fade de entrada e saida.
- [ ] Bloquear entrada durante transicoes.
- [ ] Respeitar opcao de reduzir movimento.
- [ ] Evitar transicoes longas entre turnos.

## Criterio de conclusao

- [ ] E possivel navegar do menu ate uma batalha vazia e retornar sem erros.

---

# Fase 5 - Sistema visual de batalha

## 5.1. Hierarquia sugerida

```text
BattleScreen
  Background
  Arena
    BossView
    HeroViews
    EffectsLayer
  Hud
    TurnIndicator
    CombatantPanels
    TimerView
  InteractionLayer
    DiceView
    QuestionView
    AnswerInput
  OverlayLayer
    PauseMenu
    Tutorial
    Transition
```

- [ ] Criar hierarquia.
- [ ] Separar visual de dados.
- [ ] Usar Containers para HUD.
- [ ] Definir anchors e offsets responsivos.
- [ ] Definir ordem de desenho.

## 5.2. HUD

- [ ] Mostrar jogador atual.
- [ ] Mostrar HP atual e maximo.
- [ ] Mostrar Escudo.
- [ ] Mostrar Sorte.
- [ ] Mostrar Cura.
- [ ] Mostrar estado eliminado.
- [ ] Mostrar fase atual.
- [ ] Atualizar somente em resposta a eventos ou snapshots.

## 5.3. Cronometro

- [ ] Mostrar tempo numerico.
- [ ] Mostrar barra visual.
- [ ] Alterar cor perto do fim.
- [ ] Tocar alerta sem se tornar irritante.
- [ ] Ocultar ou indicar "sem limite" quando desabilitado.
- [ ] Parar visualmente durante pausa.

## 5.4. Campo de resposta

- [ ] Receber teclado.
- [ ] Receber teclado numerico.
- [ ] Receber gamepad por teclado virtual.
- [ ] Implementar apagar.
- [ ] Implementar confirmar.
- [ ] Limitar tamanho.
- [ ] Bloquear entrada fora da fase correta.
- [ ] Exibir foco com clareza.

## 5.5. Dados digitais

- [ ] Criar visual de d6.
- [ ] Criar visual de d10.
- [ ] Criar visual de d20.
- [ ] Animar sem gerar novos resultados logicos.
- [ ] Permitir pular ou acelerar.
- [ ] Garantir que o resultado final corresponda ao evento do Core.

## Criterio de conclusao

- [ ] Uma batalha simulada por eventos falsos pode ser apresentada por
  completo sem regras dentro da cena.

---

# Fase 6 - Vertical slice do Modo A

## 6.1. Configuracao

- [ ] Selecionar Modo A.
- [ ] Selecionar dificuldade.
- [ ] Selecionar dois Herois.
- [ ] Validar selecao.
- [ ] Criar configuracao do Core.

## 6.2. Turno completo

- [ ] Mostrar passagem hot-seat.
- [ ] Executar Suporte Vital.
- [ ] Animar d20.
- [ ] Resolver cura ou falha.
- [ ] Animar 2d10.
- [ ] Mostrar multiplicacao.
- [ ] Iniciar cronometro.
- [ ] Receber resposta.
- [ ] Resolver acerto.
- [ ] Resolver erro.
- [ ] Resolver timeout.
- [ ] Resolver Ricochete Laser.
- [ ] Executar Esquiva.
- [ ] Resolver dano.
- [ ] Trocar jogador.
- [ ] Resolver vitoria.

## 6.3. Resultado

- [ ] Mostrar vencedor.
- [ ] Mostrar resumo da partida.
- [ ] Mostrar acertos.
- [ ] Mostrar erros.
- [ ] Mostrar timeouts.
- [ ] Permitir revanche.
- [ ] Permitir voltar ao menu.

## 6.4. Primeira passagem audiovisual

- [ ] Uma nave aliada animada.
- [ ] Um oponente visual.
- [ ] Efeito de rolagem.
- [ ] Efeito de ataque.
- [ ] Efeito de impacto.
- [ ] Efeito de cura.
- [ ] Efeito de Ricochete.
- [ ] Musica provisoria.
- [ ] Efeitos sonoros provisorios.

## Criterio de conclusao

- [ ] Uma partida completa do Modo A pode ser jogada do menu ao resultado.

---

# Fase 7 - Modo B

## 7.1. Configuracao cooperativa

- [ ] Selecionar dois Herois.
- [ ] Selecionar um Chefe.
- [ ] Selecionar dificuldade.
- [ ] Identificar visualmente os dois jogadores.

## 7.2. Ataque sincronizado

- [ ] Rolar um d10 por Heroi.
- [ ] Receber resposta conjunta.
- [ ] Resolver primeira tentativa.
- [ ] Iniciar Protocolo de Emergencia.
- [ ] Exibir timer especial de cinco segundos.
- [ ] Resolver resposta de emergencia.
- [ ] Aplicar dano reduzido.
- [ ] Aplicar Ricochete aos dois em falha final.

## 7.3. Turno do Chefe

- [ ] Apresentar retaliacao.
- [ ] Rolar esquivas individualmente.
- [ ] Aplicar dano direto.
- [ ] Regenerar na fase correta.
- [ ] Encerrar imediatamente se o Chefe for eliminado.

## 7.4. Balanceamento

- [ ] Criar simulador sem UI.
- [ ] Medir duracao media.
- [ ] Medir taxa de vitoria por dupla.
- [ ] Avaliar regeneracao.
- [ ] Avaliar dano reduzido.
- [ ] Ajustar dados, nao codigo visual.

## Criterio de conclusao

- [ ] Partidas cooperativas completas funcionam contra todos os Chefes.

---

# Fase 8 - Modo C

## 8.1. Turnos dos Herois

- [ ] Configurar tres Herois.
- [ ] Mostrar passagem hot-seat.
- [ ] Executar Folego.
- [ ] Executar ataque matematico.
- [ ] Resolver dano.
- [ ] Verificar eliminacao.
- [ ] Passar ao proximo Heroi ativo.

## 8.2. Turno do Mestre

- [ ] Confirmar troca hot-seat.
- [ ] Regenerar o Chefe.
- [ ] Rolar 2d10.
- [ ] Apresentar pergunta.
- [ ] Executar cronometro.
- [ ] Resolver acerto, erro ou timeout.
- [ ] Executar Defesa Desesperada.
- [ ] Aplicar dano em area.

## 8.3. Eliminacao

- [ ] Pular Herois eliminados.
- [ ] Encerrar quando todos os Herois forem eliminados.
- [ ] Encerrar imediatamente quando o Chefe for eliminado.
- [ ] Mostrar eliminados claramente.

## Criterio de conclusao

- [ ] O Modo C funciona integralmente usando o mesmo Core dos demais modos.

---

# Fase 9 - Arte e animacao finais

## 9.1. Direcao de arte

- [ ] Criar guia de paleta.
- [ ] Criar guia de formas dos aliados.
- [ ] Criar guia de formas das ameacas.
- [ ] Definir estilo dos paineis.
- [ ] Definir estilo dos dados.
- [ ] Definir resolucao-fonte dos assets.
- [ ] Definir politica de importacao e compressao.

## 9.2. Personagens

- [ ] Capitao Estelar.
- [ ] Sombra Neon.
- [ ] Tecnomago.
- [ ] Saqueador Espacial.
- [ ] Ciborgue Titanio.
- [ ] Devorador de Planetas.
- [ ] Nebulosa Fantasma.
- [ ] Tita Cibernetico.
- [ ] Estados normal, dano, cura e derrota.
- [ ] Icones ou retratos.

## 9.3. Sistema de animacao

- [ ] Criar controlador de animacao por eventos.
- [ ] Criar fila de apresentacao.
- [ ] Aguardar animacoes bloqueantes sem parar a aplicacao.
- [ ] Permitir aceleracao.
- [ ] Permitir reducao de movimento.
- [ ] Garantir que animacao nao decida regras.

## 9.4. Efeitos

- [ ] Laser.
- [ ] Impacto no escudo.
- [ ] Esquiva.
- [ ] Ricochete.
- [ ] Sobrecarga.
- [ ] Cura.
- [ ] Regeneracao.
- [ ] Vitoria.
- [ ] Derrota.

## Criterio de conclusao

- [ ] Todos os eventos importantes possuem feedback visual claro e consistente.

---

# Fase 10 - Audio

## 10.1. Estrutura

- [ ] Criar buses Master, Music, SFX e UI.
- [ ] Criar controle de volume por bus.
- [ ] Persistir configuracoes.
- [ ] Impedir sobreposicao excessiva de sons.

## 10.2. Efeitos sonoros

- [ ] Navegacao.
- [ ] Confirmacao.
- [ ] Cancelamento.
- [ ] Rolagem de dado.
- [ ] Acerto matematico.
- [ ] Erro matematico.
- [ ] Alerta de tempo.
- [ ] Ataque.
- [ ] Impacto.
- [ ] Esquiva.
- [ ] Cura.
- [ ] Derrota.

## 10.3. Musica

- [ ] Menu.
- [ ] Batalha.
- [ ] Vitoria.
- [ ] Derrota.
- [ ] Transicoes suaves.
- [ ] Loop sem cortes perceptiveis.

## Criterio de conclusao

- [ ] Audio reforca os eventos sem encobrir instrucoes ou cansar o jogador.

---

# Fase 11 - Acessibilidade e experiencia infantil

## 11.1. Legibilidade

- [ ] Fonte grande.
- [ ] Contraste suficiente.
- [ ] Pouco texto por tela.
- [ ] Icones acompanhados por texto.
- [ ] Destaque claro do jogador atual.
- [ ] Suporte a diferentes proporcoes de tela.

## 11.2. Cronometro e pressao

- [ ] Avisar antes de iniciar.
- [ ] Permitir modo sem cronometro.
- [ ] Permitir reduzir sons de alerta.
- [ ] Nao usar flashes agressivos.
- [ ] Pausar quando a janela perde foco, se apropriado.

## 11.3. Feedback educativo

- [ ] Mostrar a operacao correta apos erro.
- [ ] Mostrar a resposta correta apos timeout.
- [ ] Dar tempo para leitura.
- [ ] Usar linguagem encorajadora.
- [ ] Explicar a consequencia mecanica.
- [ ] Permitir confirmacao antes de continuar.

## 11.4. Opcoes

- [ ] Volume geral.
- [ ] Volume de musica.
- [ ] Volume de efeitos.
- [ ] Tela cheia.
- [ ] Reduzir movimento.
- [ ] Velocidade das animacoes.
- [ ] Cronometro conforme dificuldade.
- [ ] Remapeamento ou alternativas de entrada, quando viavel.

## Criterio de conclusao

- [ ] Criancas entendem pergunta, tempo, resposta e consequencia sem orientacao
  constante.

---

# Fase 12 - Persistencia e localizacao

## 12.1. Configuracoes

- [ ] Definir formato versionado.
- [ ] Salvar volumes.
- [ ] Salvar modo de janela.
- [ ] Salvar opcoes de acessibilidade.
- [ ] Tratar arquivo ausente.
- [ ] Tratar arquivo corrompido explicitamente.
- [ ] Implementar migracao entre versoes quando necessario.

## 12.2. Progresso opcional

Somente implementar depois de decisao no GDD:

- [ ] Definir estatisticas permitidas.
- [ ] Definir progresso ou desbloqueios.
- [ ] Evitar armazenar dados pessoais de criancas.
- [ ] Permitir apagar o progresso.
- [ ] Nao tornar progresso requisito para jogar os modos principais.

## 12.3. Localizacao

- [ ] Extrair todos os textos de UI.
- [ ] Definir chaves estaveis.
- [ ] Implementar portugues.
- [ ] Preparar pluralizacao.
- [ ] Testar textos longos.
- [ ] Evitar texto embutido em imagens.

## Criterio de conclusao

- [ ] Configuracoes sobrevivem ao reinicio e os textos podem ser traduzidos sem
  alterar cenas.

---

# Fase 13 - Qualidade, desempenho e exportacao

## 13.1. Testes de integracao

- [ ] Menu ate batalha.
- [ ] Batalha ate resultado.
- [ ] Revanche.
- [ ] Retorno ao menu.
- [ ] Pausa.
- [ ] Troca de dispositivo de entrada.
- [ ] Todas as dificuldades.
- [ ] Todos os Herois.
- [ ] Todos os Chefes.
- [ ] Todos os modos.

## 13.2. Casos extremos

- [ ] Acerto no ultimo instante.
- [ ] Timeout sem entrada.
- [ ] Entrada no mesmo frame do timeout.
- [ ] Ricochete eliminando o atacante.
- [ ] Chefe eliminado antes de retaliar.
- [ ] Cura proxima do HP maximo.
- [ ] Todos os Herois eliminados no mesmo ataque.
- [ ] Pausa durante pergunta.
- [ ] Queda brusca de frame.
- [ ] Gamepad desconectado.

## 13.3. Desempenho

- [ ] Usar Profiler da Godot.
- [ ] Eliminar alocacoes repetidas em loops importantes.
- [ ] Reduzir overdraw.
- [ ] Revisar tamanhos de textura.
- [ ] Revisar importacao de audio.
- [ ] Testar hardware de baixo desempenho.
- [ ] Definir alvo de FPS.
- [ ] Confirmar que o Core nao depende do FPS.

## 13.4. Exportacao

Para cada plataforma escolhida:

- [ ] Instalar export template.
- [ ] Configurar preset.
- [ ] Configurar icone e metadados.
- [ ] Exportar build Debug.
- [ ] Exportar build Release.
- [ ] Testar em instalacao limpa.
- [ ] Verificar suporte da GDExtension.
- [ ] Gerar checksums ou artefatos versionados.

## 13.5. Release candidate

- [ ] Congelar regras.
- [ ] Congelar formato de dados.
- [ ] Executar todos os testes.
- [ ] Revisar erros do console.
- [ ] Revisar licencas de assets.
- [ ] Atualizar creditos.
- [ ] Atualizar versao.
- [ ] Criar notas da versao.

## Criterio de conclusao

- [ ] O jogo pode ser instalado e jogado integralmente nas plataformas-alvo sem
  erros conhecidos de alta severidade.

---

# Marcos do projeto

- [x] **G0 - Pesquisa:** GDD analisado e plano criado.
- [ ] **G1 - Fundacao:** projeto, entrada e navegacao basica funcionando.
- [ ] **G2 - Core:** regras testadas e integradas por adaptador.
- [ ] **G3 - Apresentacao:** HUD, dados, resposta e cronometro funcionais.
- [ ] **G4 - Duelo:** Modo A jogavel do menu ao resultado.
- [ ] **G5 - Cooperativo:** Modo B completo.
- [ ] **G6 - Mestre:** Modo C completo.
- [ ] **G7 - Conteudo:** arte, animacoes e audio finais integrados.
- [ ] **G8 - Acessibilidade:** opcoes e feedback infantil validados.
- [ ] **G9 - Release candidate:** QA, desempenho e exportacoes concluidos.
- [ ] **G10 - Lancamento:** builds finais publicados.

# Procedimento de retomada

Ao voltar ao projeto depois de uma pausa:

1. Ler `GDD.md`.
2. Ler "Estado atual", "Questoes em aberto" e "Historico de decisoes" neste
   arquivo.
3. Verificar se `SPEC-msx.md` possui alguma decisao de regras mais recente.
4. Localizar a primeira tarefa `[~]`; se nao houver, localizar a primeira `[ ]`
   da fase atual.
5. Consultar o ultimo commit e as alteracoes nao commitadas.
6. Abrir o projeto na versao registrada da Godot.
7. Executar os testes do Core e abrir a cena principal.
8. Atualizar "Estado atual" antes de iniciar uma nova fase.
9. Ao terminar, marcar tarefas, registrar decisoes e indicar o proximo passo.

# Registro de validacoes

Adicionar uma linha a cada validacao relevante.

| Data | Fase | Ambiente | Comando ou teste | Resultado |
|---|---|---|---|---|
| 2026-10-03 | Pesquisa | Repositorio | Analise do GDD e criacao da SPEC | Concluido |

# Historico de decisoes

Adicionar decisoes que alterem arquitetura, regras ou plataforma. Nao registrar
detalhes temporarios de implementacao.

| Data | Decisao | Motivo |
|---|---|---|
| 2026-10-03 | Criar versao Godot em 2D | O jogo usa paineis, dados e combate por turnos |
| 2026-10-03 | Separar Core, aplicacao e apresentacao | Portabilidade e testes |
| 2026-10-03 | Usar GDScript na apresentacao | Integracao direta e produtiva com Godot |
| 2026-10-03 | Recomendar Core C compartilhado | Evitar divergencia entre Godot e MSX |
| 2026-10-03 | Usar renderer Compatibility inicialmente | Maior alcance de hardware |
| 2026-10-03 | Usar resolucao interna 1280x720 inicialmente | Base 16:9 simples para UI responsiva |
