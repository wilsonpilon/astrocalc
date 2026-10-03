# Matematica nas Estrelas - MSX

Projeto MSX2 em C/SDCC usando a MSXgl e MSX-DOS 2.

## Requisitos do jogo

- MSX2 ou superior
- 128 KB de VRAM
- Memory Mapper de 256 KB
- MSX-DOS 2 ou Nextor

## Compilar

No Windows:

```bat
build.bat
```

O script usa pelo WSL as versoes Linux das ferramentas incluidas na propria
MSXgl. Isso evita o bloqueio do `sdcpp.exe` pela politica de controle de
aplicativos do Windows desta maquina.

Arquivos principais gerados:

```text
out\matstar.com
emul\dos2\matstar.com
emul\dsk\DOS2_matstar.dsk
```

## Testar

```bat
run.bat
```

O disco inicia o MSX-DOS 2 e executa `MATSTAR.COM` automaticamente. O programa
entra em SCREEN 5, mostra informacoes do VDP, DOS e Memory Mapper e retorna
limpamente ao DOS quando ESC e pressionado.
