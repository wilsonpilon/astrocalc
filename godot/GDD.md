# Game Design Document (GDD): Matemática nas Estrelas (v2.1)

> **v2.1 (2026-10-03):** consolida o PDF "Manual Consolidado Definitivo" (nomes e
> personagens) com o GDD v2.0 (Ricochete Laser e Protocolo de Emergência) e aplica
> o rebalanceamento validado por simulação (seção 7).

## 1. Diretriz de arquitetura

O sistema separa rigidamente o **Core** (máquina de estados, turnos, regras,
RNG, cronômetros e atributos) da **Apresentação** (UI, gráficos, áudio).

- Implementação atual: **Godot 4.7**, Core em **GDScript puro** (classes
  `RefCounted`, sem `Node`, `Timer`, `SceneTree` ou sinais internos).
- O Core deve continuar portável para uma futura versão MSX (C/SDCC).
- Público: crianças a partir de 7 anos. A criança-alvo tem Altas Habilidades e
  domina a tabuada completa, então os dados vão de 1×1 a 10×10 em todas as
  dificuldades.

## 2. Mecânicas globais de matemática

- **Mira Fixada (cronômetro):** durante a resolução da conta corre um
  temporizador cuja duração depende da dificuldade (seção 6). Na dificuldade
  mais fácil ele pode ser desligado.
- **Uma resposta por tentativa:** o jogador digita e confirma uma vez. A única
  segunda chance é o Protocolo de Emergência (Modo B).
- **Ricochete Laser (todos os modos):** resposta errada OU tempo esgotado →
  o ataque falha (`DanoBruto = 0`) e quem atacou perde **10 HP** direto,
  ignorando o Escudo. Vale também para o Mestre no Modo C.
- **Feedback educativo:** após erro ou timeout, a interface mostra a conta
  correta antes de seguir.

## 3. Direção de arte

Estética de painel de nave espacial (Dark Mode, fundo `#161b22`).

- Aliados: 5 heróis com ilustrações já existentes.
- Ameaças: 3 chefes com ilustrações já existentes.
- Dados: representações 2D de d20, d10 e d6 (amarelo néon).

## 4. Atributos

| Atributo | Uso |
|---|---|
| `HP` | Pontos de vida. Com `HP <= 0` a entidade é eliminada. |
| `Escudo` | Subtraído do dano bruto recebido (nunca deixa o dano negativo). |
| `Sorte` | Somada ao d6 da esquiva. Esquiva com `d6 + Sorte >= 8`. |
| `Cura` | Somada ao d20 no Fôlego (heróis) ou regeneração passiva (chefes). |

Chance de esquiva por Sorte: 1 → 0% · 2 → 17% · 3 → 33% · 4 → 50%.

### 4.1. Heróis

Todos começam com **200 HP**. A cura pode levar o HP até o **máximo de 250**.

| ID | Herói | Papel | Escudo | Sorte | Cura |
|---|---|---|---|---|---|
| `astro` | Astro-Enlatado | O Ciborgue Enferrujado (tanque) | 15 | 2 | 6 |
| `capitao` | Capitão Estelar | O Paladino da Guarda | 10 | 2 | 14 |
| `barbaro` | Bárbaro de Marte | O Alien Furioso (equilíbrio) | 6 | 3 | 10 |
| `mago` | Mago Quântico | O Cientista Maluco (recarga) | 2 | 3 | 18 |
| `ninja` | Ninja Sideral | O Alienígena Veloz (esquiva) | 2 | 4 | 4 |

### 4.2. Chefes

Os valores de **HP** e **Regeneração** da carta valem para **3 atacantes por
rodada**. Em jogo, ambos escalam pelo número de ataques por rodada `k`:

```
HP(k)    = round(HP_carta    * k / 3)
Regen(k) = round(Regen_carta * k / 3)
```

`k = 1` no Modo B (ataque conjunto único) e `k = nº de heróis` no Modo C.
O HP inicial é o máximo, e a regeneração nunca o ultrapassa.

| ID | Chefe | Papel | HP carta | Escudo | Sorte | Regen carta | Modo B (HP/Regen) | 4 heróis (HP/Regen) |
|---|---|---|---|---|---|---|---|---|
| `nebulosa` | Nebulosa Fantasma | A Intangível (esquiva 50%) | 360 | 5 | 4 | 9 | 120 / 3 | 480 / 12 |
| `tita` | Titã Cibernético | O Colosso (regeneração) | 420 | 12 | 2 | 18 | 140 / 6 | 560 / 24 |
| `devorador` | O Devorador | O Tanque Absurdo (nunca esquiva) | 500 | 20 | 1 | 9 | 167 / 3 | 667 / 12 |

## 5. Regras compartilhadas

### 5.1. Fôlego Heroico (d20) — igual em todos os modos

