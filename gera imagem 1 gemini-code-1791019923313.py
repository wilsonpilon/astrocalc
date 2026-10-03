import os
import zipfile
from PIL import Image, ImageDraw, ImageFont

os.makedirs('rpg_export', exist_ok=True)

spec_content = """# SPEC.md - RPG Espacial: Matemática nas Estrelas

## 1. Instrução de Inicialização (System Prompt)
Você é um Arquiteto de Software, Engenheiro Sênior e Game Designer. Utilize este Game Design Document (GDD) como contexto para me auxiliar na arquitetura e programação do jogo "Matemática nas Estrelas". O desenvolvimento pode ser feito escolhendo uma das seguintes tecnologias, e você deve adaptar a estrutura de acordo com o pedido:
- **Godot Engine (GDScript)**
- **GameMaker (GML)**
- **Golang (Go)** (Backend/CLI ou TUI usando tview)
- **C/C++ ou Z80 Assembly / SDCC** (Para hardwares retro como MSX)

**Diretriz Arquitetural:** Separe estritamente a "Máquina de Estados" (Turnos, Fases) e o motor de RNG/Matemática da camada de Interface Gráfica ou Textual, para facilitar portas entre MSX e Windows.

## 2. Visão Geral
RPG educativo focado em operações matemáticas (adição, subtração, multiplicação).
**Direção de Arte:** Painéis de nave espacial, interface "Dark Mode" (Fundo `#161b22`) com linhas geométricas neon (Azul `#58a6ff` para aliados, Vermelho `#ff7b72` para inimigos, Amarelo `#f9a826` para itens/regras).

## 3. Personagens e Status (Data Structures)
Atributos Base: `HP` (Vida Máxima), `Escudo` (Redutor de Dano), `Sorte` (Bônus de Esquiva), `Cura` (Regeneração Passiva/Ativa).

**Heróis (Player Characters):**
1. Capitão Estelar: HP 200 | Escudo 15 | Sorte 2 | Cura 6
2. Sombra Neon: HP 200 | Escudo 3 | Sorte 5 | Cura 8
3. Tecnomago: HP 200 | Escudo 5 | Sorte 3 | Cura 18
4. Saqueador Espacial: HP 200 | Escudo 8 | Sorte 4 | Cura 10
5. Ciborgue Titânio: HP 200 | Escudo 12 | Sorte 2 | Cura 14

**Chefes (Bosses / IA):**
1. Devorador de Planetas: HP 600 | Escudo 25 | Sorte 2 | Cura 10
2. Nebulosa Fantasma: HP 400 | Escudo 12 | Sorte 5 | Cura 15
3. Titã Cibernético: HP 500 | Escudo 18 | Sorte 4 | Cura 20

## 4. Lógica de Jogo (Game Modes & Turn Flow)

### 4.1. Modos Competitivos (1v1 e Torneio de Chaves)
*Estrutura do Turno (Player A):*
- **Fase 1 (Suporte Vital):** Rola `1d20`. 
  - `>= 6`: `HP = HP + Dado + Cura`
  - `<= 5`: `HP = HP - Dado` (Falha)
- **Fase 2 (Ataque Bruto):** Rola `2d10`. `DanoBruto = Dado1 * Dado2`
- **Fase 3 (Esquiva/Defesa do Player B):** Rola `1d6 + Sorte`.
  - `>= 8`: `DanoReal = 0` (Esquivou)
  - `<= 7`: `DanoReal = DanoBruto - Escudo do Player B` (Min 0). `Player B HP -= DanoReal`.

### 4.2. Ameaça Autônoma (Coop: 2 Heróis vs 1 Chefe IA)
- **Ataque Sincronizado:** Herói 1 e Herói 2 rolam `1d10` simultaneamente. `DanoConjunto = D1 * D2`. `DanoReal = DanoConjunto - Escudo do Chefe`.
- **Retaliação (Auto-Trigger):** Após o ataque, o Chefe revida. Heróis rolam `1d6 + Sorte`. Se `<= 7`, sofrem 15 de dano perfurante direto.
- **Cura Passiva:** Fim da rodada, `Chefe HP += Chefe.Cura`.

### 4.3. Mestre da Galáxia (PvE: N Heróis vs 1 Chefe Controlado por Humano)
- **Fôlego Heroico (Heróis):** `1d20`. `15 a 20`: Cura normal. `6 a 14`: `HP` não altera. `1 a 5`: `HP -= 10`.
- **Turno do Chefe:**
  - Regeneração Passiva Automática (`HP += Cura`).
  - Raio em Área: Chefe rola `2d10` -> `DanoBruto = D1 * D2`.
  - Cada herói rola individualmente a Esquiva (`1d6 + Sorte`). Se falhar, sofre `DanoBruto - Escudo`.
"""

