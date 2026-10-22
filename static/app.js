// SIGEP Bolivia - Exact Cleaned Grid, Side Panel & Batch Printing Engine

let catalogData = {
  partidas_gasto: [],
  rubros_recurso: [],
  plan_cuentas: [],
  momentos: [],
  fuentes_organismos: [],
  plantillas: []
};

// Current Voucher State
let currentVoucher = {
  id: null,
  entidad: "1814 - GM - GOBIERNO AUTÓNOMO MUNICIPAL DE SAN JOAQUÍN",
  direccion: "DIRECCION ADMINISTRATIVA Y FINANCIERA",
  unidad_ejecutora: "001",
  unidad_ejecutora_desc: "DIRECCION ADMINISTRATIVA Y FINANCIERA",
  numero_cbte: "0000001",
  moneda: "BBS",
  momento_codigo: "12",
  momento_desc: "Devengado de Recursos",
  depositante: "DISTINTOS BENEFICIARIOS",
  beneficiario: "DISTINTOS BENEFICIARIOS",
  fecha: "10/09/2026",
  hora: "10:30:00",
  doc_respaldo: "INFORME DEL CAJERO, ARQUEO DE CAJA",
  dolar: "6.86",
  tipo_cambio: "6.86",
  ufv: "3.36081",
  elaborado_por: "C.T.",
  glosa: "REGISTRO POR LA VENTA DE SERVICIOS, FORMULARIOS (BS. 200), CARATULAS MUNICIPALES (BS. 2000) Y TIMBRES (BS. 700) A DISTINTOS BENEFICIARIOS SEGUN ARQUEO DE CAJA E INFORME DEL CAJERO.",
  grid_rows: []
};

let activeRowIndex = 0;
let savedVouchersList = [];

// ========================================================
// CODE FORMATTER WITH DOTS (AUTOMATIC)
// ========================================================
function formatCodeWithDots(code) {
  if (!code) return "";
  const str = code.toString().trim();
  // If user already typed with dots, preserve it
  if (str.includes(".")) return str;

  const clean = str.replace(/[^0-9]/g, "");
  if (clean.length === 5) {
    return `${clean[0]}.${clean[1]}.${clean[2]}.${clean[3]}.${clean[4]}`;
  } else if (clean.length === 4) {
    return `${clean[0]}.${clean[1]}.${clean[2]}.${clean[3]}`;
  } else if (clean.length === 3) {
    return `${clean[0]}.${clean[1]}.${clean[2]}`;
  } else if (clean.length === 2) {
    return `${clean[0]}.${clean[1]}`;
  }
  return str;
}

// Search Catalogs ignoring dots
function searchCatalogItem(code, type = "any") {
  if (!code) return null;
  const clean = code.toString().replace(/[^0-9]/g, "");
  if (!clean) return null;

  // 1. If searching for CTA or any
  if (type === "cta" || type === "any") {
    const fc = catalogData.plan_cuentas.find(c => c.codigo.replace(/[^0-9]/g, "") === clean);
    if (fc) return { tipo: "cuenta", codigo: fc.codigo, nombre: fc.nombre };
  }

  // 2. If searching for Rubro / Gasto or any
  if (type === "rubro" || type === "any") {
    const fr = catalogData.rubros_recurso.find(r => r.codigo.replace(/[^0-9]/g, "") === clean);
    if (fr) return { tipo: "recurso", codigo: fr.codigo, nombre: fr.nombre };

    const fg = catalogData.partidas_gasto.find(p => p.codigo.replace(/[^0-9]/g, "") === clean);
    if (fg) return { tipo: "gasto", codigo: fg.codigo, nombre: fg.nombre };
  }

  return null;
}

// Spanish Number to Words (Bolivianos)
function numeroALetras(cantidad) {
  const numero = parseFloat(cantidad) || 0;
  const entero = Math.floor(numero);
  const centavos = Math.round((numero - entero) * 100);
  const centavosStr = centavos.toString().padStart(2, '0') + "/100 Bs.";

  if (entero === 0) return "CERO " + centavosStr;

  function Unidades(num) {
    switch (num) {
      case 1: return "UN";
      case 2: return "DOS";
      case 3: return "TRES";
      case 4: return "CUATRO";
      case 5: return "CINCO";
      case 6: return "SEIS";
      case 7: return "SIETE";
      case 8: return "OCHO";
      case 9: return "NUEVE";
      default: return "";
    }
  }

  function DecenasY(strSin, numUnidades) {
    if (numUnidades > 0) return strSin + " Y " + Unidades(numUnidades);
    return strSin;
  }

  function Decenas(num) {
    const decena = Math.floor(num / 10);
    const unidad = num - (decena * 10);
    switch (decena) {
      case 1:
        switch (unidad) {
          case 0: return "DIEZ";
          case 1: return "ONCE";
          case 2: return "DOCE";
          case 3: return "TRECE";
          case 4: return "CATORCE";
          case 5: return "QUINCE";
          default: return "DIECI" + Unidades(unidad);
        }
      case 2:
        switch (unidad) {
          case 0: return "VEINTE";
          default: return "VEINTI" + Unidades(unidad);
        }
      case 3: return DecenasY("TREINTA", unidad);
      case 4: return DecenasY("CUARENTA", unidad);
      case 5: return DecenasY("CINCUENTA", unidad);
      case 6: return DecenasY("SESENTA", unidad);
      case 7: return DecenasY("SETENTA", unidad);
      case 8: return DecenasY("OCHENTA", unidad);
      case 9: return DecenasY("NOVENTA", unidad);
      case 0: return Unidades(unidad);
      default: return "";
    }
  }

  function Centenas(num) {
    const centenas = Math.floor(num / 100);
    const decenas = num - (centenas * 100);
    switch (centenas) {
      case 1:
        if (decenas > 0) return "CIENTO " + Decenas(decenas);
        return "CIEN";
      case 2: return "DOSCIENTOS " + Decenas(decenas);
      case 3: return "TRESCIENTOS " + Decenas(decenas);
      case 4: return "CUATROCIENTOS " + Decenas(decenas);
      case 5: return "QUINIENTOS " + Decenas(decenas);
      case 6: return "SEISCIENTOS " + Decenas(decenas);
      case 7: return "SETECIENTOS " + Decenas(decenas);
      case 8: return "OCHOCIENTOS " + Decenas(decenas);
      case 9: return "NOVECIENTOS " + Decenas(decenas);
      default: return Decenas(decenas);
    }
  }

  function Miles(num) {
    const divisor = 1000;
    const cientos = Math.floor(num / divisor);
    const resto = num - (cientos * divisor);
    let strMiles = "";
    let strCentenas = "";

    if (cientos === 1) strMiles = "MIL";
    if (cientos > 1) strMiles = Centenas(cientos) + " MIL";

    if (resto > 0) strCentenas = Centenas(resto);

    if (strMiles === "") return strCentenas;
    return (strMiles + " " + strCentenas).trim();
  }

  function Millones(num) {
    const divisor = 1000000;
    const cientos = Math.floor(num / divisor);
    const resto = num - (cientos * divisor);
    let strMillones = "";
    let strMiles = "";

    if (cientos === 1) strMillones = "UN MILLON";
    if (cientos > 1) strMillones = Centenas(cientos) + " MILLONES";

    if (resto > 0) strMiles = Miles(resto);

    if (strMillones === "") return strMiles;
    return (strMillones + " " + strMiles).trim();
  }

  const literal = Millones(entero);
  return ("Son: " + literal.trim() + " " + centavosStr).toUpperCase();
}

