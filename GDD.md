# Game Design Document (GDD): Operação Sideral — RPG Matemático (v3.0)

> **Fonte única das regras:** "Operação Sideral — Manual v2.1, Edição Definitiva
> (D12)" (`manual_2-1.html` / `manual_opera_o_sideral-2-1.md`).
> Todos os manuais e GDDs anteriores (incluindo "Matemática nas Estrelas" v1.3a,
> o Manual Consolidado em PDF e o GDD v2.0/v2.1) estão **substituídos**.
>
> Onde o manual é omisso, este GDD lista a lacuna na seção 9 com uma proposta
> marcada como **[PROPOSTA]**. Propostas só viram regra depois de confirmadas.

## 1. Visão geral

RPG matemático de combate por turnos em uma temática espacial. Os jogadores
pilotam naves, rolam dados e multiplicam o resultado de **2d12** para disparar o
canhão. A precisão e a velocidade na tabuada (até 12×12) decidem a batalha.

- **Público:** crianças a partir de 7 anos. A criança-alvo tem Altas
  Habilidades e domina tabuadas avançadas.
- **Plataforma atual:** Godot 4.7, Windows (principal) e Linux.

## 2. Arquitetura

O sistema separa rigidamente o **Core** (máquina de estados, turnos, regras,
RNG, cronômetro e atributos) da **Apresentação** (UI, gráficos, áudio).

- Core em **GDScript puro** (classes `RefCounted`, sem `Node`, `Timer`,
  `SceneTree` ou sinais internos), só com inteiros e RNG próprio com semente.
- O Core deve continuar portável para uma eventual versão MSX (C/SDCC).

## 3. Atributos

| Atributo | Uso |
|---|---|
| `HP` | Pontos de vida. Com `HP <= 0` a entidade é eliminada. |
| `Escudo` | Subtraído do dano bruto recebido (o dano nunca fica negativo). |
| `Sorte` | Somada ao d6 da esquiva. Esquiva com `d6 + Sorte >= 8`. |
| `Cura` | Heróis: somada ao d20 no Suporte Vital. Chefes: cura automática. |

Chance de esquiva por Sorte:

| Sorte | d6 necessário | Chance |
|---|---|---|
| 1 | — | 0% |
| 2 | 6 | 17% |
| 3 | 5 ou 6 | 33% |
| 4 | 4, 5 ou 6 | 50% |

### 3.1. Limites de HP

- **Heróis:** máximo de **200 HP** (começam com 200).
- **Chefes:** o máximo é o HP inicial.
- Toda cura acima do limite é desperdiçada.

## 4. Personagens

### 4.1. Heróis da Frota

| ID | Herói | Papel | HP | Escudo | Sorte | Cura |
|---|---|---|---|---|---|---|
| `astro` | Astro-Enlatado | Tanque: nunca esquiva, escudo alto | 200 | 15 | 1 | 2 |
| `ninja` | Ninja Sideral | Esquiva: desvia com 5 ou 6 | 200 | 2 | 3 | 2 |
| `mago` | Mago Quântico | Recarga: melhor cura do jogo | 200 | 5 | 2 | 8 |
| `barbaro` | Bárbaro de Marte | Equilíbrio | 200 | 8 | 2 | 4 |
| `capitao` | Capitão Estelar | Paladino: absorção fixa, ignora esquiva | 200 | 10 | 1 | 6 |
| `rastreador` | Rastreador Cometa | Patrulheiro: 50% de esquiva | 200 | 4 | 4 | 5 |

### 4.2. Ameaças Colossais (Chefes)

| ID | Chefe | Descrição | HP | Escudo | Sorte | Cura |
|---|---|---|---|---|---|---|
| `nebulosa` | Nebulosa Fantasma | Esquiva com frequência e regenera bem | 300 | 10 | 3 | 15 |
| `tita` | Titã Cibernético | Fortaleza de aço | 400 | 15 | 2 | 15 |
| `devorador` | O Devorador | Nunca esquiva; carapaça corta 18 | 450 | 18 | 1 | 10 |
| `singularidade` | Singularidade Sombria | Regeneração absurda | 600 | 5 | 1 | 20 |

## 5. Regras gerais de controle

- **Cronômetro:** toda conta é cronometrada.
- **Tempo Esgotado (Falha de Mira):** o ataque é cancelado e o atacante perde
  **5 HP**.
- **Erro de Conta (Sobrecarga):** respondeu no tempo, mas errou → o ataque falha
  e o atacante perde **10 HP** direto (ignora Escudo).
- **Árbitro:** na versão digital, o próprio sistema valida a conta e o tempo.
- **Feedback educativo:** após erro ou tempo esgotado, a interface mostra a conta
  correta antes de seguir.