with open('rpg_export/SPEC.md', 'w', encoding='utf-8') as f:
    f.write(spec_content)

def draw_neon_asset(filename, name, asset_type):
    img = Image.new('RGB', (400, 600), color='#161b22')
    draw = ImageDraw.Draw(img)
    
    if asset_type == 'hero':
        color = '#58a6ff'
        # Draw a stylized space fighter
        draw.polygon([(200, 150), (320, 380), (200, 320), (80, 380)], outline=color, width=6)
        draw.line([(200, 150), (200, 320)], fill=color, width=3)
    elif asset_type == 'boss':
        color = '#ff7b72'
        # Draw an alien menace / mechanical core
        draw.ellipse([(120, 200), (280, 360)], outline=color, width=6)
        draw.polygon([(100, 420), (200, 280), (300, 420)], outline=color, width=6)
        draw.ellipse([(180, 260), (220, 300)], fill=color)
    elif asset_type == 'dice':
        color = '#f9a826'
        if 'd20' in filename: # Hexagon for d20
            draw.polygon([(200, 120), (300, 180), (300, 300), (200, 360), (100, 300), (100, 180)], outline=color, width=6)
            draw.line([(200, 120), (200, 240)], fill=color, width=3)
            draw.line([(100, 180), (200, 240)], fill=color, width=3)
            draw.line([(300, 180), (200, 240)], fill=color, width=3)
        elif 'd10' in filename: # Diamond/Kite for d10
            draw.polygon([(200, 120), (320, 240), (200, 380), (80, 240)], outline=color, width=6)
            draw.line([(200, 120), (200, 380)], fill=color, width=3)
        else: # Square/Cube for d6
            draw.rectangle([(120, 180), (280, 340)], outline=color, width=6)
            draw.ellipse([(185, 245), (215, 275)], fill=color)
    else: # Cover
        color = '#c9d1d9'
        draw.rectangle([(60, 60), (340, 540)], outline=color, width=4)
        draw.ellipse([(150, 150), (250, 250)], outline='#58a6ff', width=4)
        draw.ellipse([(160, 350), (240, 430)], outline='#ff7b72', width=4)

    # Outer Neon Border
    draw.rounded_rectangle([(15, 15), (385, 585)], radius=20, outline=color, width=8)
    
    # Try loading a readable font for Linux
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
    except:
        font = ImageFont.load_default()
    
    # Fake multiline text for cover
    if "\n" in name:
        lines = name.split("\n")
        draw.text((200, 480), lines[0].upper(), fill=color, font=font, anchor="ms")
        draw.text((200, 520), lines[1].upper(), fill=color, font=font, anchor="ms")
    else:
        draw.text((200, 500), name.upper(), fill=color, font=font, anchor="ms")
        
    img.save(f'rpg_export/{filename}')

# Generate assets
draw_neon_asset('capa.png', 'Matematica\nNas Estrelas', 'cover')
draw_neon_asset('heroi_1_capitao.png', 'Capitao Estelar', 'hero')
draw_neon_asset('heroi_2_sombra.png', 'Sombra Neon', 'hero')
draw_neon_asset('heroi_3_tecnomago.png', 'Tecnomago', 'hero')
draw_neon_asset('heroi_4_saqueador.png', 'Saqueador', 'hero')
draw_neon_asset('heroi_5_ciborgue.png', 'Ciborgue Titanio', 'hero')
draw_neon_asset('chefe_1_devorador.png', 'Devorador', 'boss')
draw_neon_asset('chefe_2_nebulosa.png', 'Nebulosa Fantasma', 'boss')
draw_neon_asset('chefe_3_tita.png', 'Tita Cibernetico', 'boss')
draw_neon_asset('dado_d20.png', 'Dado D20', 'dice')
draw_neon_asset('dado_d10.png', 'Dado D10', 'dice')
draw_neon_asset('dado_d6.png', 'Dado D6', 'dice')

# Package into ZIP
zip_path = 'Matematica_Nas_Estrelas_DevPack.zip'
with zipfile.ZipFile(zip_path, 'w') as zipf:
    for root, dirs, files in os.walk('rpg_export'):
        for file in files:
            zipf.write(os.path.join(root, file), file)
            
print(f"[file-tag: {zip_path}]")