| d20 | Resultado |
|---|---|
| 15–20 | Cura: `HP += d20 + Cura` (limitado a 250) |
| 6–14 | Estável: nada acontece |
| 1–5 | Sobrecarga: `HP -= 10` |

### 5.2. Ataque (2d10)

Rolam-se dois d10 (faces 1 a 10) e pede-se a multiplicação.

- Acerto no tempo: `DanoBruto = D1 × D2`.
- Erro ou timeout: Ricochete Laser.

### 5.3. Esquiva e dano

O alvo rola `d6 + Sorte`.

- `>= 8`: esquiva, nenhum dano.
- `<= 7`: `DanoReal = max(0, DanoBruto - Escudo_do_alvo)`.

Isso vale para heróis e para chefes.

### 5.4. Ataque do Chefe (Modos B e C)

Rolam-se 2d10 e multiplica-se (no Modo B o sistema calcula; no Modo C o Mestre
responde a conta). O mesmo `DanoBruto` atinge **todos os heróis vivos**, e cada
um faz sua própria esquiva (5.3).

### 5.5. Eliminação

Uma entidade com `HP <= 0` é eliminada imediatamente, inclusive por Sobrecarga
ou Ricochete. Heróis eliminados são pulados nas rodadas seguintes. A vitória é
verificada logo após cada alteração de HP.

## 6. Dificuldades (proposta — a confirmar nos testes)

| ID | Nome | Cronômetro | Protocolo de Emergência |
|---|---|---|---|
| `cadete` | Cadete | desligado | 5 s |
| `piloto` | Piloto | 60 s | 5 s |
| `capitao` | Capitão | 30 s | 5 s |
| `almirante` | Almirante | 15 s | 3 s |

## 7. Modos de jogo

### MODO A — Duelo Estelar (1v1 ou Torneio)

Os jogadores alternam turnos (quem começa é sorteado). Turno do atacante A
contra o defensor B:

1. **Fôlego** de A (5.1).
2. **Ataque** de A (5.2). Se houver Ricochete, o turno acaba.
3. **Esquiva** de B (5.3) e aplicação do dano.
4. Verificação de vitória e troca de jogador.

**Torneio:** chaves de 1v1, vencedores avançam. Na versão digital, o próprio
sistema faz o papel do Árbitro Galáctico, validando todas as contas.

### MODO B — Ameaça Autônoma (2 heróis vs chefe IA)

Cada rodada:

1. **Fôlego** de cada piloto vivo.
2. **Canhão Duplo:** cada piloto rola 1d10; a dupla responde `D1 × D2` com
   cronômetro.
   - Acerto: `DanoBruto = D1 × D2`.
   - Erro ou timeout → **Protocolo de Emergência:** abre-se um cronômetro curto
     (seção 6). Se a resposta correta vier nele, `DanoBruto = (D1 × D2) / 2`
     (divisão inteira, arredonda para baixo). Se falhar de novo, Ricochete
     Laser: **cada piloto vivo perde 10 HP** e não há ataque.
   - O chefe esquiva e desconta o Escudo (5.3). Chefe com `HP <= 0` →
     vitória imediata.
3. **Regeneração** do chefe (`Regen(1)`).
4. **Ataque do Chefe** (5.4) contra os pilotos vivos.
5. Se os dois pilotos estiverem eliminados → derrota. Se só um cair, o
   sobrevivente continua e rola os dois d10 sozinho.

### MODO C — Mestre da Galáxia (3 ou 4 heróis vs chefe humano)

1. **Turno dos heróis** (sequencial, cada herói vivo):
   - Fôlego (5.1).
   - Ataque individual (5.2), com Ricochete por erro.
   - O chefe esquiva e desconta o Escudo (5.3). Chefe eliminado → vitória
     imediata.
2. **Turno do Mestre:**
   - Regeneração passiva (`Regen(n)`), sem rolar dados.
   - Ataque do Chefe (5.4): o Mestre responde a conta com cronômetro.
     Errou ou estourou o tempo → Ricochete: **o chefe perde 10 HP** e não ataca.
   - Todos os heróis eliminados → derrota.

## 8. Balanceamento (simulação, 2026-10-03)

Premissas: crianças erram 10% das contas, Mestre erra 5%, Protocolo salva 60%
dos erros no Modo B. Monte Carlo com todas as combinações de heróis.

| Modo | Vitória | Duração mediana |
|---|---|---|
| A – Duelo | cada herói vence 47–53% dos duelos | 28 turnos (p90: 48) |
| B – Coop vs IA | heróis vencem 76–81% | 12–14 rodadas |
| C – 3 heróis vs Mestre | Nebulosa 68%, Devorador 60%, Titã 57% | 14–17 rodadas |
| C – 4 heróis vs Mestre | 55–67% | 15–18 rodadas |

Com 20% de erros todos os modos ainda terminam; no Modo C os heróis passam a
vencer 37–51%. O Modo B é propositalmente o mais fácil (porta de entrada).
