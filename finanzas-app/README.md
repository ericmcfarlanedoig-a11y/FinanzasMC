# 💰 Dashboard Financiero Familiar

## Cómo instalar como APP en Mac

### Opción A — Google Chrome (recomendado)
1. Abre Chrome y ve a `Archivo > Abrir archivo…` → selecciona `index.html`
2. En la barra de dirección aparecerá un ícono de instalación (🖥️) a la derecha
3. Haz clic en ese ícono → "Instalar Presupuesto Familiar"
4. La app se abrirá como ventana independiente, sin la barra del navegador
5. Aparecerá en tu Launchpad / Aplicaciones como cualquier otra app

### Opción B — Safari (Mac)
1. Abre el archivo `index.html` directamente en Safari
2. Menú `Archivo > Agregar a Dock`  *(Safari 17+)*
3. La app quedará en tu Dock

### Opción C — Abrir directamente
1. Doble clic en `index.html` → se abre en tu navegador predeterminado
2. Funciona perfectamente sin instalación

---

## Funciones principales

| Función | Descripción |
|---------|-------------|
| 💾 Guardar mes | Guarda un snapshot del mes actual con todos los datos |
| 📄 Exportar PDF | Imprime / exporta como PDF desde el navegador |
| 📥 PNG | Exporta la sección de Gastos Familiares como imagen |
| 🗂️ Historial | Ver, cargar o eliminar meses guardados anteriores |
| + Agregar cuota | Agrega nuevas compras en cuotas directamente |

## Los datos se guardan automáticamente

- Todos los snapshots guardados persisten en `localStorage` del navegador
- Los datos de cuotas también se guardan entre sesiones
- Para exportar un snapshot guardado, usa el botón 📄 en el historial

## Estructura de archivos

```
finanzas-app/
├── index.html      ← La aplicación principal
├── manifest.json   ← Configuración PWA
├── sw.js           ← Service Worker (offline support)
├── icon-192.png    ← Ícono app
├── icon-512.png    ← Ícono app grande
└── README.md       ← Este archivo
```