function formatMoney(val) {
  if (val === "" || val === null || val === undefined) return "0.00";
  const num = parseFloat(val);
  if (isNaN(num)) return "0.00";
  return num.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

function getFormattedCurrentDate() {
  const d = new Date();
  const day = String(d.getDate()).padStart(2, '0');
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const year = d.getFullYear();
  return `${day}/${month}/${year}`;
}

// Initialize Application
document.addEventListener("DOMContentLoaded", async () => {
  await loadCatalogData();
  setupKeyboardShortcuts();
  populateMomentosSelector();
  populatePlantillasSelector();

  // Load saved vouchers into the side panel
  await cargarListaComprobantes();

  // Start completely in blank as requested (direct for entry #1)
  nuevoComprobante();

  // Live BCB Sync
  syncBCB();
});

// Load Catalogs from server or fallback embedded
async function loadCatalogData() {
  if (window.SIGEP_EMBEDDED_DATA) {
    catalogData = window.SIGEP_EMBEDDED_DATA;
  }
  try {
    const res = await fetch("/api/catalogo");
    if (res.ok) {
      catalogData = await res.json();
    }
  } catch (e) {
    console.log("Usando datos locales embebidos");
  }
}

// Live BCB Indexation Fetcher
async function syncBCB() {
  const syncBtn = document.getElementById("btn-sync-bcb");
  if (syncBtn) syncBtn.textContent = "⏳...";

  try {
    const res = await fetch("/api/indicadores-bcb");
    if (res.ok) {
      const data = await res.json();
      currentVoucher.ufv = data.ufv || "3.36081";
      currentVoucher.tipo_cambio = data.tipo_cambio || "6.86";
      currentVoucher.dolar = data.tipo_cambio || "6.86";

      document.getElementById("input-ufv").value = currentVoucher.ufv;
      document.getElementById("input-dolar").value = currentVoucher.tipo_cambio;

      if (syncBtn) {
        syncBtn.textContent = "✓ BCB";
        syncBtn.title = `Actualizado: UFV = ${currentVoucher.ufv} | T/C = ${currentVoucher.tipo_cambio} (${data.fuente})`;
      }
    }
  } catch (err) {
    console.warn("No se pudo conectar con API BCB en línea, usando valores base:", err);
    if (syncBtn) syncBtn.textContent = "🔄 BCB";
  }
}

// Populate Selector of Momentos in top bar
function populateMomentosSelector() {
  const sel = document.getElementById("select-momento-strip");
  if (!sel) return;
  sel.innerHTML = "";
  catalogData.momentos.forEach(m => {
    const opt = document.createElement("option");
    opt.value = m.codigo;
    opt.textContent = `${m.codigo} - ${m.nombre}`;
    if (m.codigo === currentVoucher.momento_codigo) opt.selected = true;
    sel.appendChild(opt);
  });
  sel.addEventListener("change", (e) => {
    const found = catalogData.momentos.find(x => x.codigo === e.target.value);
    if (found) {
      currentVoucher.momento_codigo = found.codigo;
      currentVoucher.momento_desc = found.nombre;
    }
  });
}

function populatePlantillasSelector() {
  const sel = document.getElementById("select-plantillas-menu");
  if (!sel) return;
  sel.innerHTML = '<option value="">-- Cargar Ejercicio de Práctica --</option>';
  catalogData.plantillas.forEach(p => {
    const opt = document.createElement("option");
    opt.value = p.id;
    opt.textContent = p.titulo;
    sel.appendChild(opt);
  });
  sel.addEventListener("change", (e) => {
    if (e.target.value) {
      cargarPlantilla(e.target.value);
      e.target.value = "";
    }
  });
}

function cargarPlantilla(id) {
  const p = catalogData.plantillas.find(x => x.id === id);
  if (!p) return;
  currentVoucher = JSON.parse(JSON.stringify(p.comprobante));
  bindVoucherToForm();
  renderGrid();
  renderPhysicalVoucher();
}

function bindVoucherToForm() {
  document.getElementById("input-cbte-strip").value = currentVoucher.numero_cbte || "0000001";

  const inputUe = document.getElementById("input-ue");
  if (inputUe) inputUe.value = currentVoucher.unidad_ejecutora || "001";

  const inputUeDesc = document.getElementById("input-ue-desc");
  if (inputUeDesc) inputUeDesc.value = currentVoucher.unidad_ejecutora_desc || currentVoucher.direccion || "DIRECCION ADMINISTRATIVA Y FINANCIERA";

  const inputEntidad = document.getElementById("input-entidad");
  if (inputEntidad) inputEntidad.value = currentVoucher.entidad || "1814 - GM - GOBIERNO AUTÓNOMO MUNICIPAL DE SAN JOAQUÍN";

  const inputEnun = document.getElementById("input-enunciado");
  if (inputEnun) inputEnun.value = currentVoucher.enunciado || "";

  document.getElementById("input-depositante").value = currentVoucher.depositante || currentVoucher.beneficiario || "";
  document.getElementById("input-fecha").value = currentVoucher.fecha || getFormattedCurrentDate();
  document.getElementById("input-respaldo").value = currentVoucher.doc_respaldo || "";
  document.getElementById("input-dolar").value = currentVoucher.tipo_cambio || currentVoucher.dolar || "6.86";
  document.getElementById("input-ufv").value = currentVoucher.ufv || "3.36081";

  const glosaInput = document.getElementById("input-glosa");
  if (glosaInput) {
    glosaInput.value = currentVoucher.glosa || "";
  }

  const selM = document.getElementById("select-momento-strip");
  if (selM && currentVoucher.momento_codigo) {
    selM.value = currentVoucher.momento_codigo;
  }

  if (!currentVoucher.grid_rows || currentVoucher.grid_rows.length === 0) {
    initDefaultGrid();
  }
}

function handleGlosaVoucherInput(val) {
  currentVoucher.glosa = val;
  renderPhysicalVoucher();
}

function initDefaultGrid() {
  currentVoucher.grid_rows = [];
  for (let i = 0; i < 10; i++) {
    currentVoucher.grid_rows.push({
      rubro: "",
      cta: "",
      descripcion: "",
      presupuesto: "0.00",
      debe: "0.00",
      haber: "0.00"
    });
  }
  renderGrid();
}

// Render Entry Grid with requested exact columns
function renderGrid() {
  const tbody = document.getElementById("sigep-grid-tbody");
  if (!tbody) return;
  tbody.innerHTML = "";

  currentVoucher.grid_rows.forEach((row, idx) => {
    const tr = document.createElement("tr");
    if (idx === activeRowIndex) tr.className = "active-row";

    tr.onclick = () => selectRow(idx);

    tr.innerHTML = `
      <td style="width: 14%;">
        <div style="display:flex; align-items:center; position:relative;">
          <input type="text" class="grid-cell-input" value="${row.rubro || ''}" placeholder="Ej. 12200" 
            id="cell-rubro-${idx}"
            onfocus="selectRowAndCol(${idx}, 'rubro')" 
            oninput="handleRubroInput(${idx}, this.value)" 
            onblur="handleRubroBlur(${idx}, this)">
          <button type="button" class="btn-th-lookup" style="margin-left:2px; padding:0 3px; font-size:9px;" onclick="abrirModalRubros(${idx})" title="Desplegar Rubros y Partidas [F7]">🔍</button>
        </div>
      </td>
      <td style="width: 14%;">
        <div style="display:flex; align-items:center; position:relative;">
          <input type="text" class="grid-cell-input" value="${row.cta || ''}" placeholder="Ej. 11310" 
            id="cell-cta-${idx}"
            onfocus="selectRowAndCol(${idx}, 'cta')" 
            oninput="handleCtaInput(${idx}, this.value)" 
            onblur="handleCtaBlur(${idx}, this)">
          <button type="button" class="btn-th-lookup" style="margin-left:2px; padding:0 3px; font-size:9px;" onclick="abrirModalPlanCuentas(${idx})" title="Desplegar Plan de Cuentas [F6]">🔍</button>
        </div>
      </td>
      <td style="width: 36%;">
        <input type="text" class="grid-cell-input" value="${row.descripcion || ''}" placeholder="Nombre automático..." 
          id="cell-desc-${idx}"
          onfocus="selectRowAndCol(${idx}, 'descripcion')" 
          oninput="updateGridCell(${idx}, 'descripcion', this.value)">
      </td>
      <td style="width: 12%;">
        <input type="text" class="grid-cell-input numeric" value="${row.presupuesto || '0.00'}" 
          onfocus="selectRowAndCol(${idx}, 'presupuesto')" 
          oninput="updateGridCell(${idx}, 'presupuesto', this.value)">
      </td>
      <td style="width: 12%;">
        <input type="text" class="grid-cell-input numeric" value="${row.debe || '0.00'}" 
          onfocus="selectRowAndCol(${idx}, 'debe')" 
          oninput="updateGridCell(${idx}, 'debe', this.value)">
      </td>
      <td style="width: 12%;">
        <input type="text" class="grid-cell-input numeric" value="${row.haber || '0.00'}" 
          onfocus="selectRowAndCol(${idx}, 'haber')" 
          oninput="updateGridCell(${idx}, 'haber', this.value)">
      </td>
    `;
    tbody.appendChild(tr);
  });

  updateDetailInspector();
  calculateGridTotals();
}

// Automatic name insertion and dot formatting handlers
function handleRubroInput(idx, value) {
  currentVoucher.grid_rows[idx].rubro = value;
  const match = searchCatalogItem(value, "rubro");
  if (match) {
    currentVoucher.grid_rows[idx].descripcion = match.nombre;
    updateRowDescInput(idx, match.nombre);
  }
  updateDetailInspector();
  calculateGridTotals();
}

function handleRubroBlur(idx, inputEl) {
  const formatted = formatCodeWithDots(inputEl.value);
  inputEl.value = formatted;
  currentVoucher.grid_rows[idx].rubro = formatted;
  const match = searchCatalogItem(formatted, "rubro");
  if (match && !currentVoucher.grid_rows[idx].descripcion) {
    currentVoucher.grid_rows[idx].descripcion = match.nombre;
    updateRowDescInput(idx, match.nombre);
  }
  updateDetailInspector();
}

function handleCtaInput(idx, value) {
  currentVoucher.grid_rows[idx].cta = value;
  const match = searchCatalogItem(value, "cta");
  if (match) {
    currentVoucher.grid_rows[idx].descripcion = match.nombre;
    updateRowDescInput(idx, match.nombre);
  }
  updateDetailInspector();
  calculateGridTotals();
}

function handleCtaBlur(idx, inputEl) {
  const formatted = formatCodeWithDots(inputEl.value);
  inputEl.value = formatted;
  currentVoucher.grid_rows[idx].cta = formatted;
  const match = searchCatalogItem(formatted, "cta");
  if (match && !currentVoucher.grid_rows[idx].descripcion) {
    currentVoucher.grid_rows[idx].descripcion = match.nombre;
    updateRowDescInput(idx, match.nombre);
  }
  updateDetailInspector();
}

function updateRowDescInput(idx, text) {
  const tbody = document.getElementById("sigep-grid-tbody");
  if (tbody && tbody.children[idx]) {
    const descInput = tbody.children[idx].children[2].querySelector("input");
    if (descInput) descInput.value = text;
  }
}

function selectRow(idx) {
  activeRowIndex = idx;
  const tbody = document.getElementById("sigep-grid-tbody");
  if (tbody) {
    const rows = tbody.querySelectorAll("tr");
    rows.forEach((r, i) => {
      if (i === idx) r.classList.add("active-row");
      else r.classList.remove("active-row");
    });
  }
  updateDetailInspector();
}

function updateGridCell(rowIdx, col, value) {
  if (!currentVoucher.grid_rows[rowIdx]) return;
  currentVoucher.grid_rows[rowIdx][col] = value;
  updateDetailInspector();
  calculateGridTotals();
}

function updateDetailInspector() {
  const row = currentVoucher.grid_rows[activeRowIndex] || {};
  document.getElementById("lbl-linea-no").textContent = (activeRowIndex + 1);
  
  let rubroLabel = "-";
  if (row.rubro) {
    const match = searchCatalogItem(row.rubro, "rubro");
    rubroLabel = row.rubro + (match ? ` (${match.nombre})` : "");
  }
  document.getElementById("lbl-rubro").textContent = rubroLabel;

  let ctaLabel = "-";
  if (row.cta) {
    const match = searchCatalogItem(row.cta, "cta");
    ctaLabel = row.cta + (match ? ` (${match.nombre})` : "");
  }
  document.getElementById("lbl-cuenta").textContent = ctaLabel;

  const glosaBox = document.getElementById("txt-row-glosa");
  if (glosaBox) {
    glosaBox.value = row.descripcion || "";
  }
}

function handleGlosaInput(val) {
  if (currentVoucher.grid_rows[activeRowIndex]) {
    currentVoucher.grid_rows[activeRowIndex].descripcion = val;
    updateRowDescInput(activeRowIndex, val);
  }
}

function parseInputNumber(val) {
  if (val === null || val === undefined || val === "") return 0;
  if (typeof val === "number") return val;
  let str = val.toString().replace(/Bs\.?|\$|\s/gi, "").trim();
  if (!str) return 0;
  if (str.includes(",") && str.includes(".")) {
    if (str.lastIndexOf(",") > str.lastIndexOf(".")) {
      str = str.replace(/\./g, "").replace(",", ".");
    } else {
      str = str.replace(/,/g, "");
    }
  } else if (str.includes(",")) {
    const parts = str.split(",");
    if (parts.length === 2 && (parts[1].length === 1 || parts[1].length === 2)) {
      str = str.replace(",", ".");
    } else {
      str = str.replace(/,/g, "");
    }
  }
  const n = parseFloat(str);
  return isNaN(n) ? 0 : n;
}

function calculateGridTotals() {
  let totalPresup = 0;
  let totalDebe = 0;
  let totalHaber = 0;

  currentVoucher.grid_rows.forEach(r => {
    totalPresup += parseInputNumber(r.presupuesto);
    totalDebe += parseInputNumber(r.debe);
    totalHaber += parseInputNumber(r.haber);
  });

  const pBox = document.getElementById("total-presup-box");
  const dBox = document.getElementById("total-debe-box");
  const hBox = document.getElementById("total-haber-box");

  if (pBox) pBox.textContent = formatMoney(totalPresup);
  if (dBox) dBox.textContent = formatMoney(totalDebe);
  if (hBox) hBox.textContent = formatMoney(totalHaber);

  return { totalPresup, totalDebe, totalHaber };
}

// Global modal and focus state
let modalActiveType = null; // 'cuentas' | 'rubros' | null
let rubrosFilterType = 'all'; // 'all' | 'recursos' | 'gastos'
let modalFilteredItems = [];
let modalSelectedIndex = 0;
let activeCol = 'cta';

function selectRowAndCol(rowIdx, colName) {
  selectRow(rowIdx);
  activeCol = colName;
}

// Shortcuts Execution
function setupKeyboardShortcuts() {
  document.addEventListener("keydown", (e) => {
    // 1. Navigation when a catalog modal is open
    if (modalActiveType) {
      if (e.key === "Escape") {
        e.preventDefault();
        cerrarModales();
        return;
      }
      if (e.key === "ArrowDown") {
        e.preventDefault();
        if (modalSelectedIndex < modalFilteredItems.length - 1) {
          modalSelectedIndex++;
          if (modalActiveType === 'cuentas') renderModalCuentas();
          else renderModalRubros();
          scrollSelectedModalRowIntoView();
        }
        return;
      }
      if (e.key === "ArrowUp") {
        e.preventDefault();
        if (modalSelectedIndex > 0) {
          modalSelectedIndex--;
          if (modalActiveType === 'cuentas') renderModalCuentas();
          else renderModalRubros();
          scrollSelectedModalRowIntoView();
        }
        return;
      }
      if (e.key === "Enter") {
        e.preventDefault();
        if (modalFilteredItems.length > 0 && modalFilteredItems[modalSelectedIndex]) {
          const item = modalFilteredItems[modalSelectedIndex];
          if (modalActiveType === 'cuentas') {
            seleccionarCuenta(item.codigo, item.nombre);
          } else {
            seleccionarRubro(item.tipo, item.codigo, item.nombre);
          }
        }
        return;
      }
      return;
    }

    // 2. Global Shortcuts when in main window
    if (e.key === "F6") {
      e.preventDefault();
      abrirModalPlanCuentas();
    } else if (e.key === "F7") {
      e.preventDefault();
      abrirModalRubros();
    } else if (e.key === "F2" && e.shiftKey) {
      e.preventDefault();
      grabarYSiguiente();
    } else if (e.key === "Enter" && e.ctrlKey) {
      e.preventDefault();
      grabarYSiguiente();
    } else if (e.key === "F2") {
      e.preventDefault();
      grabarComprobante();
    } else if (e.key === "F4" && !e.ctrlKey) {
      e.preventDefault();
      eliminarFilaActiva();
    } else if (e.key === "F4" && e.ctrlKey) {
      e.preventDefault();
      limpiarFilaActiva();
    } else if (e.key === "n" && e.ctrlKey) {
      e.preventDefault();
      insertarLineas(1);
    } else if (e.key === "F3") {
      e.preventDefault();
      insertarLineas(3);
    } else if (e.key === "F8") {
      e.preventDefault();
      imprimirComprobante();
    }
  });
}

// ----------------------------------------------------
// MODAL PLAN DE CUENTAS (F6)
// ----------------------------------------------------
function abrirModalPlanCuentas(rowIdx) {
  if (rowIdx !== undefined) activeRowIndex = rowIdx;
  modalActiveType = 'cuentas';
  modalSelectedIndex = 0;

  const modal = document.getElementById("modal-plan-cuentas");
  if (modal) modal.style.display = "flex";

  const searchInput = document.getElementById("search-cta-modal");
  if (searchInput) {
    searchInput.value = "";
    setTimeout(() => searchInput.focus(), 50);
  }
  filtrarModalCuentas("");
}

function filtrarModalCuentas(query) {
  const q = (query || "").trim().toLowerCase().replace(/[^0-9a-záéíóúñ]/g, "");

  if (!catalogData.plan_cuentas) {
    modalFilteredItems = [];
  } else if (!q) {
    modalFilteredItems = catalogData.plan_cuentas.slice(0, 80);
  } else {
    modalFilteredItems = catalogData.plan_cuentas.filter(c => {
      const codeClean = (c.codigo || "").toLowerCase().replace(/[^0-9]/g, "");
      const nameClean = (c.nombre || "").toLowerCase();
      return codeClean.includes(q) || nameClean.includes(q);
    }).slice(0, 100);
  }

  modalSelectedIndex = 0;
  renderModalCuentas();
}

function renderModalCuentas() {
  const tbody = document.getElementById("tbody-modal-cuentas");
  const countLbl = document.getElementById("lbl-count-cuentas");
  if (!tbody) return;
  tbody.innerHTML = "";

  if (countLbl) {
    countLbl.textContent = `${modalFilteredItems.length} cuentas disponibles`;
  }

  if (modalFilteredItems.length === 0) {
    tbody.innerHTML = '<tr><td colspan="3" style="text-align:center; padding:15px; color:#777;">No se encontraron cuentas con ese criterio de búsqueda.</td></tr>';
    return;
  }

  modalFilteredItems.forEach((c, idx) => {
    const tr = document.createElement("tr");
    if (idx === modalSelectedIndex) tr.className = "selected";
    tr.onclick = () => seleccionarCuenta(c.codigo, c.nombre);
    tr.ondblclick = () => seleccionarCuenta(c.codigo, c.nombre);
    tr.innerHTML = `
      <td style="font-weight:bold; color:#0d47a1;">${formatCodeWithDots(c.codigo)}</td>
      <td>${c.nombre}</td>
      <td style="color:#666;">${c.nivel || 'Subcuenta'}</td>
    `;
    tbody.appendChild(tr);
  });
}

function seleccionarCuenta(codigo, nombre) {
  if (!currentVoucher.grid_rows[activeRowIndex]) {
    currentVoucher.grid_rows[activeRowIndex] = { rubro: "", cta: "", descripcion: "", presupuesto: "0.00", debe: "0.00", haber: "0.00" };
  }
  const formattedCode = formatCodeWithDots(codigo);
  currentVoucher.grid_rows[activeRowIndex].cta = formattedCode;
  currentVoucher.grid_rows[activeRowIndex].descripcion = nombre;

  cerrarModales();
  renderGrid();
  updateDetailInspector();

  // Focus the amount cell (debe or presupuesto)
  setTimeout(() => {
    const debeInput = document.querySelector(`#sigep-grid-tbody tr:nth-child(${activeRowIndex + 1}) td:nth-child(5) input`);
    if (debeInput) debeInput.focus();
  }, 50);
}

// ----------------------------------------------------
// MODAL CLASIFICADOR DE RUBROS Y PARTIDAS (F7)
// ----------------------------------------------------
function abrirModalRubros(rowIdx) {
  if (rowIdx !== undefined) activeRowIndex = rowIdx;
  modalActiveType = 'rubros';
  modalSelectedIndex = 0;

  const modal = document.getElementById("modal-clasificador-rubros");
  if (modal) modal.style.display = "flex";

  const searchInput = document.getElementById("search-rubro-modal");
  if (searchInput) {
    searchInput.value = "";
    setTimeout(() => searchInput.focus(), 50);
  }
  filtrarModalRubros("");
}

function setRubrosFilterType(type) {
  rubrosFilterType = type;
  document.querySelectorAll(".modal-tabs .modal-tab").forEach(tab => tab.classList.remove("active"));
  if (type === 'all') document.getElementById("tab-rubros-all")?.classList.add("active");
  if (type === 'recursos') document.getElementById("tab-rubros-rec")?.classList.add("active");
  if (type === 'gastos') document.getElementById("tab-rubros-gas")?.classList.add("active");

  const query = document.getElementById("search-rubro-modal")?.value || "";
  filtrarModalRubros(query);
}

function filtrarModalRubros(query) {
  const q = (query || "").trim().toLowerCase().replace(/[^0-9a-záéíóúñ]/g, "");
  let items = [];

  const rubros = (catalogData.rubros_recurso || []).map(r => ({ ...r, tipo: 'RUBRO (Recurso)' }));
  const partidas = (catalogData.partidas_gasto || []).map(p => ({ ...p, tipo: 'PARTIDA (Gasto)' }));

  if (rubrosFilterType === 'recursos') {
    items = rubros;
  } else if (rubrosFilterType === 'gastos') {
    items = partidas;
  } else {
    items = [...rubros, ...partidas];
  }

  if (!q) {
    modalFilteredItems = items.slice(0, 80);
  } else {
    modalFilteredItems = items.filter(it => {
      const codeClean = (it.codigo || "").toLowerCase().replace(/[^0-9]/g, "");
      const nameClean = (it.nombre || "").toLowerCase();
      return codeClean.includes(q) || nameClean.includes(q);
    }).slice(0, 100);
  }

  modalSelectedIndex = 0;
  renderModalRubros();
}

function renderModalRubros() {
  const tbody = document.getElementById("tbody-modal-rubros");
  const countLbl = document.getElementById("lbl-count-rubros");
  if (!tbody) return;
  tbody.innerHTML = "";

  if (countLbl) {
    countLbl.textContent = `${modalFilteredItems.length} items encontrados`;
  }

  if (modalFilteredItems.length === 0) {
    tbody.innerHTML = '<tr><td colspan="3" style="text-align:center; padding:15px; color:#777;">No se encontraron rubros o partidas con ese criterio.</td></tr>';
    return;
  }

  modalFilteredItems.forEach((it, idx) => {
    const tr = document.createElement("tr");
    if (idx === modalSelectedIndex) tr.className = "selected";
    tr.onclick = () => seleccionarRubro(it.tipo, it.codigo, it.nombre);
    tr.ondblclick = () => seleccionarRubro(it.tipo, it.codigo, it.nombre);

    const isGas = it.tipo.includes("Gasto");
    const badgeClass = isGas ? "badge-tipo-rubro badge-gas" : "badge-tipo-rubro badge-rec";

    tr.innerHTML = `
      <td><span class="${badgeClass}">${it.tipo}</span></td>
      <td style="font-weight:bold; color:#1b5e20;">${formatCodeWithDots(it.codigo)}</td>
      <td>${it.nombre}</td>
    `;
    tbody.appendChild(tr);
  });
}

function seleccionarRubro(tipo, codigo, nombre) {
  if (!currentVoucher.grid_rows[activeRowIndex]) {
    currentVoucher.grid_rows[activeRowIndex] = { rubro: "", cta: "", descripcion: "", presupuesto: "0.00", debe: "0.00", haber: "0.00" };
  }
  const formattedCode = formatCodeWithDots(codigo);
  currentVoucher.grid_rows[activeRowIndex].rubro = formattedCode;
  if (!currentVoucher.grid_rows[activeRowIndex].descripcion) {
    currentVoucher.grid_rows[activeRowIndex].descripcion = nombre;
  }

  cerrarModales();
  renderGrid();
  updateDetailInspector();

  // Focus the cta or presupuesto cell
  setTimeout(() => {
    const ctaInput = document.querySelector(`#sigep-grid-tbody tr:nth-child(${activeRowIndex + 1}) td:nth-child(2) input`);
    if (ctaInput) ctaInput.focus();
  }, 50);
}

function cerrarModales() {
  const m1 = document.getElementById("modal-plan-cuentas");
  const m2 = document.getElementById("modal-clasificador-rubros");
  const m3 = document.getElementById("modal-mayores");
  const m4 = document.getElementById("modal-eeff");
  const m5 = document.getElementById("modal-celular");
  if (m1) m1.style.display = "none";
  if (m2) m2.style.display = "none";
  if (m3) m3.style.display = "none";
  if (m4) m4.style.display = "none";
  if (m5) m5.style.display = "none";
  modalActiveType = null;
}

function abrirModalCelular() {
  const modal = document.getElementById("modal-celular");
  if (modal) modal.style.display = "flex";
}

function copiarAlPortapapeles(texto) {
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(texto).then(() => {
      showToast("📋 Enlace copiado al portapapeles");
    }).catch(() => {
      prompt("Copia este enlace:", texto);
    });
  } else {
    prompt("Copia este enlace:", texto);
  }
}

