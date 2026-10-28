---
name: Nota Alta
description: Perfumería online de marcas originales para Panamá; la fotografía y el precio mandan.
colors:
  ground: "#f1f2ee"
  surface: "#fafaf8"
  paper: "#ffffff"
  sage: "#e4e8e1"
  line: "#d5dad2"
  line-strong: "#7e8983"
  ink: "#1c2622"
  ink-soft: "#56625c"
  ink-faint: "#6b7770"
  pine: "#23463c"
  pine-deep: "#183229"
  pine-tint: "#dce7e1"
  on-pine-soft: "#c9d8d0"
  sale: "#b8431f"
  sale-deep: "#a63b1a"
  sale-tint: "#f6e3da"
  warn: "#7a4e00"
  warn-tint: "#fbefd6"
  danger: "#a1271b"
  danger-tint: "#fde7e4"
  info: "#284866"
  info-tint: "#e3ebf3"
  success: "#1f5137"
  success-tint: "#ddefe3"
typography:
  display:
    fontFamily: "Schibsted Grotesk, ui-sans-serif, system-ui, Segoe UI, sans-serif"
    fontSize: "clamp(2.6rem, 2rem + 2.4vw, 3.5rem)"
    fontWeight: 600
    lineHeight: 1.02
    letterSpacing: "-0.04em"
    fontFeature: "ss01"
  headline:
    fontFamily: "Schibsted Grotesk, ui-sans-serif, system-ui, Segoe UI, sans-serif"
    fontSize: "2.25rem"
    fontWeight: 600
    lineHeight: 1.05
    letterSpacing: "-0.02em"
    fontFeature: "ss01"
  section:
    fontFamily: "Schibsted Grotesk, ui-sans-serif, system-ui, Segoe UI, sans-serif"
    fontSize: "1.875rem"
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: "-0.02em"
    fontFeature: "ss01"
  title:
    fontFamily: "Schibsted Grotesk, ui-sans-serif, system-ui, Segoe UI, sans-serif"
    fontSize: "1rem"
    fontWeight: 600
    lineHeight: 1.375
    fontFeature: "ss01"
  body:
    fontFamily: "Schibsted Grotesk, ui-sans-serif, system-ui, Segoe UI, sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.5
    fontFeature: "ss01"
  lede:
    fontFamily: "Schibsted Grotesk, ui-sans-serif, system-ui, Segoe UI, sans-serif"
    fontSize: "1.125rem"
    fontWeight: 400
    lineHeight: 1.625
    fontFeature: "ss01"
  label:
    fontFamily: "Schibsted Grotesk, ui-sans-serif, system-ui, Segoe UI, sans-serif"
    fontSize: "0.875rem"
    fontWeight: 500
    lineHeight: 1.25
    fontFeature: "ss01"
  meta:
    fontFamily: "Schibsted Grotesk, ui-sans-serif, system-ui, Segoe UI, sans-serif"
    fontSize: "13px"
    fontWeight: 400
    lineHeight: 1.4
    fontFeature: "ss01"
  badge:
    fontFamily: "Schibsted Grotesk, ui-sans-serif, system-ui, Segoe UI, sans-serif"
    fontSize: "0.75rem"
    fontWeight: 600
    lineHeight: 1
    fontFeature: "ss01"
rounded:
  sm: "2px"
  full: "9999px"
spacing:
  gutter-mobile: "16px"
  gutter-tablet: "24px"
  gutter-desktop: "40px"
  grid-gap: "16px"
  grid-gap-lg: "24px"
  block: "32px"
  section: "96px"
  container-max: "1360px"