## 6. O Turno Básico (heróis)

### Fase 1 — Suporte Vital (1d20)

| d20 | Resultado |
|---|---|
| 11–20 | Sucesso: `HP += d20 + Cura` (limitado a 200) |
| 6–10 | Estabilidade: nada acontece |
| 1–5 | Curto-circuito: `HP -= d20` |

### Fase 2 — Canhão Principal (2d12)

Rolam-se dois d12 (faces 1 a 12). O jogador responde `D1 × D2` dentro do tempo.

- Acerto no tempo: `DanoBruto = D1 × D2`.
- Erro: Sobrecarga (−10 HP), sem ataque.
- Tempo esgotado: Falha de Mira (−5 HP), sem ataque.

### Fase 3 — Defesa / Esquiva (1d6)

O alvo rola `d6 + Sorte`.

- `>= 8`: esquiva total, nenhum dano.
- `<= 7`: `DanoReal = max(0, DanoBruto - Escudo_do_alvo)`.

## 7. Mecânica dos Chefes (PvE / Co-op)

- **Cura Automática:** no início do seu turno, o chefe não rola d20; soma a sua
  Cura diretamente ao HP (limitado ao HP inicial).
- **Sorte Ativada:** para cada ataque dos heróis, o chefe rola `d6 + Sorte`. Com
  8 ou mais, desvia do ataque inteiro. Se não desviar, aplica-se o Escudo do
  chefe normalmente.

## 8. Modos de jogo

### 8.1. Duelo (PvP, 2 pilotos)

Os pilotos alternam o Turno Básico completo (Fases 1, 2 e 3), sendo o defensor
quem faz a Fase 3. Quem começa é sorteado. Vence quem reduzir o HP do oponente
a zero.

### 8.2. Co-op contra Chefe (PvE)

Uma dupla de heróis enfrenta um chefe. Cada herói faz o seu Turno Básico (Fases
1 e 2); o chefe faz a esquiva (Sorte Ativada) e aplica o seu Escudo. No turno do
chefe ocorre a Cura Automática. As lacunas deste modo estão na seção 9.

## 9. Lacunas do manual (a decidir)

| # | Lacuna | [PROPOSTA] |
|---|---|---|
| L1 | **Como o chefe ataca** (dano, alvo, quem resolve a conta) | Chefe rola 2d12; o sistema calcula; ataca **cada** herói vivo, que faz a sua Fase 3 |
| L2 | Ordem da rodada no Co-op | Herói 1 → Herói 2 → turno do chefe (Cura Automática, depois ataque) |
| L3 | Quem controla o chefe | O sistema (IA). Um "controlador humano" fica para depois |
| L4 | Condição de derrota no Co-op | Derrota quando os dois heróis forem eliminados; o sobrevivente continua |
| L5 | Número de heróis no Co-op | Somente 2 (o manual fala em "a dupla") |
| L6 | Duração do cronômetro | Por dificuldade: sem limite / 60 s / 30 s / 15 s |
| L7 | Equilíbrio do Rastreador Cometa (ver 10.2) | Avaliar após testes com a criança |
| L8 | Modos extras dos manuais antigos (torneio, Mestre humano, Protocolo de Emergência) | Fora da v3.0; reavaliar depois |

## 10. Verificação estatística (simulação, 2026-10-03)

Monte Carlo com todas as combinações de heróis, considerando 8% de erros e 4%
de tempo esgotado.

### 10.1. Confirmações do manual

- A média de 2d12 multiplicados é **42,25** (máximo 144), como diz o manual.
- **Duelo:** mediana de 16 turnos (**~8 rodadas**, p90 de 14 rodadas). Isso
  confirma o "ritmo ideal" de 8 a 12 rodadas.
- **Co-op (estimativa de dano):** com dois heróis acertando, os chefes caem em
  ~10 (Nebulosa e Devorador), ~11 (Singularidade) e ~12 rodadas (Titã), antes de
  contar o ataque do chefe (L1).

### 10.2. Ponto de atenção — equilíbrio dos heróis

Vitórias médias no Duelo:

| Herói | Vitórias |
|---|---|
| Rastreador Cometa | **75%** |
| Ninja Sideral | 50% |
| Bárbaro de Marte | 47% |
| Mago Quântico | 45% |
| Astro-Enlatado | 44% |
| Capitão Estelar | **39%** |

A Sorte 4 (50% de esquiva) é o que domina. Reduzir Escudo e Cura do Rastreador
para valores mínimos ainda deixa a vitória em ~70%. O equilíbrio exige mexer na
Sorte ou na regra de esquiva (L7).