function handleModalBackdropClick(event, modalId) {
  if (event.target.id === modalId) {
    cerrarModales();
  }
}

function scrollSelectedModalRowIntoView() {
  const selectedRow = document.querySelector(".sigep-modal-table tr.selected");
  if (selectedRow) {
    selectedRow.scrollIntoView({ block: "nearest" });
  }
}

function eliminarFilaActiva() {
  if (currentVoucher.grid_rows.length > 1) {
    currentVoucher.grid_rows.splice(activeRowIndex, 1);
    if (activeRowIndex >= currentVoucher.grid_rows.length) {
      activeRowIndex = currentVoucher.grid_rows.length - 1;
    }
    renderGrid();
  } else {
    limpiarFilaActiva();
  }
}

function limpiarFilaActiva() {
  if (currentVoucher.grid_rows[activeRowIndex]) {
    currentVoucher.grid_rows[activeRowIndex] = {
      rubro: "", cta: "", descripcion: "", presupuesto: "0.00", debe: "0.00", haber: "0.00"
    };
    renderGrid();
  }
}

function insertarLineas(count = 1) {
  for (let i = 0; i < count; i++) {
    currentVoucher.grid_rows.push({
      rubro: "", cta: "", descripcion: "", presupuesto: "0.00", debe: "0.00", haber: "0.00"
    });
  }
  renderGrid();
}

function toggleVistaComprobante() {
  const win = document.getElementById("sigep-entry-window");
  const voucher = document.getElementById("sigep-physical-view");
  const btn = document.getElementById("btn-toggle-view");

  if (voucher.style.display === "block") {
    voucher.style.display = "none";
    win.style.display = "flex";
    btn.textContent = "👁️ Ver Cbte Oficial";
  } else {
    renderPhysicalVoucher();
    win.style.display = "none";
    voucher.style.display = "block";
    btn.textContent = "✏️ Volver a la Grilla";
  }
}