components:
  button-primary:
    backgroundColor: "{colors.pine}"
    textColor: "{colors.surface}"
    typography: "{typography.label}"
    rounded: "{rounded.sm}"
    padding: "0 20px"
    height: "44px"
  button-primary-hover:
    backgroundColor: "{colors.pine-deep}"
  button-secondary:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.sm}"
    padding: "0 20px"
    height: "44px"
  button-secondary-hover:
    backgroundColor: "{colors.paper}"
  button-ghost:
    textColor: "{colors.ink}"
    rounded: "{rounded.sm}"
    padding: "0 20px"
    height: "44px"
  button-ghost-hover:
    backgroundColor: "{colors.sage}"
  button-on-pine:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.pine}"
    rounded: "{rounded.sm}"
    padding: "0 20px"
    height: "44px"
  button-danger:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.danger}"
    rounded: "{rounded.sm}"
    padding: "0 20px"
    height: "44px"
  button-danger-hover:
    backgroundColor: "{colors.danger-tint}"
  button-small:
    rounded: "{rounded.sm}"
    padding: "0 14px"
    height: "36px"
  button-icon:
    textColor: "{colors.ink}"
    rounded: "{rounded.sm}"
    size: "44px"
  input:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    typography: "{typography.body}"
    rounded: "{rounded.sm}"
    padding: "0 12px"
    height: "44px"
  choice:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    rounded: "{rounded.sm}"
    padding: "16px"
  choice-checked:
    backgroundColor: "{colors.pine-tint}"
  badge-sale:
    backgroundColor: "{colors.sale}"
    textColor: "{colors.paper}"
    typography: "{typography.badge}"
    rounded: "{rounded.sm}"
    padding: "0 8px"
    height: "24px"
  badge-coupon:
    backgroundColor: "{colors.sale-tint}"
    textColor: "{colors.sale-deep}"
    typography: "{typography.badge}"
    rounded: "{rounded.sm}"
    padding: "0 8px"
    height: "24px"
  badge-sold-out:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.surface}"
    typography: "{typography.badge}"
    rounded: "{rounded.sm}"
    height: "24px"
  tone-brand:
    backgroundColor: "{colors.pine-tint}"
    textColor: "{colors.pine}"
    rounded: "{rounded.sm}"
  tone-warn:
    backgroundColor: "{colors.warn-tint}"
    textColor: "{colors.warn}"
    rounded: "{rounded.sm}"
  tone-danger:
    backgroundColor: "{colors.danger-tint}"
    textColor: "{colors.danger}"
    rounded: "{rounded.sm}"
  tone-info:
    backgroundColor: "{colors.info-tint}"
    textColor: "{colors.info}"
    rounded: "{rounded.sm}"
  tone-success:
    backgroundColor: "{colors.success-tint}"
    textColor: "{colors.success}"
    rounded: "{rounded.sm}"
  tone-neutral:
    backgroundColor: "{colors.sage}"
    textColor: "{colors.ink}"
    rounded: "{rounded.sm}"
  cart-count:
    backgroundColor: "{colors.sale}"
    textColor: "{colors.paper}"
    rounded: "{rounded.full}"
    height: "18px"
  panel:
    backgroundColor: "{colors.surface}"
    rounded: "{rounded.sm}"
  photo-mat:
    backgroundColor: "{colors.sage}"
    rounded: "{rounded.sm}"
    padding: "7%"
  photo-tile:
    backgroundColor: "{colors.sage}"
    rounded: "{rounded.sm}"
  toast:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    rounded: "{rounded.sm}"
    padding: "12px 16px"
  promo-band:
    backgroundColor: "{colors.pine}"
    textColor: "{colors.surface}"
  footer:
    backgroundColor: "{colors.pine}"
    textColor: "{colors.on-pine-soft}"
  dashboard-nav-item-active:
    backgroundColor: "{colors.pine-tint}"
    textColor: "{colors.pine}"
    rounded: "{rounded.sm}"
    height: "40px"
---

# Design System: Nota Alta

## Overview

**Creative North Star: "El mostrador de niebla y pino"**

Nota Alta es una perfumería estándar de categoría ejecutada con el acabado de Aesop y Le Labo/Byredo: el frasco fotografiado y el precio honesto son los protagonistas, y todo lo demás retrocede. El fondo es una niebla fría casi blanca, la tinta es un verde pino casi negro, y el pino pleno aparece solo en regiones comprometidas (botón primario, banda de promoción, pie, barra de aviso). Un único color cálido, el caqui persimón, existe exclusivamente para hablar de dinero ahorrado.

La densidad es de tienda real, no de revista: cuadrículas de producto de 2 a 4 columnas, buscador siempre visible, filtros a mano. La expresión vive en la fotografía (sobre paspartú salvia en las rejillas, a sangre en lo editorial), en una sola familia tipográfica trabajada con tracking negativo y peso 600, y en una geometría casi recta de 2px. El tema es solo claro, por decisión.

Rechazos confirmados: el negro con dorado "premium" y el crema con latón; ilustración vectorial en lugar de foto de producto.

El panel (/panel/) es una superficie de operación que hereda los mismos tokens con menos expresión: barra lateral, tablas de datos, sin fotografía editorial ni animación de entrada.

