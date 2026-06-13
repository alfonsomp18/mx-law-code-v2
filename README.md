# 📋 mexico-fiscal-catalog

Índice y tracker del Marco Fiscal Federal de México.  
Este repositorio **solo contiene el catálogo** — no los archivos de leyes.  
Los archivos transformados (.md) van en el repositorio principal `mexico-law-as-code`.

---

## ¿Qué contiene este repo?

| Archivo | Para qué sirve |
|---|---|
| `catalog.json` | El índice completo: 80+ leyes con sus URLs, status y metadatos |
| `README.md` | Este archivo |

---

## Estados disponibles (`status`)

| Valor | Significado |
|---|---|
| `sin_iniciar` | No se ha hecho nada con este documento |
| `descargado_local` | Archivo descargado en tu computadora (PDF o DOCX), aún no en GitHub |
| `en_revision` | Descargado, revisando manualmente antes de transformar |
| `transformado_md` | Convertido exitosamente a formato .md con el script Python |
| `publicado_github` | Archivo .md publicado y visible en `mexico-law-as-code` |
| `desactualizado` | Tiene una reforma más reciente disponible, requiere actualización |
| `no_disponible` | No se encontró fuente oficial descargable |

---

## Cómo actualizar el catálogo cuando avanzas con una ley

1. Abre `catalog.json` en VS Code
2. Busca la ley por su `id` (ej: `"id": "LISR"`)
3. Edita los campos que correspondan:
   - `"status"` → cambia al estado actual
   - `"fecha_descarga"` → agrega la fecha (formato: `"2026-05-23"`)
   - `"formato_descargado"` → `"PDF"` o `"DOCX"`
   - `"ruta_local"` → ruta en tu computadora
   - `"ruta_github"` → ruta dentro de `mexico-law-as-code`
   - `"ultima_reforma_dof"` → fecha de la última reforma del documento
   - `"notas"` → cualquier observación relevante
4. Guarda el archivo (`Ctrl + S`)
5. Sube el cambio a GitHub (ver instrucciones abajo)

---

## Jerarquía normativa fiscal (niveles)

| Nivel | Nombre | Ejemplo |
|---|---|---|
| 1 | Constitución Política | CPEUM |
| 2 | Tratados Internacionales | T-MEC, CDTs |
| 3 | Código Marco Fiscal | CFF, CPF-Fiscal, LFDC |
| 4 | Leyes Fiscales Especiales | LISR, LIVA, LIEPS, LA |
| 5 | Leyes con Impacto Fiscal Indirecto | CCF, LFT, LSS, LGSM |
| 6 | Reglamentos | RCFF, RLISR, RLIVA |
| 7 | Disposiciones Administrativas y Jurisprudencia | RMF, SCJN, TFJA |

**Supletoriedad (Art. 5 CFF):** Ley especial → CFF → Derecho federal común → Constitución.

---

## Repositorios del proyecto

- **Este repo** (`mexico-fiscal-catalog`): solo el índice/tracker
- **Repo principal** (`mexico-law-as-code`): los archivos .md de cada ley