// ========================================================
// GENERATE PHYSICAL VOUCHER HTML FOR A GIVEN VOUCHER
// ========================================================
function generateVoucherSheetHtml(v) {
  let totalPresup = 0;
  let totalDebe = 0;
  let totalHaber = 0;

  (v.grid_rows || []).forEach(r => {
    totalPresup += parseFloat(r.presupuesto) || 0;
    totalDebe += parseFloat(r.debe) || 0;
    totalHaber += parseFloat(r.haber) || 0;
  });

  const displayTotal = totalDebe > 0 ? totalDebe : (totalPresup > 0 ? totalPresup : totalHaber);
  const sonLiteral = numeroALetras(displayTotal);

  const filledRows = (v.grid_rows || []).filter(r => 
    r.rubro || r.cta || r.descripcion || (parseFloat(r.presupuesto) > 0) || (parseFloat(r.debe) > 0) || (parseFloat(r.haber) > 0)
  );

  let tableRowsHtml = "";

  filledRows.forEach(r => {
    const rubroCode = r.rubro || "";
    const ctaCode = r.cta || "";
    const presupVal = (parseFloat(r.presupuesto) > 0) ? formatMoney(r.presupuesto) : "";
    const debeVal = (parseFloat(r.debe) > 0) ? formatMoney(r.debe) : "";
    const haberVal = (parseFloat(r.haber) > 0) ? formatMoney(r.haber) : "";

    tableRowsHtml += `
      <tr class="item-row">
        <td class="col-rubro">${rubroCode}</td>
        <td class="col-cta">${ctaCode}</td>
        <td class="col-desc" style="white-space: pre-line;">${r.descripcion || ''}</td>
        <td class="col-presup">${presupVal}</td>
        <td class="col-debe">${debeVal}</td>
        <td class="col-haber">${haberVal}</td>
      </tr>
    `;
  });

  const enunciadoText = (v.enunciado || "").trim();
  const hasEnunciado = enunciadoText.length > 0;

  // Calibración de filas: 5 filas si tiene enunciado (baja 7-8cm), o 9 filas si no tiene (empieza a 3cm)
  const targetRows = hasEnunciado ? 5 : 9;
  const minRows = Math.max(0, targetRows - filledRows.length);
  for (let i = 0; i < minRows; i++) {
    tableRowsHtml += `<tr class="item-row"><td>&nbsp;</td><td></td><td></td><td></td><td></td><td></td></tr>`;
  }

  const enunciadoBlock = hasEnunciado ? `
    <!-- Espacio superior de 7 a 8 cm para el Enunciado en letra grande legible 16pt -->
    <div class="sigep-enunciado-area">
      <div class="enunciado-title">ENUNCIADO / TRANSACCIÓN:</div>
      <div class="enunciado-text">${enunciadoText.replace(/\n/g, '<br/>')}</div>
    </div>
  ` : '';

  return `
    <div class="sigep-sheet ${hasEnunciado ? 'with-enunciado' : 'no-enunciado'}">
      ${enunciadoBlock}

      <!-- Top Header -->
      <div class="sigep-header">
        <div class="sigep-header-left">
          <div class="org-title">${v.entidad || '1814 - GM - GOBIERNO AUTÓNOMO MUNICIPAL DE SAN JOAQUÍN'}</div>
          <div class="org-sub">${v.unidad_ejecutora_desc || v.direccion || 'DIRECCION ADMINISTRATIVA Y FINANCIERA'}</div>
        </div>
        <div class="sigep-header-right">
          <div>Fecha : ${v.fecha || '10/09/2026'}</div>
          <div>Hora : ${v.hora || '10:30:00'}</div>
          <div>Página : 1</div>
        </div>
      </div>

      <!-- Title Box & Cbte No. (Aligned exactly as in Word) -->
      <div class="sigep-title-wrapper">
        <div class="title-dummy-left"></div>
        <div class="sigep-title-box">
          COMPROBANTE DE CONTABILIDAD
        </div>
        <div class="sigep-cbte-num-box">
          <div class="num-lbl">ValidadoCbte No.</div>
          <div class="num-val">${v.numero_cbte || '0000001'}</div>
        </div>
      </div>

      <!-- Metadata Grid -->
      <div class="sigep-meta-grid">
        <div class="sigep-meta-row">
          <div>
            <span class="lbl">Unidad Ejecutora : </span>
            <span class="val-italic">${v.unidad_ejecutora || '001'}&nbsp;&nbsp;&nbsp;&nbsp;${v.unidad_ejecutora_desc || v.direccion || 'DIRECCION ADMINISTRATIVA Y FINANCIERA'}</span>
          </div>
          <div>
            <span class="lbl">Fecha Cbte.&nbsp;&nbsp;</span>
            <span class="val-date">${v.fecha || '10/09/2026'}</span>
          </div>
        </div>
        <div class="sigep-meta-row">
          <div>
            <span class="lbl">Cod. Transac. : </span>
            <span class="val-italic">${v.momento_codigo || '12'}&nbsp;&nbsp;&nbsp;&nbsp;${v.momento_desc || 'Devengado de Recursos'}</span>
          </div>
        </div>
        <div class="sigep-meta-row">
          <div>
            <span class="lbl">Moneda : </span>
            <span class="val-italic">${v.moneda || 'BBS'} Bolivianos</span>
          </div>
        </div>
        <div class="sigep-meta-row">
          <div>
            <span class="lbl">T/C (BCB) : </span><span class="val-bold-italic">${v.tipo_cambio || '6.86'}</span>&nbsp;&nbsp;&nbsp;&nbsp;
            <span class="lbl">UFV (BCB) : </span><span class="val-bold-italic">${v.ufv || '3.36131'}</span>&nbsp;&nbsp;&nbsp;&nbsp;
            <span class="lbl">Documento Respaldo : </span><span class="val-italic">${v.doc_respaldo || ''}</span>
          </div>
        </div>
      </div>

      <!-- Main Table with requested exact columns -->
      <table class="sigep-table">
        <thead>
          <tr>
            <th style="width: 13.2%;">RUBRO</th>
            <th style="width: 13.9%;">CUENTA<br>CONTABLE</th>
            <th style="width: 36.8%;">DESCRIPCION DE LAS CUENTAS</th>
            <th style="width: 12.0%;">PRESUPUESTOS<br>(Bs.)</th>
            <th style="width: 12.0%;">DEBE<br>(Bs.)</th>
            <th style="width: 12.1%;">HABER<br>(Bs.)</th>
          </tr>
        </thead>
        <tbody>
          ${tableRowsHtml}
          <!-- Totales Row -->
          <tr class="totals-row">
            <td colspan="3" class="totals-label">TOTALES</td>
            <td class="col-presup" style="font-weight:bold; font-size:8.5pt;">${totalPresup > 0 ? formatMoney(totalPresup) : ''}</td>
            <td class="col-debe" style="font-weight:bold; font-size:8.5pt;">${totalDebe > 0 ? formatMoney(totalDebe) : ''}</td>
            <td class="col-haber" style="font-weight:bold; font-size:8.5pt;">${totalHaber > 0 ? formatMoney(totalHaber) : ''}</td>
          </tr>
        </tbody>
      </table>

      <!-- Literal Amount Row -->
      <div class="sigep-literal-row">
        ${sonLiteral}
      </div>

      <!-- Beneficiary and Glosa Box -->
      <div class="sigep-bottom-box">
        <div class="sigep-beneficiary-col">
          <div class="sigep-box-title"><u><b>Beneficiario / Depositante :</b></u></div>
          <div style="font-weight: normal; margin-top: 3px;">${v.depositante || v.beneficiario || ''}</div>
        </div>
        <div class="sigep-description-col">
          <div>
            <div class="sigep-box-title"><u>Descripción de la Transacción :</u></div>
            <div style="font-size: 7pt; text-align: justify; line-height: 1.25;">
              ${v.glosa || 'REGISTRO DE LA TRANSACCIÓN SEGÚN DOCUMENTACIÓN DE RESPALDO ADJUNTA.'}
            </div>
          </div>
          <div class="sigep-signer-name">
            ${(v.elaborado_por === 'Alejandro Cazas Tarqui' || !v.elaborado_por) ? 'C.T.' : v.elaborado_por}
          </div>
        </div>
      </div>

      <!-- Signatures Table -->
      <table class="sigep-signatures-table">
        <tbody>
          <tr>
            <td>
              <div class="sigepmv-label">SIGEP</div>
              ELABORADO POR
            </td>
            <td>REVISADO</td>
            <td>APROBADO</td>
            <td>APROBADO</td>
            <td>APROBADO</td>
          </tr>
        </tbody>
      </table>
    </div>
  `;
}

function renderPhysicalVoucher() {
  const container = document.getElementById("sigep-sheet-container");
  if (!container) return;

  syncInputsToVoucher();
  container.innerHTML = generateVoucherSheetHtml(currentVoucher);
}

function syncInputsToVoucher() {
  currentVoucher.numero_cbte = document.getElementById("input-cbte-strip").value || "0000001";

  const inputUe = document.getElementById("input-ue");
  if (inputUe) currentVoucher.unidad_ejecutora = inputUe.value.trim() || "001";

  const inputUeDesc = document.getElementById("input-ue-desc");
  if (inputUeDesc) {
    currentVoucher.unidad_ejecutora_desc = inputUeDesc.value.trim() || "DIRECCION ADMINISTRATIVA Y FINANCIERA";
    currentVoucher.direccion = currentVoucher.unidad_ejecutora_desc;
  }

  const inputEntidad = document.getElementById("input-entidad");
  if (inputEntidad) currentVoucher.entidad = inputEntidad.value.trim() || "1814 - GM - GOBIERNO AUTÓNOMO MUNICIPAL DE SAN JOAQUÍN";

  const inputEnun = document.getElementById("input-enunciado");
  if (inputEnun) currentVoucher.enunciado = inputEnun.value;

  currentVoucher.depositante = document.getElementById("input-depositante").value || "";
  currentVoucher.beneficiario = currentVoucher.depositante;
  currentVoucher.fecha = document.getElementById("input-fecha").value || "10/09/2026";
  currentVoucher.doc_respaldo = document.getElementById("input-respaldo").value || "";
  currentVoucher.dolar = document.getElementById("input-dolar").value || "6.86";
  currentVoucher.tipo_cambio = currentVoucher.dolar;
  currentVoucher.ufv = document.getElementById("input-ufv").value || "3.36081";
  const glosaInput = document.getElementById("input-glosa");
  if (glosaInput) currentVoucher.glosa = glosaInput.value;
}

function imprimirComprobante() {
  syncInputsToVoucher();
  renderPhysicalVoucher();

  document.body.classList.add("print-single-mode");
  document.body.classList.remove("print-batch-mode");

  const batchContainer = document.getElementById("sigep-batch-print-view");
  const singleContainer = document.getElementById("sigep-physical-view");
  const entryWindow = document.getElementById("sigep-entry-window");

  if (batchContainer) batchContainer.style.display = "none";
  if (singleContainer) {
    singleContainer.style.display = "block";
    singleContainer.style.background = "transparent";
    singleContainer.style.boxShadow = "none";
    singleContainer.style.padding = "0";
    singleContainer.style.margin = "0";
    singleContainer.style.borderRadius = "0";
  }
  if (entryWindow) entryWindow.style.display = "none";

  window.print();

  setTimeout(() => {
    document.body.classList.remove("print-single-mode");
    if (entryWindow) entryWindow.style.display = "flex";
    if (singleContainer) {
      singleContainer.style.background = "";
      singleContainer.style.boxShadow = "";
      singleContainer.style.padding = "";
      singleContainer.style.margin = "";
      singleContainer.style.borderRadius = "";
    }
  }, 1000);
}

