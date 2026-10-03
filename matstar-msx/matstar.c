// ____________________________
// ██▀▀█▀▀██▀▀▀▀▀▀▀█▀▀█        │   ▄▄▄                ▄▄
// ██  ▀  █▄  ▀██▄ ▀ ▄█ ▄▀▀ █  │  ▀█▄  ▄▀██ ▄█▄█ ██▀▄ ██  ▄███
// █  █ █  ▀▀  ▄█  █  █ ▀▄█ █▄ │  ▄▄█▀ ▀▄██ ██ █ ██▀  ▀█▄ ▀█▄▄
// ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀────────┘                 ▀▀
//  Matematica nas Estrelas - MSX-DOS 2 bootstrap
//─────────────────────────────────────────────────────────────────────────────

//=============================================================================
// INCLUDES
//=============================================================================
#include "msxgl.h"
#include "dos.h"
#include "dos_mapper.h"

//=============================================================================
// DEFINES
//=============================================================================

// Fonts data
#include "font/font_mgl_sample6.h"

// Sign-of-life animation
const u8 g_ChrAnim[] = { '-', '/', '|', '\\' };

//=============================================================================
// FUNCTIONS
//=============================================================================

//-----------------------------------------------------------------------------
// Get total Memory Mapper capacity in kilobytes
u16 GetMapperSize()
{
	DOS_VarTable* mapper = DOSMapper_GetVarTable();
	u16 segments = 0;

	while (mapper && (mapper->Slot != 0))
	{
		segments += mapper->NumSeg;
		mapper++;
	}

	return segments * 16;
}

//-----------------------------------------------------------------------------
// Get detected VDP name
const c8* GetVDPName()
{
	switch (VDP_GetVersion())
	{
	case VDP_VERSION_V9938:
		return "V9938 / MSX2";

	case VDP_VERSION_V9958:
		return "V9958 / MSX2+";
	}

	return "Nao suportado";
}

//=============================================================================
// MAIN LOOP
//=============================================================================

//-----------------------------------------------------------------------------
// Program entry point
void main(void)
{
	DOS_Version dosVersion;
	bool mapperReady;
	u8 frame = 0;

	DOS_GetVersion(&dosVersion);
	mapperReady = DOSMapper_Init();

	BIOS_SetKeyClick(FALSE);
	VDP_SetMode(VDP_MODE_SCREEN5);
	VDP_SetColor(COLOR_BLACK);
	VDP_EnableVBlank(TRUE);
	VDP_EnableSprite(FALSE);
	VDP_ClearVRAM();

	Print_SetBitmapFont(g_Font_MGL_Sample6);
	Print_SetColor(0xFF, 0x11);

	Print_SetPosition(24, 24);
	Print_DrawText("MATEMATICA NAS ESTRELAS");
	Print_SetPosition(24, 40);
	Print_DrawText("BOOTSTRAP MSX-DOS 2");

	Print_SetPosition(24, 72);
	Print_DrawFormat("Video: %s", GetVDPName());
	Print_SetPosition(24, 88);
	Print_DrawFormat("MSX-DOS: %i.%i", dosVersion.Kernel >> 8, dosVersion.Kernel & 0xFF);
	Print_SetPosition(24, 104);
	if (mapperReady)
		Print_DrawFormat("Memory Mapper: %i KB", GetMapperSize());
	else
		Print_DrawText("Memory Mapper: indisponivel");

	Print_SetPosition(24, 136);
	Print_DrawText("SCREEN 5 ATIVA");
	Print_SetPosition(24, 176);
	Print_DrawText("PRESSIONE ESC PARA SAIR");

	while (!Keyboard_IsKeyPressed(KEY_ESC))
	{
		Halt(); // Wait V-Blank
		Print_SetPosition(255-8, 0);
		Print_DrawChar(g_ChrAnim[(frame++ >> 3) & 0x03]);
	}

	BIOS_Exit(0);
}