**Key Characteristics:**
- Niebla fría (#f1f2ee) de fondo, tinta pino (#1c2622), campo pino (#23463c) en regiones comprometidas.
- Caqui persimón (#b8431f) reservado a rebajas, cupones y contador del carrito.
- Una sola familia: Schibsted Grotesk, 600 en titulares con tracking negativo.
- Esquinas de 2px en todo; redondo completo solo en indicadores pequeños.
- Foto de producto sobre paspartú salvia en rejillas; foto a sangre en baldosas editoriales.
- Plano: filetes en vez de sombras; una única sombra flotante para capas temporales.
- Movimiento mínimo: una revelación del hero y el ascenso de su texto.

## Colors

Paleta fría y vegetal de bajo croma, con un solo acento cálido que significa "precio rebajado".

### Primary
- **Pino de campo** (pine): botón primario, barra de aviso de envío, banda de promoción, pie, selección de texto, anillo de foco, estado activo de navegación (subrayado de 2px) y pasos completados de la línea de tiempo del pedido. Su versión profunda (pine-deep) es solo el hover del primario.
- **Pino velado** (pine-tint): fondo de la opción seleccionada (al 50%), del ítem activo del panel y de los avisos informativos de marca (envío gratis, ayuda en el login).
- **Salvia suave sobre pino** (on-pine-soft): texto secundario sobre campos pino (pie, promoción).

### Secondary
- **Caqui persimón** (sale): precio rebajado, insignia de descuento, enlace "Ofertas", líneas de cupón en los resúmenes y el contador del carrito. Sale-deep y sale-tint forman el chip de cupón (borde discontinuo).

### Tertiary
- **Tonos de estado** (warn, danger, info, success con sus tint): exclusivamente estados de pedido y avisos del sistema, siempre como par tinte de fondo + tono de texto. Danger también marca campos con error.

### Neutral
- **Niebla fría** (ground): fondo de página de tienda y panel; hover de filas de tabla.
- **Superficie** (surface): paneles, celdas de las rejillas de servicio y marcas, barra lateral del panel, texto sobre pino.
- **Papel** (paper): interior de campos, opciones seleccionables, avisos (toast) y el hover que "aclara" superficies.
- **Salvia** (sage): baldosa y paspartú de fotografía, hover de botones fantasma e icono, tono neutral.
- **Filete** (line): bordes de paneles, separadores, rejillas de 1px (gap-px sobre fondo de filete).
- **Filete fuerte** (line-strong): bordes de campos y botón secundario; hover de paneles.
- **Tinta / tinta suave / tinta tenue** (ink, ink-soft, ink-faint): texto principal; metadatos, marca, descripciones; placeholders.

### Named Rules
**The Caqui Reservado Rule.** El caqui persimón solo dice "ahorro": precio rebajado, % de descuento, cupón, enlace de Ofertas y contador del carrito. Nunca decoración, nunca énfasis genérico, nunca error.

**The Campo Comprometido Rule.** El pino pleno ocupa regiones enteras y con función (botón primario, banda de aviso, promoción, pie). No se usa en franjas decorativas ni en textos de acento sueltos.

**The Par de Tono Rule.** Los estados siempre se expresan como tinte de fondo + tono de texto de la misma familia; nunca un tono saturado de fondo con texto blanco, salvo la insignia de rebaja.

## Typography

**Display Font:** Schibsted Grotesk (con ui-sans-serif, system-ui, Segoe UI)
**Body Font:** Schibsted Grotesk
**Label/Mono Font:** la misma familia; no hay monoespaciada.

**Character:** Una grotesca editorial de periódico, apretada y segura en titulares (600, tracking negativo) y neutra en lectura. La alternativa estilística ss01 está activada en todo el documento.

### Hierarchy
- **Display** (600, 2.6rem a 3.5rem, 1.02, -0.04em): solo el titular del hero de Inicio.
- **Headline** (600, 2.25rem a 3rem, -0.02em): H1 de página (catálogo, carrito, checkout, perfil, marcas); el titular de la banda de promoción.
- **Section** (600, 1.875rem a 2.25rem, -0.02em): H2 de sección en la tienda. En el panel las secciones bajan a 16px semibold.
- **Title** (600, 15 a 16px, 1.375): nombre de producto en tarjeta, títulos de bloques.
- **Body** (400, 16px, 1.5): texto general; **Lede** (18px, 1.625, max 42 a 60ch) para subtítulos de hero y de sección.
- **Label** (500, 14px): etiquetas de formulario, botones pequeños; botones normales a 15px/500.
- **Meta** (400, 13px, ink-soft): marca sobre el nombre, línea de especificaciones.
- **Badge** (600, 12px): insignias y tonos de estado; encabezados de tabla del panel.

Precios: 600 (price) a 18px en tarjeta, 20px en ofertas, 30px en detalle; precio anterior tachado en ink-soft a 14px.

### Named Rules
**The Una Voz Rule.** Una sola familia en todo el sistema; la jerarquía sale de tamaño, peso 600 y tracking negativo, nunca de una segunda fuente.

**The Cifras Proporcionales Rule.** Los precios y cifras usan los numerales por defecto de Schibsted. No se activan numerales tabulares (tnum): en esta familia se leen como monoespaciados. La alineación en tablas se resuelve alineando a la derecha.

**The Sin Mayúsculas Rule.** No hay etiquetas en versalitas ni mayúsculas espaciadas; la única excepción funcional es el código de cupón (campo en mayúsculas y chip con tracking 0.08em).

## Layout

Contenedor centrado de 1360px como máximo con márgenes de 16px (móvil), 24px (sm) y 40px (lg). Móvil primero: el buscador ocupa su propia fila en móvil y pasa al centro de la cabecera desde md; la navegación principal aparece desde lg y en móvil vive en una hoja lateral.

Ritmo vertical de tienda: secciones separadas por 96px (80px en la primera tras el hero), 32px entre el titular de sección y su contenido. Rejillas de producto de 2 columnas en móvil, 3 en md y 4 en lg, con 16px de gap horizontal (24px en lg) y 40px vertical. El hero se divide 5/7 en xl (6/6 en lg) con la foto a toda la altura del primer viewport. Las categorías usan una rejilla asimétrica 1.25fr/1fr con la primera baldosa en dos filas. Las familias olfativas se convierten en carrusel con scroll-snap en móvil y en 4 columnas en lg.

Rejillas de filete: listas de servicios y marcas se componen con gap de 1px sobre fondo de filete, celdas de superficie y un solo borde exterior.

Panel: barra lateral fija de 240px desde lg (hoja lateral en móvil), contenido de hasta 1400px, encabezado de página con acciones a la derecha. Las tablas ocultan columnas progresivamente en pantallas estrechas y los estados pueden partirse en dos líneas en lugar de recortarse.

Cabecera: barra de aviso pino de 36px, cabecera fija de 64px sobre niebla con filete inferior, fila de navegación de 44px con subrayado activo de 2px en pino.

## Elevation & Depth

Sistema plano. La profundidad se comunica con tono (niebla, superficie, papel) y filetes de 1px, no con sombras. Solo las capas temporales que flotan sobre la página (hojas laterales y avisos toast) llevan sombra, con un velo de tinta al 45% detrás de las hojas.

### Shadow Vocabulary
- **Flotante** (`box-shadow: 0 6px 16px -6px rgb(28 38 34 / 0.2), 0 1px 3px rgb(28 38 34 / 0.08)`): hojas laterales (menú móvil, filtros, menú del panel) y toasts. Nada más.

### Named Rules
**The Plano Por Defecto Rule.** Tarjetas, paneles, botones y fotos no tienen sombra. Si algo necesita separarse, usa un filete o un cambio de superficie.

## Shapes

Una sola esquina: 2px en botones, campos, paneles, insignias, fotos, baldosas y la imagen dentro del paspartú. El redondo completo se reserva a indicadores pequeños: contador del carrito, círculos de los pasos de la línea de tiempo del pedido, puntos de radio en filtros y el icono de confirmación. Los cupones se dibujan con borde discontinuo, como un vale recortable. Las baldosas de categoría llevan un degradado de tinta desde abajo para sostener el texto blanco sobre la foto.

**The Dos Píxeles Rule.** Todo rectángulo lleva 2px; no existen radios intermedios (4, 8, 12px). Si no es un indicador pequeño, no es redondo.

## Components

### Buttons
Rectos, firmes y de altura táctil.
- **Shape:** esquina casi recta (2px), altura 44px (36px en la variante pequeña), 15px/500, icono Phosphor opcional con 8px de separación.
- **Primary:** campo pino con texto superficie, 20px de padding horizontal. Hover a pino profundo.
- **Secondary:** superficie con borde filete fuerte y texto tinta; hover oscurece el borde a tinta y aclara el fondo a papel. Es el botón "Agregar" de las tarjetas.
- **Ghost / Icon:** sin fondo; hover salvia. Los botones de icono son cuadrados de 44px.
- **On-pine:** superficie con texto pino, para acciones sobre campos pino.
- **Danger:** superficie con borde y texto danger; hover tinte danger.
- **States:** transición de 200ms con ease-out-expo; activo baja 1px; deshabilitado al 45% de opacidad. Foco: contorno pino de 2px con 2px de separación (global).

### Chips
- **Insignia de rebaja:** caqui pleno con texto blanco, "-N%", sobre la esquina superior izquierda de la foto.
- **Cupón:** tinte caqui, texto caqui profundo, borde discontinuo; icono de ticket.
- **Agotado:** tinta plena con texto superficie.
- **Tonos de estado:** par tinte + tono (neutral, brand, warn, danger, info, success) para estados de pedido; 24px de alto, 12px/600.

### Cards / Containers
- **Tarjeta de producto:** sin caja. Foto en paspartú 4:5, luego marca (meta), nombre (title), descripción de dos líneas, especificaciones, cupón opcional, precio y botón secundario de bloque pegado abajo.
- **Panel:** superficie con filete y 2px; padding según contenido (12 a 24px). Hover a filete fuerte cuando es enlazable.
- **Shadow Strategy:** ninguna (ver Elevation & Depth).

### Inputs / Fields
- **Style:** papel con borde filete fuerte, 2px, 44px de alto, 16px de texto, placeholder tinta tenue, caret pino. Select con chevrón propio.
- **Focus:** borde pino con anillo de 3px de pino al 20%.
- **Error:** borde danger y anillo danger; mensaje en danger 14px/500 con icono debajo del campo.
- **Choice (envío, pago):** caja papel con filete; seleccionada pasa a borde pino y fondo pino velado.

### Navigation
- **Tienda:** enlaces a 15px en tinta suave; activo en tinta semibold con subrayado pino de 2px; hover subrayado filete fuerte. "Ofertas" va a la derecha en caqui con icono de etiqueta. En móvil, hoja lateral con filas de 56px separadas por filetes.
- **Panel:** barra lateral superficie, ítems de 40px con icono; activo en pino velado con texto pino semibold, hover niebla.

### Fotografía de producto (signature)
- **Paspartú:** en toda rejilla de producto la foto se asienta dentro de una baldosa salvia con 7% de margen interior, ambas a 2px. Así frascos de distinto encuadre conviven en la misma cuadrícula.
- **Baldosa editorial:** en hero, promoción, familias y ofertas la foto llena la baldosa salvia a sangre.
- **Sin zoom:** las fotos no escalan al pasar el cursor; el gesto de hover es la flecha que avanza 4px o el subrayado del nombre.

### Motion
- **Revelación del hero:** recorte que se abre desde abajo con leve desescalado (1100ms, ease-out-expo).
- **Ascenso:** titular, subtítulo y botones del hero suben 14px y aparecen (700ms, escalonados 0/90/160ms). Los toasts reutilizan el ascenso (420ms); las hojas entran deslizando (380ms).
- Todo se colapsa a 1ms con prefers-reduced-motion.

### Tabla de datos (panel)
Texto de 14px, encabezados fijos en superficie a 12px/600 tinta suave, filas con filete inferior y hover niebla; números alineados a la derecha sin cortes de línea.

## Do's and Don'ts

### Do:
- **Do** presentar toda foto de producto en rejilla sobre paspartú salvia (7% de margen) y la foto editorial a sangre en baldosa salvia.
- **Do** usar 2px en toda esquina y redondo completo solo en indicadores pequeños (contador, pasos, puntos de radio).
- **Do** mostrar el precio rebajado en caqui junto al precio anterior tachado en tinta suave y la insignia "-N%".
- **Do** expresar estados de pedido con el par tinte + tono de la misma familia.
- **Do** separar superficies con filetes de 1px (#d5dad2) y rejillas gap-px antes que con sombras.
- **Do** usar iconos Phosphor regular, en tinta suave o pino, siempre con aria-hidden junto a texto.
- **Do** mantener el panel en los mismos tokens con menos expresión: sin fotografía editorial ni animaciones de entrada.

### Don't:
- **Don't** usar el caqui para errores, campos obligatorios, decoración o énfasis que no sea ahorro.
- **Don't** usar negro con dorado ni crema con latón como señal de lujo.
- **Don't** añadir una segunda familia tipográfica ni activar numerales tabulares.
- **Don't** aplicar zoom al pasar el cursor sobre fotos de producto.
- **Don't** añadir sombras a tarjetas, paneles o botones; la sombra flotante es solo para hojas y toasts.
- **Don't** introducir tema oscuro; el sistema es solo claro por decisión.
- **Don't** añadir animaciones más allá de la revelación del hero, el ascenso de su texto, toasts y hojas.
- **Don't** usar ilustraciones vectoriales en lugar de fotografía real de frascos.