// ========================================================
// BATCH PRINT: PRINT ALL ACCUMULATED (UP TO 50) IN ONE GO
// ========================================================
function imprimirTodasEnUna() {
  if (!savedVouchersList || savedVouchersList.length === 0) {
    alert("No hay comprobantes grabados en la base de datos aún. Graba al menos un comprobante antes de imprimir el lote.");
    return;
  }

  document.body.classList.add("print-batch-mode");
  document.body.classList.remove("print-single-mode");

  const batchContainer = document.getElementById("sigep-batch-print-view");
  const singleContainer = document.getElementById("sigep-physical-view");
  const entryWindow = document.getElementById("sigep-entry-window");

  // Ordenar siempre cronológicamente de menor a mayor por número de comprobante
  const sortedVouchers = [...savedVouchersList].sort((a, b) => {
    const na = parseInt((a.numero_cbte || "0").replace(/[^0-9]/g, "")) || 0;
    const nb = parseInt((b.numero_cbte || "0").replace(/[^0-9]/g, "")) || 0;
    return na - nb;
  });

  // Cada comprobante se genera dentro de su propio .sigep-sheet con salto de página estricto
  let allSheetsHtml = "";
  sortedVouchers.forEach(v => {
    const voucherData = (v.datos && Object.keys(v.datos).length > 0) ? v.datos : v;
    allSheetsHtml += generateVoucherSheetHtml(voucherData);
  });

  batchContainer.innerHTML = allSheetsHtml;
  batchContainer.style.display = "block";
  if (singleContainer) singleContainer.style.display = "none";
  if (entryWindow) entryWindow.style.display = "none";

  window.print();

  setTimeout(() => {
    document.body.classList.remove("print-batch-mode");
    if (batchContainer) batchContainer.style.display = "none";
    if (entryWindow) entryWindow.style.display = "flex";
  }, 1000);
}

// ========================================================
// EXPORT ALL VOUCHERS TO PDF (DIRECT DOWNLOAD & PRINT)
// ========================================================
function exportarComoPdf() {
  if (!savedVouchersList || savedVouchersList.length === 0) {
    alert("No hay comprobantes guardados para exportar. Graba al menos un comprobante antes de exportar a PDF.");
    return;
  }

  showToast(`📄 Generando y descargando archivo PDF con los ${savedVouchersList.length} comprobantes...`, 4000);

  // 1. Descarga automática del archivo PDF oficial generado por el sistema
  window.location.href = "/api/descargar-pdf-oficial";
}

// ========================================================
// SAVED VOUCHERS ACCUMULATOR & PERSISTENCE MANAGEMENT
// ========================================================
function showToast(msg, duration = 3500) {
  let toast = document.getElementById("sigep-toast-popup");
  if (!toast) {
    toast = document.createElement("div");
    toast.id = "sigep-toast-popup";
    toast.className = "sigep-toast";
    document.body.appendChild(toast);
  }
  toast.innerHTML = `<span>${msg}</span>`;
  toast.style.display = "flex";

  if (window._toastTimeout) clearTimeout(window._toastTimeout);
  window._toastTimeout = setTimeout(() => {
    if (toast) toast.style.display = "none";
  }, duration);
}

function updateEditModeIndicator() {
  const badge = document.getElementById("lbl-edit-mode");
  if (!badge) return;
  if (currentVoucher && currentVoucher.id) {
    badge.className = "mode-badge editing";
    badge.textContent = "✏️ EDITANDO (GUARDADO)";
    badge.title = `Editando comprobante guardado Nº ${currentVoucher.numero_cbte}. Al hacer clic en Grabar se actualizarán los cambios en la base de datos.`;
  } else {
    badge.className = "mode-badge new";
    badge.textContent = "🟢 NUEVO CBTE";
    badge.title = "Comprobante nuevo listo para llenar y guardar";
  }
}

function updateSessionResumeBanner() {
  const banner = document.getElementById("session-resume-banner");
  if (!banner) return;

  if (savedVouchersList && savedVouchersList.length > 0) {
    const nums = savedVouchersList.map(c => parseInt((c.numero_cbte || "0").replace(/[^0-9]/g, "")) || 0).filter(n => n > 0);
    const minNum = nums.length > 0 ? Math.min(...nums) : 1;
    const maxNum = nums.length > 0 ? Math.max(...nums) : 1;
    const nextNum = maxNum + 1;
    const nextNumStr = nextNum.toString().padStart(7, '0');
    const lastNumStr = maxNum.toString().padStart(7, '0');

    banner.style.display = "flex";
    banner.innerHTML = `
      <span>📂 <b>Base de datos activa:</b> Tienes ${savedVouchersList.length} comprobantes guardados (del Nº ${minNum.toString().padStart(7, '0')} al Nº ${lastNumStr}).</span>
      <div class="session-resume-actions">
        <button type="button" class="btn-resume-action sec" onclick="cargarUltimoComprobanteGuardado()">✏️ Cargar Último (Nº ${lastNumStr})</button>
        <button type="button" class="btn-resume-action" onclick="nuevoComprobante()">➕ Continuar en Blanco (Nº ${nextNumStr})</button>
      </div>
    `;
  } else {
    banner.style.display = "none";
  }
}

function cargarUltimoComprobanteGuardado() {
  if (!savedVouchersList || savedVouchersList.length === 0) return;
  cargarComprobanteDeLista(savedVouchersList.length - 1);
}

async function cargarListaComprobantes() {
  try {
    const res = await fetch("/api/comprobantes");
    if (res.ok) {
      savedVouchersList = await res.json();
    } else {
      savedVouchersList = JSON.parse(localStorage.getItem("sigep_cbtes_lote") || "[]");
    }
  } catch (e) {
    savedVouchersList = JSON.parse(localStorage.getItem("sigep_cbtes_lote") || "[]");
  }

  // Ordenar siempre cronológicamente por número de comprobante
  savedVouchersList.sort((a, b) => {
    const na = parseInt((a.numero_cbte || "0").replace(/[^0-9]/g, "")) || 0;
    const nb = parseInt((b.numero_cbte || "0").replace(/[^0-9]/g, "")) || 0;
    return na - nb;
  });

  try {
    localStorage.setItem("sigep_cbtes_lote", JSON.stringify(savedVouchersList));
  } catch (e) {}

  renderSidePanelList();
  updateSessionResumeBanner();
}

function renderSidePanelList() {
  const container = document.getElementById("saved-cbte-list");
  const countBadge = document.getElementById("lbl-cbte-count");
  if (!container) return;

  const count = savedVouchersList.length;
  if (countBadge) countBadge.textContent = `${count} guardados`;

  if (count === 0) {
    container.innerHTML = `
      <div style="text-align:center; padding:24px 8px; color:#64748b; font-size:12px;">
        <p>No hay comprobantes grabados en la base de datos.</p>
        <p style="margin-top:6px;">Llena la grilla y presiona <b>[💾 Grabar]</b> o <b>[Guardar y Siguiente]</b> para acumularlos aquí.</p>
      </div>
    `;
    return;
  }

  let html = "";
  savedVouchersList.forEach((c, idx) => {
    const isCurrent = (currentVoucher && currentVoucher.id && currentVoucher.id === c.id) || 
                      (currentVoucher && currentVoucher.numero_cbte === c.numero_cbte);
    const monto = formatMoney(c.monto_total || 0);
    const glosaCorta = (c.datos && c.datos.glosa) ? c.datos.glosa.substring(0, 50) + "..." : "";

    html += `
      <div class="saved-cbte-card ${isCurrent ? 'active' : ''}" onclick="cargarComprobanteDeLista(${idx})">
        <div class="card-top">
          <span class="card-num">Cbte: ${c.numero_cbte}</span>
          <span class="card-momento">${c.momento_codigo || ''}</span>
        </div>
        <div class="card-detail">
          <div><b>Fecha:</b> ${c.fecha || ''}</div>
          <div style="overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">
            <b>Dep:</b> ${c.beneficiario || 'Varios'}
          </div>
          ${glosaCorta ? `<div style="font-size:9.5px; color:#555; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; margin-top:2px;">${glosaCorta}</div>` : ''}
        </div>
        <div class="card-bottom">
          <span class="card-total">Bs. ${monto}</span>
          <div class="card-actions">
            <button class="btn-card-action" style="font-weight:bold; background:#e0f2fe; color:#0369a1;" onclick="event.stopPropagation(); cargarComprobanteDeLista(${idx})">✏️ Editar</button>
            <button class="btn-card-action" style="color:#d32f2f;" onclick="event.stopPropagation(); eliminarComprobanteDeLista(${idx})" title="Eliminar este comprobante">🗑️</button>
          </div>
        </div>
      </div>
    `;
  });

  container.innerHTML = html;
}

function cargarComprobanteDeLista(idx) {
  const item = savedVouchersList[idx];
  if (!item) return;

  currentVoucher = (item.datos && Object.keys(item.datos).length > 0) ? JSON.parse(JSON.stringify(item.datos)) : JSON.parse(JSON.stringify(item));
  if (item.id) currentVoucher.id = item.id;
  if (item.numero_cbte) currentVoucher.numero_cbte = item.numero_cbte;

  bindVoucherToForm();
  renderGrid();
  renderPhysicalVoucher();
  renderSidePanelList();
  updateEditModeIndicator();
  showToast(`✏️ Comprobante Nº ${currentVoucher.numero_cbte} cargado para revisión y edición`);
}

async function eliminarComprobanteDeLista(idx) {
  const item = savedVouchersList[idx];
  if (!item) return;

  if (confirm(`¿Está seguro de eliminar el Comprobante Nº ${item.numero_cbte}?`)) {
    if (item.id) {
      try {
        await fetch(`/api/comprobantes/${item.id}`, { method: "DELETE" });
      } catch (e) {}
    }
    savedVouchersList.splice(idx, 1);
    localStorage.setItem("sigep_cbtes_lote", JSON.stringify(savedVouchersList));
    renderSidePanelList();
    updateSessionResumeBanner();
    
    // Invalidar caché de Mayores y EEFF para que recalculen automáticamente con los comprobantes restantes
    eeffAllData = null;
    mayoresData = null;
    
    // Si el comprobante eliminado es el que está en pantalla, preparar uno nuevo
    if (currentVoucher && currentVoucher.id === item.id) {
      nuevoComprobante();
    }
    showToast(`🗑️ Comprobante Nº ${item.numero_cbte} eliminado.`);
  }
}

function vaciarTodosLosComprobantes() {
  if (confirm("¿Está seguro de vaciar todos los comprobantes de la base de datos? Esta acción no se puede deshacer.")) {
    savedVouchersList.forEach(async (c) => {
      if (c.id) {
        try { await fetch(`/api/comprobantes/${c.id}`, { method: "DELETE" }); } catch(e){}
      }
    });
    savedVouchersList = [];
    localStorage.removeItem("sigep_cbtes_lote");
    nuevoComprobante();
    renderSidePanelList();
    updateSessionResumeBanner();
    showToast("Base de datos de comprobantes vaciada.");
  }
}

function nuevoComprobante() {
  // Determinar siguiente correlativo
  let nextNum = 1;
  if (savedVouchersList && savedVouchersList.length > 0) {
    const nums = savedVouchersList.map(c => parseInt((c.numero_cbte || "0").replace(/[^0-9]/g, "")) || 0).filter(n => n > 0);
    if (nums.length > 0) {
      nextNum = Math.max(...nums) + 1;
    }
  }
  const nextNumStr = nextNum.toString().padStart(7, '0');

  currentVoucher = {
    id: null,
    entidad: "1814 - GM - GOBIERNO AUTÓNOMO MUNICIPAL DE SAN JOAQUÍN",
    direccion: "DIRECCION ADMINISTRATIVA Y FINANCIERA",
    unidad_ejecutora: "001",
    unidad_ejecutora_desc: "DIRECCION ADMINISTRATIVA Y FINANCIERA",
    numero_cbte: nextNumStr,
    moneda: "BBS",
    momento_codigo: (currentVoucher && currentVoucher.momento_codigo) ? currentVoucher.momento_codigo : "12",
    momento_desc: (currentVoucher && currentVoucher.momento_desc) ? currentVoucher.momento_desc : "Devengado de Recursos",
    depositante: "",
    beneficiario: "",
    fecha: (currentVoucher && currentVoucher.fecha) ? currentVoucher.fecha : getFormattedCurrentDate(),
    hora: new Date().toLocaleTimeString('es-ES'),
    doc_respaldo: "",
    dolar: (currentVoucher && currentVoucher.dolar) ? currentVoucher.dolar : "6.86",
    tipo_cambio: (currentVoucher && currentVoucher.tipo_cambio) ? currentVoucher.tipo_cambio : "6.86",
    ufv: (currentVoucher && currentVoucher.ufv) ? currentVoucher.ufv : "3.36081",
    elaborado_por: "C.T.",
    glosa: "",
    grid_rows: []
  };

  bindVoucherToForm();
  initDefaultGrid();
  renderPhysicalVoucher();
  renderSidePanelList();
  updateEditModeIndicator();
  updateSessionResumeBanner();
}

