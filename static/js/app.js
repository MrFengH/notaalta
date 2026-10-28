/* Nota Alta: interacciones de la tienda y del panel (JavaScript sin dependencias). */
(() => {
  "use strict";

  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));

  /* ---------- Paneles <dialog> (menú móvil, filtros) ---------- */
  document.addEventListener("click", (event) => {
    const opener = event.target.closest("[data-dialog-open]");
    if (opener) {
      const dialog = document.getElementById(opener.dataset.dialogOpen);
      if (dialog) {
        dialog.showModal();
        opener.setAttribute("aria-expanded", "true");
        dialog.addEventListener("close", () => {
          opener.setAttribute("aria-expanded", "false");
          opener.focus();
        }, { once: true });
      }
      return;
    }
    if (event.target.closest("[data-dialog-close]")) {
      event.target.closest("dialog")?.close();
      return;
    }
    // Clic sobre el fondo del <dialog> lo cierra
    if (event.target instanceof HTMLDialogElement && event.target.open) {
      const r = event.target.getBoundingClientRect();
      const inside = event.clientX >= r.left && event.clientX <= r.right && event.clientY >= r.top && event.clientY <= r.bottom;
      if (!inside) event.target.close();
    }
  });

  /* ---------- Avisos (toasts) ---------- */
  const toastRegion = $("[data-toasts]");
  const dismiss = (toast) => {
    if (!toast || toast.dataset.leaving) return;
    toast.dataset.leaving = "1";
    setTimeout(() => toast.remove(), 220);
  };
  const armToast = (toast) => {
    let timer = setTimeout(() => dismiss(toast), 5000);
    toast.addEventListener("mouseenter", () => clearTimeout(timer));
    toast.addEventListener("focusin", () => clearTimeout(timer));
    toast.addEventListener("mouseleave", () => { timer = setTimeout(() => dismiss(toast), 2500); });
  };
  $$("[data-toast]").forEach(armToast);
  document.addEventListener("click", (event) => {
    const btn = event.target.closest("[data-toast-close]");
    if (btn) dismiss(btn.closest("[data-toast]"));
  });

  const ICONS = { ok: "ph-check-circle text-success", warn: "ph-warning text-warn" };
  const showToast = (text, ok = true) => {
    const tpl = $("#toast-template");
    if (!tpl || !toastRegion) return;
    const node = tpl.content.firstElementChild.cloneNode(true);
    $("[data-toast-text]", node).textContent = text;
    $("[data-toast-icon]", node).className = `ph ${ok ? ICONS.ok : ICONS.warn} mt-0.5 text-xl`;
    toastRegion.append(node);
    armToast(node);
  };

  /* ---------- Agregar al carrito sin recargar ---------- */
  const updateCartCount = (count) => {
    $$("[data-cart-count]").forEach((badge) => {
      badge.textContent = count;
      badge.classList.toggle("hidden", !count);
    });
    $$("[data-cart-link]").forEach((link) => {
      link.setAttribute("aria-label", `Carrito, ${count} artículo${count === 1 ? "" : "s"}`);
    });
  };

  document.addEventListener("submit", async (event) => {
    const form = event.target.closest("[data-add-to-cart]");
    if (!form) return;
    event.preventDefault();
    const button = $("button[type=submit]", form);
    const label = button.innerHTML;
    button.disabled = true;
    button.setAttribute("aria-busy", "true");
    button.innerHTML = '<i class="ph ph-circle-notch animate-spin" aria-hidden="true"></i>Agregando';
    try {
      const response = await fetch(form.action, {
        method: "POST",
        body: new FormData(form),
        headers: { "X-Requested-With": "fetch" },
      });
      if (!response.ok) throw new Error(response.statusText);
      const data = await response.json();
      updateCartCount(data.count);
      showToast(data.message, data.ok);
    } catch {
      form.submit(); // sin conexión con fetch: envío normal
      return;
    } finally {
      button.disabled = false;
      button.removeAttribute("aria-busy");
      button.innerHTML = label;
    }
  });

  /* ---------- Filtros del catálogo: aplicar al cambiar ---------- */
  $$("[data-autosubmit]").forEach((form) => {
    form.addEventListener("change", (event) => {
      if (event.target.matches("input[type=number]")) return; // precio: se aplica con el botón
      form.requestSubmit();
    });
  });

  /* ---------- Galería del detalle de producto ---------- */
  const gallery = $("[data-gallery]");
  if (gallery) {
    const main = $("[data-gallery-main]", gallery);
    $$("[data-gallery-thumb]", gallery).forEach((thumb) => {
      thumb.addEventListener("click", () => {
        main.src = thumb.dataset.src;
        main.alt = thumb.dataset.alt;
        $$("[data-gallery-thumb]", gallery).forEach((t) => t.setAttribute("aria-pressed", String(t === thumb)));
      });
    });
  }

  /* ---------- Selector de cantidad ---------- */
  document.addEventListener("click", (event) => {
    const step = event.target.closest("[data-qty-step]");
    if (!step) return;
    const input = $("input", step.closest("[data-qty]"));
    const next = Number(input.value || 0) + Number(step.dataset.qtyStep);
    const min = Number(input.min || 0);
    const max = Number(input.max || 999);
    input.value = Math.min(Math.max(next, min), max);
    input.dispatchEvent(new Event("change", { bubbles: true }));
  });
  // En el carrito, la cantidad se guarda al cambiar
  $$("[data-qty-autosubmit]").forEach((form) => {
    form.addEventListener("change", () => form.requestSubmit());
  });

  /* ---------- Checkout: resumen según envío ---------- */
  const summary = $("[data-checkout-summary]");
  if (summary) {
    const fmt = new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" });
    const base = Number(summary.dataset.base);
    const refresh = () => {
      const checked = $("input[name=shipping_method]:checked");
      if (!checked) return;
      const cost = Number(checked.dataset.cost);
      $("[data-shipping-cost]", summary).textContent = cost ? fmt.format(cost) : "Gratis";
      $("[data-grand-total]", summary).textContent = fmt.format(base + cost);
    };
    document.addEventListener("change", (event) => {
      if (event.target.name === "shipping_method") refresh();
    });
    refresh();
  }

  /* ---------- Resumen de errores: llevar el foco al cargar ---------- */
  $("[data-autofocus]")?.focus();

  /* ---------- Confirmación antes de acciones destructivas ---------- */
  document.addEventListener("submit", (event) => {
    const msg = event.target.dataset?.confirm;
    if (msg && !window.confirm(msg)) event.preventDefault();
  });
})();