async function grabarComprobante(isSilent = false) {
  syncInputsToVoucher();
  const { totalPresup, totalDebe, totalHaber } = calculateGridTotals();
  const displayTotal = totalDebe > 0 ? totalDebe : (totalPresup > 0 ? totalPresup : totalHaber);

  const payload = {
    id: currentVoucher.id || null,
    numero_cbte: currentVoucher.numero_cbte,
    fecha: currentVoucher.fecha,
    entidad: currentVoucher.entidad,
    momento_codigo: currentVoucher.momento_codigo,
    momento_desc: currentVoucher.momento_desc,
    beneficiario: currentVoucher.depositante || "DISTINTOS BENEFICIARIOS",
    monto_total: displayTotal,
    datos: JSON.parse(JSON.stringify(currentVoucher))
  };

  // 1. Guardar en base de datos SQLite a través de la API
  try {
    const res = await fetch("/api/comprobantes", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    if (res.ok) {
      const data = await res.json();
      currentVoucher.id = data.id;
      payload.id = data.id;
      payload.datos.id = data.id;
    }
  } catch (err) {
    console.warn("Servidor desconectado o error de red, guardando en almacenamiento local:", err);
  }

  // 2. Agregar o Actualizar en la lista de comprobantes
  const existingIdx = savedVouchersList.findIndex(c => (payload.id && c.id === payload.id) || (c.numero_cbte === payload.numero_cbte));
  if (existingIdx !== -1) {
    savedVouchersList[existingIdx] = payload;
  } else {
    savedVouchersList.push(payload);
  }

  // Ordenar cronológicamente
  savedVouchersList.sort((a, b) => {
    const na = parseInt((a.numero_cbte || "0").replace(/[^0-9]/g, "")) || 0;
    const nb = parseInt((b.numero_cbte || "0").replace(/[^0-9]/g, "")) || 0;
    return na - nb;
  });

  localStorage.setItem("sigep_cbtes_lote", JSON.stringify(savedVouchersList));
  renderSidePanelList();
  updateEditModeIndicator();
  updateSessionResumeBanner();

  // Invalidar caché de Mayores y EEFF para que siempre se actualicen con el nuevo comprobante
  eeffAllData = null;
  mayoresData = null;

  if (!isSilent) {
    showToast(`✅ Comprobante Nº ${currentVoucher.numero_cbte} guardado con éxito en la base de datos (${savedVouchersList.length} en total).`);
  }
  return true;
}

async function grabarYSiguiente() {
  const ok = await grabarComprobante(true);
  if (ok) {
    nuevoComprobante();
    showToast(`💾 Comprobante guardado con éxito. ¡Listo para llenar el siguiente!`, 3500);
  }
}

// ========================================================
// 5. MOTOR CLIENTE: LIBRO MAYOR (MAYORES DE TODAS LAS CUENTAS)
// ========================================================
let mayoresData = null;
let currentMayoresFilter = "all";
let currentMayoresSearch = "";

async function abrirModalMayores() {
  const modal = document.getElementById("modal-mayores");
  if (!modal) return;
  modal.style.display = "flex";
  
  const container = document.getElementById("mayores-list-container");
  if (container) {
    container.innerHTML = `<div style="text-align:center; padding:40px; color:#64748b; font-size:13px;">⏳ Procesando los 36 comprobantes y calculando libros mayores...</div>`;
  }

  try {
    const res = await fetch("/api/mayores");
    if (res.ok) {
      mayoresData = await res.json();
      poblarSelectCuentasMayor();
      actualizarResumenPillsMayores();
      renderMayoresList();
    } else {
      throw new Error("No se pudo cargar la información de mayores.");
    }
  } catch (err) {
    console.error("Error cargando mayores:", err);
    if (container) {
      container.innerHTML = `<div style="color:#ef4444; padding:20px; text-align:center;">Error al cargar libro mayor: ${err.message}</div>`;
    }
  }
}

function poblarSelectCuentasMayor() {
  const select = document.getElementById("select-cuenta-mayor");
  if (!select || !mayoresData || !mayoresData.cuentas) return;

  let html = `<option value="all">Todas las Cuentas (${mayoresData.cuentas.length} cuentas registradas)</option>`;
  mayoresData.cuentas.forEach(c => {
    html += `<option value="${c.codigo_formato}">${c.codigo_formato} - ${c.descripcion}</option>`;
  });
  select.innerHTML = html;
  select.value = currentMayoresFilter;
}

function actualizarResumenPillsMayores() {
  const pillsEl = document.getElementById("mayores-summary-pills");
  if (!pillsEl || !mayoresData || !mayoresData.resumen) return;

  const r = mayoresData.resumen;
  pillsEl.innerHTML = `
    <span style="background:#e0e7ff; color:#3730a3; padding:3px 8px; border-radius:4px; font-size:11px; font-weight:bold;">Cuentas: ${r.total_cuentas}</span>
    <span style="background:#dcfce7; color:#166534; padding:3px 8px; border-radius:4px; font-size:11px; font-weight:bold;">Total Debe: Bs. ${r.total_debe_fmt}</span>
    <span style="background:#dcfce7; color:#166534; padding:3px 8px; border-radius:4px; font-size:11px; font-weight:bold;">Total Haber: Bs. ${r.total_haber_fmt}</span>
    <span style="background:${r.cuadrado ? '#dcfce7' : '#fee2e2'}; color:${r.cuadrado ? '#166534' : '#991b1b'}; padding:3px 8px; border-radius:4px; font-size:11px; font-weight:bold;">
      ${r.cuadrado ? '✓ Balance Cuadrado' : '⚠️ Dif: ' + r.diferencia_fmt}
    </span>
  `;
}

function filtrarVistaMayores(codigo) {
  currentMayoresFilter = codigo;
  renderMayoresList();
}

function filtrarMayoresTexto(texto) {
  currentMayoresSearch = (texto || "").toLowerCase().trim();
  renderMayoresList();
}

function renderMayoresList() {
  const container = document.getElementById("mayores-list-container");
  if (!container || !mayoresData || !mayoresData.cuentas) return;

  let cuentasMostrar = mayoresData.cuentas;

  if (currentMayoresFilter !== "all") {
    cuentasMostrar = cuentasMostrar.filter(c => c.codigo_formato === currentMayoresFilter || c.codigo === currentMayoresFilter);
  }

  if (currentMayoresSearch) {
    cuentasMostrar = cuentasMostrar.filter(c => {
      const matchHeader = c.codigo.toLowerCase().includes(currentMayoresSearch) ||
                          c.codigo_formato.toLowerCase().includes(currentMayoresSearch) ||
                          c.descripcion.toLowerCase().includes(currentMayoresSearch);
      const matchMov = (c.movimientos || []).some(m => 
        (m.cbte && m.cbte.toLowerCase().includes(currentMayoresSearch)) ||
        (m.glosa && m.glosa.toLowerCase().includes(currentMayoresSearch)) ||
        (m.fecha && m.fecha.includes(currentMayoresSearch))
      );
      return matchHeader || matchMov;
    });
  }

  if (cuentasMostrar.length === 0) {
    container.innerHTML = `
      <div style="text-align:center; padding:40px; color:#64748b; font-size:13px;">
        No se encontraron cuentas o movimientos que coincidan con la búsqueda.
      </div>
    `;
    return;
  }

  let html = "";
  cuentasMostrar.forEach(acc => {
    const isDeudor = acc.tipo_saldo === "Deudor";
    html += `
      <div class="mayor-card">
        <div class="mayor-card-header">
          <div class="mayor-card-title">
            <span style="color:#2563eb; font-weight:800; font-family:'Courier New', monospace; font-size:13px;">${acc.codigo_formato}</span>
            <span style="margin: 0 6px; color:#94a3b8;">&mdash;</span>
            <span>${acc.descripcion}</span>
          </div>
          <div class="mayor-card-badges">
            <span style="font-size:11px; color:#475569;">${acc.movimientos.length} mov.</span>
            <span class="badge-saldo ${isDeudor ? 'deudor' : 'acreedor'}">
              Saldo: Bs. ${acc.saldo_fmt} (${acc.tipo_saldo})
            </span>
          </div>
        </div>

        <table class="mayor-table">
          <thead>
            <tr>
              <th style="width: 12%;">Fecha</th>
              <th style="width: 14%;">Cbte Nº</th>
              <th style="width: 44%;">Descripción / Glosa de la Transacción</th>
              <th style="width: 15%; text-align:right;">Debe (Bs.)</th>
              <th style="width: 15%; text-align:right;">Haber (Bs.)</th>
            </tr>
          </thead>
          <tbody>
    `;

    (acc.movimientos || []).forEach(m => {
      html += `
        <tr>
          <td>${m.fecha || '-'}</td>
          <td><span style="font-weight:bold; color:#1e293b; font-family:'Courier New';">${m.cbte}</span></td>
          <td style="font-size:10.5px; line-height:1.25;">${m.glosa || 'Movimiento contable según comprobante'}</td>
          <td class="num-col" style="color: ${m.debe > 0 ? '#111827' : '#94a3b8'};">${m.debe_fmt || '-'}</td>
          <td class="num-col" style="color: ${m.haber > 0 ? '#111827' : '#94a3b8'};">${m.haber_fmt || '-'}</td>
        </tr>
      `;
    });

    html += `
          </tbody>
          <tfoot>
            <tr class="tot-row">
              <td colspan="3" style="text-align:right; text-transform:uppercase; font-size:11px;">TOTALES CUENTA ${acc.codigo_formato}:</td>
              <td class="num-col">Bs. ${acc.total_debe_fmt}</td>
              <td class="num-col">Bs. ${acc.total_haber_fmt}</td>
            </tr>
            <tr style="background:#f8fafc; font-weight:bold; font-size:11px;">
              <td colspan="3" style="text-align:right;">SALDO FINAL (${acc.tipo_saldo.toUpperCase()}):</td>
              <td colspan="2" class="num-col" style="color:${isDeudor ? '#1e40af' : '#991b1b'}; font-size:12px;">
                Bs. ${acc.saldo_fmt}
              </td>
            </tr>
          </tfoot>
        </table>
      </div>
    `;
  });

  container.innerHTML = html;
}

function imprimirMayores() {
  const container = document.getElementById("mayores-list-container");
  if (!container) return;

  const printWin = window.open("", "_blank");
  printWin.document.write(`
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <title>LIBRO MAYOR GENERAL - SIGEP</title>
      <style>
        body { font-family: Arial, sans-serif; font-size: 8pt; color: #000; margin: 15mm; }
        .header-print { text-align: center; margin-bottom: 15px; border-bottom: 2px solid #000; padding-bottom: 8px; }
        .header-print h2 { margin: 0; font-size: 13pt; text-transform: uppercase; }
        .header-print p { margin: 3px 0; font-size: 8pt; color: #444; }
        .mayor-card { margin-bottom: 18px; border: 1px solid #000; page-break-inside: avoid; }
        .mayor-card-header { background: #f2f2f2; padding: 4px 8px; font-weight: bold; border-bottom: 1px solid #000; display: flex; justify-content: space-between; }
        table { width: 100%; border-collapse: collapse; font-size: 7.5pt; }
        th, td { border: 1px solid #ccc; padding: 3px 5px; }
        th { background: #fafafa; border-bottom: 1px solid #000; text-align: center; }
        .num-col { text-align: right; font-family: 'Courier New', monospace; font-weight: bold; }
        .tot-row td { background: #f2f2f2; font-weight: bold; border-top: 1px solid #000; border-bottom: 1px solid #000; }
        @page { size: letter portrait; margin: 12mm; }
      </style>
    </head>
    <body>
      <div class="header-print">
        <h2>GOBIERNO AUTÓNOMO MUNICIPAL DE SAN JOAQUÍN</h2>
        <p><b>SISTEMA DE CONTABILIDAD INTEGRADA (SIGEP) &mdash; LIBRO MAYOR GENERAL</b></p>
        <p>Expresado en Bolivianos &bull; Periodo Fiscal 2026</p>
      </div>
      ${container.innerHTML}
      <script>
        window.onload = function() { window.print(); }
      </script>
    </body>
    </html>
  `);
  printWin.document.close();
}


// ========================================================
// 6. MOTOR CLIENTE: LOS 8 EEFF (ESTADOS FINANCIEROS EDITABLES)
// ========================================================
let eeffAllData = null;
let currentEEFFReportId = "balance_general";
let eeffModifiedReports = {};

async function abrirModalEEFF() {
  const modal = document.getElementById("modal-eeff");
  if (!modal) return;
  modal.style.display = "flex";

  const content = document.getElementById("eeff-report-content");
  if (content) {
    content.innerHTML = `<div style="text-align:center; padding:60px; color:#475569; font-size:14px;">⏳ Calculando y estructurando los 8 Estados Financieros oficiales...</div>`;
  }

  try {
    const res = await fetch("/api/eeff");
    if (res.ok) {
      eeffAllData = await res.json();
      seleccionarReporteEEFF(currentEEFFReportId);
    } else {
      throw new Error("No se pudo obtener la información de Estados Financieros.");
    }
  } catch (err) {
    console.error("Error al abrir EEFF:", err);
    if (content) {
      content.innerHTML = `<div style="color:#ef4444; padding:30px; text-align:center;">Error al cargar Estados Financieros: ${err.message}</div>`;
    }
  }
}

function seleccionarReporteEEFF(reportId) {
  currentEEFFReportId = reportId;

  // Actualizar botones de pestañas
  const tabBtns = document.querySelectorAll(".eeff-tab-btn");
  tabBtns.forEach(b => {
    if (b.getAttribute("data-report") === reportId) {
      b.classList.add("active");
    } else {
      b.classList.remove("active");
    }
  });

  actualizarEstadoBadgeEEFF();
  renderActiveEEFFReport();
}

function actualizarEstadoBadgeEEFF() {
  const badge = document.getElementById("lbl-eeff-status");
  if (!badge) return;
  const isEdited = !!eeffModifiedReports[currentEEFFReportId];
  if (isEdited) {
    badge.className = "eeff-badge-status edited";
    badge.textContent = "✏️ Cambios Personalizados (Sin Guardar)";
  } else {
    badge.className = "eeff-badge-status";
    badge.textContent = "⚡ Calculado desde 36 Comprobantes";
  }
}

function renderActiveEEFFReport() {
  const content = document.getElementById("eeff-report-content");
  if (!content || !eeffAllData) return;

  const report = eeffAllData[currentEEFFReportId];
  if (!report) {
    content.innerHTML = `<div style="padding:40px; text-align:center;">Estado Financiero no disponible.</div>`;
    return;
  }

  let html = `
    <!-- Header Institucional -->
    <div class="eeff-header-block">
      <div class="top-row">
        <div class="left">${report.entidad || '1814 - GM - GOBIERNO AUTÓNOMO MUNICIPAL DE SAN JOAQUÍN'}</div>
        <div class="right">Fecha : 21/10/2026<br/>Hora : 22:30:00<br/>Página : 1 de 1</div>
      </div>
      <div style="font-size:7.5pt; color:#333; margin-top:2px;">
        <span>${report.periodo || 'Del 01/01/2026 Al 31/12/2026'}</span> &bull; 
        <span>${report.expresado || 'Expresado en Bolivianos'}</span><br/>
        <span>UNIDAD : ${report.unidad || '001 - DIRECCION ADMINISTRATIVA Y FINANCIERA'}</span> &bull; 
        <span>NIVEL : ${report.nivel || 'SUB CUENTA'}</span>
      </div>
    </div>

    <!-- Título Principal Sombreado -->
    <div class="eeff-title-banner">
      ${report.titulo}
    </div>
  `;

  // Renderizar tabla editable según tipo de reporte
  if (currentEEFFReportId === "balance_general") {
    html += renderTablaBalanceGeneral(report);
  } else if (currentEEFFReportId === "recursos_gastos_corrientes") {
    html += renderTablaRecursosGastos(report);
  } else if (currentEEFFReportId === "flujo_efectivo" || currentEEFFReportId === "cuenta_ahorro_inversion_financiamiento") {
    html += renderTablaFlujoOcaif(report);
  } else if (currentEEFFReportId === "cambios_patrimonio_neto") {
    html += renderTablaCambiosPatrimonio(report);
  } else if (currentEEFFReportId === "ejecucion_presupuesto_recursos") {
    html += renderTablaEjecucionRecursos(report);
  } else if (currentEEFFReportId === "ejecucion_presupuesto_gastos") {
    html += renderTablaEjecucionGastos(report);
  } else if (currentEEFFReportId === "estado_cuentas_complementaria") {
    html += renderTablaEstadoCuentas(report);
  }

  // Cuadro de Firmas Oficiales
  html += `
    <div class="eeff-signatures">
      <div class="eeff-sig-box">
        <div class="eeff-sig-line"></div>
        <b>ELABORADO POR</b><br/>ALEJANDRO CAZAS TARQUI
      </div>
      <div class="eeff-sig-box">
        <div class="eeff-sig-line"></div>
        <b>REVISADO POR</b><br/>CONTABILIDAD
      </div>
      <div class="eeff-sig-box">
        <div class="eeff-sig-line"></div>
        <b>APROBADO POR</b><br/>DIR. ADM. Y FINANCIERA
      </div>
    </div>
  `;

  content.innerHTML = html;
}

// ----------------------------------------------------
// TABLAS ESPECÍFICAS DE CADA REPORTE CON CELDAS EDITABLES
// ----------------------------------------------------
function renderTablaBalanceGeneral(rep) {
  let rowsHtml = "";
  (rep.filas || []).forEach((f, idx) => {
    const cls = f.tipo ? `row-${f.tipo}` : '';
    rowsHtml += `
      <tr class="${cls}">
        <td style="width:10%; font-family:monospace; font-weight:bold;">${f.cuenta}</td>
        <td style="width:38%;">${f.descripcion}</td>
        <td style="width:13%; text-align:right;" contenteditable="true" class="eeff-cell-editable" onblur="handleCellEdit(this, ${idx}, 'ej_anterior')">${f.ej_anterior}</td>
        <td style="width:13%; text-align:right;" contenteditable="true" class="eeff-cell-editable" onblur="handleCellEdit(this, ${idx}, 'parcial1')">${f.parcial1}</td>
        <td style="width:13%; text-align:right;" contenteditable="true" class="eeff-cell-editable" onblur="handleCellEdit(this, ${idx}, 'parcial2')">${f.parcial2}</td>
        <td style="width:13%; text-align:right; font-weight:bold;" contenteditable="true" class="eeff-cell-editable" onblur="handleCellEdit(this, ${idx}, 'total')">${f.total}</td>
      </tr>
    `;
  });

  const tot = rep.totales || {};
  return `
    <table class="eeff-table">
      <thead>
        <tr>
          <th>Cuenta</th>
          <th>Descripción</th>
          <th>Ejerc. Anterior</th>
          <th>Parciales</th>
          <th>Parciales</th>
          <th>Totales</th>
        </tr>
      </thead>
      <tbody>
        ${rowsHtml}
        <tr style="background:#e2e8f0; font-weight:bold; font-size:8pt; border-top:2px solid #000;">
          <td colspan="5" style="text-align:right;">TOTAL PASIVO Y PATRIMONIO :</td>
          <td style="text-align:right; font-family:'Courier New';">${tot.total_pasivo_patrimonio_fmt || '0.00'}</td>
        </tr>
      </tbody>
    </table>
    <div style="font-size:7pt; color:#475569; margin: 4px 0 12px 0;">
      <b>OBSERVACIONES:</b> ${rep.observaciones || 'Balance General procesado conforme a las transacciones registradas en el SIGEP.'}
    </div>
  `;
}

function renderTablaRecursosGastos(rep) {
  let rowsHtml = "";
  (rep.filas || []).forEach((f, idx) => {
    const cls = f.tipo ? `row-${f.tipo}` : '';
    rowsHtml += `
      <tr class="${cls}">
        <td style="width:12%; font-family:monospace; font-weight:bold;">${f.cuenta}</td>
        <td style="width:43%;">${f.descripcion}</td>
        <td style="width:15%; text-align:right;" contenteditable="true" class="eeff-cell-editable" onblur="handleCellEdit(this, ${idx}, 'parcial1')">${f.parcial1}</td>
        <td style="width:15%; text-align:right;" contenteditable="true" class="eeff-cell-editable" onblur="handleCellEdit(this, ${idx}, 'parcial2')">${f.parcial2}</td>
        <td style="width:15%; text-align:right; font-weight:bold;" contenteditable="true" class="eeff-cell-editable" onblur="handleCellEdit(this, ${idx}, 'total')">${f.total}</td>
      </tr>
    `;
  });

  const tot = rep.totales || {};
  return `
    <table class="eeff-table">
      <thead>
        <tr>
          <th>Cuenta</th>
          <th>Descripción</th>
          <th>Parciales</th>
          <th>Parciales</th>
          <th>Totales</th>
        </tr>
      </thead>
      <tbody>
        ${rowsHtml}
        <tr style="background:#e2e8f0; font-weight:bold; font-size:8pt; border-top:2px solid #000;">
          <td colspan="4" style="text-align:right;">${tot.tipo_resultado || 'GANANCIA (PERDIDA) DE LA GESTION :'}</td>
          <td style="text-align:right; font-family:'Courier New';">${tot.resultado_ejercicio_fmt || '0.00'}</td>
        </tr>
      </tbody>
    </table>
  `;
}

function renderTablaFlujoOcaif(rep) {
  let rowsHtml = "";
  (rep.filas || []).forEach((f, idx) => {
    const isMain = f.codigo.endsWith("000000000000") || f.codigo.endsWith("000000") || ["C", "F", "G", "H"].includes(f.codigo);
    rowsHtml += `
      <tr style="${isMain ? 'font-weight:bold; background:#f8fafc;' : ''}">
        <td style="width:20%; font-family:monospace; font-size:7pt;">${f.codigo}</td>
        <td style="width:60%; ${isMain ? 'font-weight:bold;' : ''}">${f.descripcion}</td>
        <td style="width:20%; text-align:right; font-family:'Courier New'; font-weight:bold;" contenteditable="true" class="eeff-cell-editable" onblur="handleCellEdit(this, ${idx}, 'monto')">${f.monto}</td>
      </tr>
    `;
  });

  return `
    <table class="eeff-table">
      <thead>
        <tr>
          <th>Código</th>
          <th>Descripción</th>
          <th>Monto (Bs.)</th>
        </tr>
      </thead>
      <tbody>
        ${rowsHtml}
      </tbody>
    </table>
  `;
}

function renderTablaCambiosPatrimonio(rep) {
  let rowsHtml = "";
  (rep.filas || []).forEach((f, idx) => {
    const isTot = idx === (rep.filas.length - 1);
    rowsHtml += `
      <tr style="${isTot ? 'font-weight:bold; background:#e2e8f0;' : ''}">
        <td style="width:24%; font-weight:bold;">${f.denominacion}</td>
        <td style="width:9.5%; text-align:right;" contenteditable="true" class="eeff-cell-editable" onblur="handleCellEdit(this, ${idx}, 'c1')">${f.c1}</td>
        <td style="width:9.5%; text-align:right;" contenteditable="true" class="eeff-cell-editable" onblur="handleCellEdit(this, ${idx}, 'c2')">${f.c2}</td>
        <td style="width:9.5%; text-align:right;" contenteditable="true" class="eeff-cell-editable" onblur="handleCellEdit(this, ${idx}, 'c3')">${f.c3}</td>
        <td style="width:9.5%; text-align:right;" contenteditable="true" class="eeff-cell-editable" onblur="handleCellEdit(this, ${idx}, 'c4')">${f.c4}</td>
        <td style="width:9.5%; text-align:right;" contenteditable="true" class="eeff-cell-editable" onblur="handleCellEdit(this, ${idx}, 'c5')">${f.c5}</td>
        <td style="width:9.5%; text-align:right;" contenteditable="true" class="eeff-cell-editable" onblur="handleCellEdit(this, ${idx}, 'c6')">${f.c6}</td>
        <td style="width:9.5%; text-align:right;" contenteditable="true" class="eeff-cell-editable" onblur="handleCellEdit(this, ${idx}, 'c7')">${f.c7}</td>
        <td style="width:9.5%; text-align:right; font-weight:bold;" contenteditable="true" class="eeff-cell-editable" onblur="handleCellEdit(this, ${idx}, 'total')">${f.total}</td>
      </tr>
    `;
  });

  return `
    <table class="eeff-table" style="font-size:7pt;">
      <thead>
        <tr>
          <th>Denominación</th>
          <th>Capital Inst.</th>
          <th>Aportes</th>
          <th>Transf./Donac.</th>
          <th>Reservas</th>
          <th>Ajuste Global</th>
          <th>Res. Acum.</th>
          <th>Res. Ejerc.</th>
          <th>Total General</th>
        </tr>
      </thead>
      <tbody>
        ${rowsHtml}
      </tbody>
    </table>
  `;
}

function renderTablaEjecucionRecursos(rep) {
  let rowsHtml = "";
  (rep.filas || []).forEach((f, idx) => {
    rowsHtml += `
      <tr>
        <td style="width:10%; font-family:monospace; font-weight:bold;">${f.rubro}</td>
        <td style="width:36%;">${f.desc}</td>
        <td style="width:11%; text-align:right;" contenteditable="true" class="eeff-cell-editable" onblur="handleCellEdit(this, ${idx}, 'inicial')">${f.inicial}</td>
        <td style="width:10%; text-align:right;" contenteditable="true" class="eeff-cell-editable" onblur="handleCellEdit(this, ${idx}, 'modif')">${f.modif}</td>
        <td style="width:11%; text-align:right; font-weight:bold;" contenteditable="true" class="eeff-cell-editable" onblur="handleCellEdit(this, ${idx}, 'vigente')">${f.vigente}</td>
        <td style="width:11%; text-align:right;" contenteditable="true" class="eeff-cell-editable" onblur="handleCellEdit(this, ${idx}, 'devengado')">${f.devengado}</td>
        <td style="width:11%; text-align:right;" contenteditable="true" class="eeff-cell-editable" onblur="handleCellEdit(this, ${idx}, 'percibido')">${f.percibido}</td>
      </tr>
    `;
  });

  const tot = rep.totales || {};
  return `
    <table class="eeff-table">
      <thead>
        <tr>
          <th>Rubro</th>
          <th>Descripción</th>
          <th>Presup. Inicial</th>
          <th>Modificaciones</th>
          <th>Total Vigente</th>
          <th>Devengado</th>
          <th>Percibido</th>
        </tr>
      </thead>
      <tbody>
        ${rowsHtml}
        <tr style="background:#e2e8f0; font-weight:bold; font-size:8pt; border-top:2px solid #000;">
          <td colspan="2" style="text-align:right;">TOTALES GENERALES :</td>
          <td style="text-align:right;">${tot.inicial || '0.00'}</td>
          <td style="text-align:right;">${tot.modif || '0.00'}</td>
          <td style="text-align:right;">${tot.vigente || '0.00'}</td>
          <td style="text-align:right;">${tot.devengado || '0.00'}</td>
          <td style="text-align:right;">${tot.percibido || '0.00'}</td>
        </tr>
      </tbody>
    </table>
  `;
}

function renderTablaEjecucionGastos(rep) {
  let rowsHtml = "";
  (rep.filas || []).forEach((f, idx) => {
    rowsHtml += `
      <tr>
        <td style="width:9%; font-family:monospace; font-weight:bold;">${f.partida}</td>
        <td style="width:31%;">${f.desc}</td>
        <td style="width:10%; text-align:right;" contenteditable="true" class="eeff-cell-editable" onblur="handleCellEdit(this, ${idx}, 'inicial')">${f.inicial}</td>
        <td style="width:10%; text-align:right;" contenteditable="true" class="eeff-cell-editable" onblur="handleCellEdit(this, ${idx}, 'modif')">${f.modif}</td>
        <td style="width:10%; text-align:right; font-weight:bold;" contenteditable="true" class="eeff-cell-editable" onblur="handleCellEdit(this, ${idx}, 'vigente')">${f.vigente}</td>
        <td style="width:10%; text-align:right;" contenteditable="true" class="eeff-cell-editable" onblur="handleCellEdit(this, ${idx}, 'compromiso')">${f.compromiso}</td>
        <td style="width:10%; text-align:right;" contenteditable="true" class="eeff-cell-editable" onblur="handleCellEdit(this, ${idx}, 'devengado')">${f.devengado}</td>
        <td style="width:10%; text-align:right;" contenteditable="true" class="eeff-cell-editable" onblur="handleCellEdit(this, ${idx}, 'pagado')">${f.pagado}</td>
      </tr>
    `;
  });

  const tot = rep.totales || {};
  return `
    <table class="eeff-table">
      <thead>
        <tr>
          <th>Partida</th>
          <th>Descripción</th>
          <th>Presup. Inicial</th>
          <th>Modificaciones</th>
          <th>Total Vigente</th>
          <th>Compromiso</th>
          <th>Devengado</th>
          <th>Pagado</th>
        </tr>
      </thead>
      <tbody>
        ${rowsHtml}
        <tr style="background:#e2e8f0; font-weight:bold; font-size:8pt; border-top:2px solid #000;">
          <td colspan="2" style="text-align:right;">TOTALES GENERALES :</td>
          <td style="text-align:right;">${tot.inicial || '0.00'}</td>
          <td style="text-align:right;">${tot.modif || '0.00'}</td>
          <td style="text-align:right;">${tot.vigente || '0.00'}</td>
          <td style="text-align:right;">${tot.compromiso || '0.00'}</td>
          <td style="text-align:right;">${tot.devengado || '0.00'}</td>
          <td style="text-align:right;">${tot.pagado || '0.00'}</td>
        </tr>
      </tbody>
    </table>
  `;
}

function renderTablaEstadoCuentas(rep) {
  let rowsHtml = "";
  (rep.filas || []).forEach((f, idx) => {
    rowsHtml += `
      <tr>
        <td style="width:12%; font-family:monospace; font-weight:bold;">${f.cuenta_fmt || f.cuenta}</td>
        <td style="width:40%;">${f.descripcion}</td>
        <td style="width:12%; text-align:right;" contenteditable="true" class="eeff-cell-editable" onblur="handleCellEdit(this, ${idx}, 'saldo_anterior')">${f.saldo_anterior}</td>
        <td style="width:12%; text-align:right;" contenteditable="true" class="eeff-cell-editable" onblur="handleCellEdit(this, ${idx}, 'debe')">${f.debe}</td>
        <td style="width:12%; text-align:right;" contenteditable="true" class="eeff-cell-editable" onblur="handleCellEdit(this, ${idx}, 'haber')">${f.haber}</td>
        <td style="width:12%; text-align:right; font-weight:bold;" contenteditable="true" class="eeff-cell-editable" onblur="handleCellEdit(this, ${idx}, 'saldo_actual')">${f.saldo_actual}</td>
      </tr>
    `;
  });

  const tot = rep.totales || {};
  return `
    <table class="eeff-table">
      <thead>
        <tr>
          <th>Cuenta</th>
          <th>Descripción</th>
          <th>Saldo Anterior</th>
          <th>Debe</th>
          <th>Haber</th>
          <th>Saldo Actual</th>
        </tr>
      </thead>
      <tbody>
        ${rowsHtml}
        <tr style="background:#e2e8f0; font-weight:bold; font-size:8pt; border-top:2px solid #000;">
          <td colspan="2" style="text-align:right;">TOTAL MOVIMIENTOS :</td>
          <td style="text-align:right;">${tot.saldo_anterior || '0.00'}</td>
          <td style="text-align:right;">${tot.total_debe || '0.00'}</td>
          <td style="text-align:right;">${tot.total_haber || '0.00'}</td>
          <td style="text-align:right;">-</td>
        </tr>
      </tbody>
    </table>
  `;
}

function handleCellEdit(cellEl, rowIndex, fieldKey) {
  if (!eeffAllData || !eeffAllData[currentEEFFReportId]) return;

  const newVal = cellEl.textContent.trim();
  const report = eeffAllData[currentEEFFReportId];
  if (report.filas && report.filas[rowIndex]) {
    report.filas[rowIndex][fieldKey] = newVal;
    eeffModifiedReports[currentEEFFReportId] = true;
    actualizarEstadoBadgeEEFF();
  }
}

async function guardarCambiosEEFFActual() {
  if (!eeffAllData || !eeeffAllData[currentEEFFReportId]) return;

  const report = eeffAllData[currentEEFFReportId];
  try {
    const res = await fetch(`/api/eeff/${currentEEFFReportId}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(report)
    });
    if (res.ok) {
      delete eeffModifiedReports[currentEEFFReportId];
      actualizarEstadoBadgeEEFF();
      showToast(`💾 Cambios guardados con éxito para ${report.titulo}.`);
    } else {
      throw new Error("Error en el servidor al guardar cambios.");
    }
  } catch (err) {
    showToast(`❌ Error al guardar: ${err.message}`, 4000);
  }
}

async function recalcularEEFFActual() {
  if (!confirm(`¿Deseas recalcular ${currentEEFFReportId} directamente desde los 36 comprobantes y descartar ediciones manuales?`)) {
    return;
  }

  try {
    const res = await fetch(`/api/eeff/${currentEEFFReportId}/reset`, { method: "POST" });
    if (res.ok) {
      const fresh = await res.json();
      eeffAllData[currentEEFFReportId] = fresh;
      delete eeffModifiedReports[currentEEFFReportId];
      seleccionarReporteEEFF(currentEEFFReportId);
      showToast(`🔄 Reporte recalculado fielmente desde los comprobantes.`);
    } else {
      throw new Error("No se pudo reiniciar el reporte.");
    }
  } catch (err) {
    showToast(`❌ Error al recalcular: ${err.message}`, 4000);
  }
}

function descargarDocxEEFFActual() {
  showToast(`📄 Generando documento Word oficial de ${currentEEFFReportId}...`);
  window.location.href = `/api/eeff/${currentEEFFReportId}/download-docx`;
}

function imprimirEEFFActual() {
  const paperEl = document.getElementById("eeff-paper-wrapper");
  if (!paperEl) return;

  const printWin = window.open("", "_blank");
  printWin.document.write(`
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <title>${eeffAllData[currentEEFFReportId]?.titulo || 'ESTADO FINANCIERO'}</title>
      <style>
        body { font-family: Arial, sans-serif; font-size: 7.5pt; color: #000; margin: 10mm; }
        .eeff-paper-sheet { border: none !important; box-shadow: none !important; padding: 0 !important; width: 100% !important; }
        .eeff-header-block .top-row { display: flex; justify-content: space-between; font-size: 8pt; margin-bottom: 4px; }
        .eeff-title-banner { background: #f2f2f2; border: 1px solid #000; padding: 4px 10px; text-align: center; font-size: 10.5pt; font-weight: bold; margin: 6px 0 10px 0; }
        .eeff-table { width: 100%; border-collapse: collapse; font-size: 7pt; margin-bottom: 12px; }
        .eeff-table th, .eeff-table td { border: 1px solid #000; padding: 3px 5px; }
        .eeff-table th { background: #f8fafc; font-weight: bold; text-align: center; }
        .eeff-signatures { display: flex; justify-content: space-between; margin-top: 24px; border-top: 1px solid #000; padding-top: 8px; }
        .eeff-sig-box { flex: 1; text-align: center; font-size: 7pt; }
        .eeff-sig-line { border-bottom: 1px solid #000; height: 35px; margin-bottom: 4px; }
        @page { size: letter portrait; margin: 8mm 10mm; }
      </style>
    </head>
    <body>
      ${paperEl.innerHTML}
      <script>
        window.onload = function() { window.print(); }
      </script>
    </body>
    </html>
  `);
  printWin.document.close();
}
