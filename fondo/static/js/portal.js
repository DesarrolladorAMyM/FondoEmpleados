// 
//  ESTADO GLOBAL
// 

let currentStep = 1;
const TOTAL_STEPS = 5;



//  UTILIDADES DE ERROR



function markError(field, msg) {
  clearError(field);
  field.classList.add('input--error');

  const errorEl = document.createElement('span');
  errorEl.className = 'field-error';
  errorEl.textContent = msg;

  const hint = field.parentElement.querySelector('.form__hint');
  if (hint) {
    hint.insertAdjacentElement('afterend', errorEl);
  } else if (field.type === 'checkbox' || field.type === 'radio') {
    
    const wrapper = field.closest('label') || field.parentElement;
    wrapper.insertAdjacentElement('afterend', errorEl);
  } else {
    field.insertAdjacentElement('afterend', errorEl);
  }
}

function clearError(field) {
  field.classList.remove('input--error');
  const prev = field.parentElement.querySelector('.field-error');
  if (prev) prev.remove();
}

function clearAllErrors() {
  document.querySelectorAll('.input--error').forEach(f => f.classList.remove('input--error'));
  document.querySelectorAll('.field-error').forEach(el => el.remove());
  document.querySelectorAll('.panel-error').forEach(el => el.remove());
}

function showPanelError(panelId, msg) {
  const panel = document.getElementById(panelId);
  const existing = panel.querySelector('.panel-error');
  if (existing) existing.remove();

  const div = document.createElement('div');
  div.className = 'panel-error';
  div.innerHTML = `<i class="fas fa-circle-exclamation"></i> ${msg}`;
  panel.querySelector('.form-panel__header').insertAdjacentElement('afterend', div);
}


// ═══════════════════════════════════════════════════════
//  HELPERS DE VALIDACIÓN
// ═══════════════════════════════════════════════════════

const REGEX = {
  soloLetras:  /^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s\-']+$/,
  correo:      /^[\w.+\-]+@[\w\-]+\.[a-zA-Z]{2,}$/,
  celular:     /^3\d{9}$/,
  soloDigitos: /^\d+$/,
};

function esMayorDeEdad(fechaStr) {
  const fecha = new Date(fechaStr);
  const hoy   = new Date();
  const edad  = Math.floor((hoy - fecha) / (365.25 * 24 * 3600 * 1000));
  return edad >= 18;
}

function esFechaFutura(fechaStr) {
  return new Date(fechaStr) > new Date();
}

function edadExcesiva(fechaStr) {
  const fecha = new Date(fechaStr);
  const hoy   = new Date();
  const edad  = Math.floor((hoy - fecha) / (365.25 * 24 * 3600 * 1000));
  return edad > 100;
}


// ═══════════════════════════════════════════════════════
//  VALIDACIÓN POR PASO
// ═══════════════════════════════════════════════════════

// ── PASO 1: Identificación
function validateStep1() {
  let ok = true;
  clearAllErrors();

  const tipoDoc   = document.getElementById('tipo-doc');
  const numDoc    = document.getElementById('num-doc');
  const correoReg = document.getElementById('correo-reg');
  const autoriza  = document.getElementById('autoriza-datos');

  if (!tipoDoc.value) {
    markError(tipoDoc, 'Selecciona el tipo de documento.');
    ok = false;
  }

  if (!numDoc.value.trim()) {
    markError(numDoc, 'El número de documento es obligatorio.');
    ok = false;
  } else if (!REGEX.soloDigitos.test(numDoc.value.trim())) {
    markError(numDoc, 'Solo se permiten dígitos.');
    ok = false;
  } else {
    const longitudes = { CC: [6, 10], CE: [6, 12], PA: [5, 20], NIT: [9, 10] };
    const tipo = tipoDoc.value;
    if (longitudes[tipo]) {
      const [min, max] = longitudes[tipo];
      const len = numDoc.value.trim().length;
      if (len < min || len > max) {
        markError(numDoc, `Para ${tipo} el documento debe tener entre ${min} y ${max} dígitos.`);
        ok = false;
      }
    }
  }

  if (!correoReg.value.trim()) {
    markError(correoReg, 'El correo registrado es obligatorio.');
    ok = false;
  } else if (!REGEX.correo.test(correoReg.value.trim())) {
    markError(correoReg, 'Ingresa un correo electrónico válido.');
    ok = false;
  }

  if (!autoriza.checked) {
    markError(autoriza, 'Debes aceptar el tratamiento de datos para continuar.');
    ok = false;
  }

  return ok;
}

// ── PASO 2: Datos personales
function validateStep2() {
  let ok = true;
  clearAllErrors();

  const pNombre    = document.getElementById('p-nombre');
  const sNombre    = document.getElementById('s-nombre');
  const pApellido  = document.getElementById('p-apellido');
  const sApellido  = document.getElementById('s-apellido');
  const fechaNac   = document.getElementById('fecha-nac');
  const genero     = document.getElementById('genero');
  const telCel     = document.getElementById('tel-cel');
  const depto      = document.getElementById('departamento');
  const ciudad     = document.getElementById('ciudad');
  const direccion  = document.getElementById('direccion');
  const correoReg  = document.getElementById('correo-reg');

  if (!pNombre.value.trim()) {
    markError(pNombre, 'El primer nombre es obligatorio.');
    ok = false;
  } else if (!REGEX.soloLetras.test(pNombre.value.trim())) {
    markError(pNombre, 'El nombre solo puede contener letras.');
    ok = false;
  } else if (pNombre.value.trim().length < 2) {
    markError(pNombre, 'El nombre debe tener al menos 2 caracteres.');
    ok = false;
  }

  if (sNombre.value.trim() && !REGEX.soloLetras.test(sNombre.value.trim())) {
    markError(sNombre, 'El segundo nombre solo puede contener letras.');
    ok = false;
  }

  if (!pApellido.value.trim()) {
    markError(pApellido, 'El primer apellido es obligatorio.');
    ok = false;
  } else if (!REGEX.soloLetras.test(pApellido.value.trim())) {
    markError(pApellido, 'El apellido solo puede contener letras.');
    ok = false;
  } else if (pApellido.value.trim().length < 2) {
    markError(pApellido, 'El apellido debe tener al menos 2 caracteres.');
    ok = false;
  }

  if (sApellido.value.trim() && !REGEX.soloLetras.test(sApellido.value.trim())) {
    markError(sApellido, 'El segundo apellido solo puede contener letras.');
    ok = false;
  }

  if (!fechaNac.value) {
    markError(fechaNac, 'La fecha de nacimiento es obligatoria.');
    ok = false;
  } else if (esFechaFutura(fechaNac.value)) {
    markError(fechaNac, 'La fecha de nacimiento no puede ser futura.');
    ok = false;
  } else if (!esMayorDeEdad(fechaNac.value)) {
    markError(fechaNac, 'Debes ser mayor de 18 años para usar este portal.');
    ok = false;
  } else if (edadExcesiva(fechaNac.value)) {
    markError(fechaNac, 'Verifica la fecha de nacimiento ingresada.');
    ok = false;
  }

  if (!genero.value) {
    markError(genero, 'Selecciona el género.');
    ok = false;
  }

  const celLimpio = telCel.value.replace(/[\s\-]/g, '').replace('+57', '');
  if (!telCel.value.trim()) {
    markError(telCel, 'El celular es obligatorio.');
    ok = false;
  } else if (!REGEX.celular.test(celLimpio)) {
    markError(telCel, 'Ingresa un celular colombiano válido (10 dígitos, empieza por 3).');
    ok = false;
  }


  if (!depto.value) {
    markError(depto, 'El departamento es obligatorio.');
    ok = false;
  }

  if (!ciudad.value.trim()) {
    markError(ciudad, 'La ciudad es obligatoria.');
    ok = false;
  } else if (ciudad.value.trim().length < 3) {
    markError(ciudad, 'Ingresa el nombre completo de tu ciudad.');
    ok = false;
  }

  if (!direccion.value.trim()) {
    markError(direccion, 'La dirección de residencia es obligatoria.');
    ok = false;
  } else if (direccion.value.trim().length < 8) {
    markError(direccion, 'Ingresa una dirección más completa.');
    ok = false;
  }

  return ok;
}

// ── PASO 3: Información financiera
// NOTA: Solo valida los campos que realmente existen en el HTML actual.
function validateStep3() {
  let ok = true;
  clearAllErrors();

  // Patrimonio
  const patrimonio = document.getElementById('patrimonio');
  if (!patrimonio || !patrimonio.value) {
    if (patrimonio) markError(patrimonio, 'Selecciona el rango de patrimonio.');
    ok = false;
  }

  // Fuente de recursos (radio obligatorio)
  const fuenteChecked = document.querySelector('input[name="fuente_recursos"]:checked');
  if (!fuenteChecked) {
    const fuenteGroup = document.getElementById('fuente-recursos-group');
    if (fuenteGroup) {
      const prevErr = fuenteGroup.querySelector('.field-error');
      if (prevErr) prevErr.remove();
      const span = document.createElement('span');
      span.className = 'field-error';
      span.textContent = 'Indica la fuente de tus recursos.';
      fuenteGroup.appendChild(span);
    }
    ok = false;
  } else if (fuenteChecked.value === 'otro') {
    // Si eligió "Otro", el texto es obligatorio
    const otroTexto = document.getElementById('otro-fuente-texto');
    if (otroTexto && !otroTexto.value.trim()) {
      markError(otroTexto, 'Especifica la fuente de tus recursos.');
      ok = false;
    }
  }

  // Residencia fiscal (radio obligatorio)
  const residenciaChecked = document.querySelector('input[name="residencia_fiscal"]:checked');
  if (!residenciaChecked) {
    const residenciaGroup = document.getElementById('residencia-fiscal-group');
    if (residenciaGroup) {
      const prevErr = residenciaGroup.querySelector('.field-error');
      if (prevErr) prevErr.remove();
      const span = document.createElement('span');
      span.className = 'field-error';
      span.textContent = 'Indica si tienes residencia fiscal en otro país.';
      residenciaGroup.appendChild(span);
    }
    ok = false;
  } else if (residenciaChecked.value === 'si') {
    // Si respondió Sí, el país es obligatorio
    const paisInput = document.getElementById('residencia-fiscal-pais');
    if (paisInput && !paisInput.value.trim()) {
      markError(paisInput, 'Indica el país de residencia fiscal.');
      ok = false;
    }
  }

  // Declarante de renta (radio obligatorio)
  const decRenta = document.querySelector('input[name="declarante_renta"]:checked');
  if (!decRenta) {
    const decGroup = document.querySelector('input[name="declarante_renta"]')?.closest('.form__group');
    if (decGroup) {
      const prevErr = decGroup.querySelector('.field-error');
      if (prevErr) prevErr.remove();
      const span = document.createElement('span');
      span.className = 'field-error';
      span.textContent = 'Indica si eres declarante de renta.';
      decGroup.appendChild(span);
    }
    ok = false;
  }

  // PEP (radio obligatorio)
  const pep = document.querySelector('input[name="pep"]:checked');
  if (!pep) {
    const pepGroup = document.querySelector('input[name="pep"]')?.closest('.form__group');
    if (pepGroup) {
      const prevErr = pepGroup.querySelector('.field-error');
      if (prevErr) prevErr.remove();
      const span = document.createElement('span');
      span.className = 'field-error';
      span.textContent = 'Indica si eres Persona Expuesta Políticamente.';
      pepGroup.appendChild(span);
    }
    ok = false;
  }

  return ok;
}

// ── PASO 4: Autorizaciones
function validateStep4() {
  let ok = true;
  clearAllErrors();

  const acepta = document.querySelector('input[name="acepta_autorizaciones"]:checked');
  if (!acepta) {
    const aceptaInput = document.getElementById('acepta-autorizaciones');
    if (aceptaInput) {
      const prevErr = aceptaInput.closest('.auth-accept')?.parentElement?.querySelector('.field-error-auth');
      if (prevErr) prevErr.remove();

      const span = document.createElement('span');
      span.className = 'field-error field-error-auth';
      span.style.display = 'block';
      span.style.marginTop = '0.5rem';
      span.textContent = 'Debes leer y aceptar todas las autorizaciones para continuar.';
      aceptaInput.closest('.auth-accept').insertAdjacentElement('afterend', span);
    }
    ok = false;
  }

  return ok;
}

// ── PASO 5: Confirmación final
function validateStep5() {
  const confirma = document.getElementById('confirma-envio');
  if (!confirma.checked) {
    markError(confirma, 'Debes confirmar que la información es veraz para enviar.');
    return false;
  }
  return true;
}


// ═══════════════════════════════════════════════════════
//  NAVEGACIÓN ENTRE PASOS
// ═══════════════════════════════════════════════════════

async function goToStep(targetStep) {
  // Validar paso actual antes de avanzar
  if (targetStep > currentStep) {
    let valid = true;
    if (currentStep === 1) valid = validateStep1();
    if (currentStep === 2) valid = validateStep2();
    if (currentStep === 3) valid = validateStep3();
    if (currentStep === 4) valid = validateStep4();
    if (!valid) return;

    // ── NUEVA VALIDACIÓN AJAX: verificar duplicado al salir del paso 1 ──
    if (currentStep === 1 && targetStep === 2) {
      const pasaValidacion = await verificarPaso1EnServidor();
      if (!pasaValidacion) return;  // se muestra el error en el campo, no avanzamos
    }
  }

  // Ocultar panel actual
  const currentPanel = document.getElementById(`panel-${currentStep}`);
  if (currentPanel) currentPanel.classList.remove('active');

  // Actualizar indicador actual
  const currentIndicator = document.getElementById(`step-indicator-${currentStep}`);
  if (currentIndicator) {
    currentIndicator.classList.remove('active');
    if (targetStep > currentStep) currentIndicator.classList.add('completed');
  }

  currentStep = targetStep;

  // Mostrar panel nuevo
  const newPanel = document.getElementById(`panel-${currentStep}`);
  if (newPanel) newPanel.classList.add('active');

  // Activar indicador nuevo
  const newIndicator = document.getElementById(`step-indicator-${currentStep}`);
  if (newIndicator) {
    newIndicator.classList.remove('completed');
    newIndicator.classList.add('active');
  }

  // Construir resumen si vamos al paso 5 (confirmación)
  if (currentStep === 5) buildSummary();

  // Scroll al inicio del formulario
  document.querySelector('.portal__form-wrapper')
    ?.scrollIntoView({ behavior: 'smooth', block: 'start' });
}


// ═══════════════════════════════════════════════════════
//  AJAX: VERIFICAR PASO 1 EN EL SERVIDOR
// ═══════════════════════════════════════════════════════

async function verificarPaso1EnServidor() {
  const btn = document.querySelector('#panel-1 .btn--primary');

  // Feedback visual mientras espera respuesta
  const textoOriginal = btn.innerHTML;
  btn.disabled = true;
  btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Verificando…';

  try {
    const formData = new FormData();
    formData.append('tipo_documento',   document.getElementById('tipo-doc').value);
    formData.append('numero_documento', document.getElementById('num-doc').value.trim());
    formData.append('correo_registrado',document.getElementById('correo-reg').value.trim());
    formData.append('año',              document.getElementById('año').value.trim());

    const response = await fetch('/FondoEmpleados/PortalAsociados/verificar-paso1/', {   // ← ajusta la URL si tu proyecto usa prefijo
      method: 'POST',
      headers: { 'X-CSRFToken': getCookie('csrftoken') },
      body: formData,
    });

    const data = await response.json();

    if (data.ok) {
      return true;   // todo bien, dejamos avanzar
    }

    // Mostrar errores devueltos por el servidor en los campos del paso 1
    const campoMap = {
      tipo_documento:    'tipo-doc',
      numero_documento:  'num-doc',
      correo_registrado: 'correo-reg',
      año:               'año',
    };

    for (const [campo, mensaje] of Object.entries(data.errores || {})) {
      const htmlId = campoMap[campo];
      if (htmlId) {
        const el = document.getElementById(htmlId);
        if (el) markError(el, mensaje);
      }
    }

    return false;   // hay errores, no avanzamos

  } catch (err) {
    console.error('[FAMYM] Error verificando paso 1:', err);
    showPanelError('panel-1', 'Error de conexión al verificar tus datos. Intenta de nuevo.');
    return false;

  } finally {
    // Restaurar botón siempre
    btn.disabled = false;
    btn.innerHTML = textoOriginal;
  }
}

// ═══════════════════════════════════════════════════════
//  RESUMEN EN PASO 5
// ═══════════════════════════════════════════════════════

function buildSummary() {
  const contenedor = document.getElementById('summary-content');
  if (!contenedor) return;

  // Campos estándar (input / select)
  const campos = [
    { label: 'Tipo de documento',  id: 'tipo-doc',    tipo: 'select' },
    { label: 'Número de documento',id: 'num-doc',      tipo: 'input'  },
    { label: 'Correo registrado',  id: 'correo-reg',   tipo: 'input'  },
    { label: 'Primer nombre',      id: 'p-nombre',     tipo: 'input'  },
    { label: 'Primer apellido',    id: 'p-apellido',   tipo: 'input'  },
    { label: 'Fecha nacimiento',   id: 'fecha-nac',    tipo: 'input'  },
    { label: 'Celular',            id: 'tel-cel',      tipo: 'input'  },
    { label: 'Correo nuevo',       id: 'email-nuevo',  tipo: 'input'  },
    { label: 'Departamento',       id: 'departamento', tipo: 'select' },
    { label: 'Ciudad',             id: 'ciudad',       tipo: 'input'  },
    { label: 'Dirección',          id: 'direccion',    tipo: 'input'  },
    { label: 'Patrimonio',         id: 'patrimonio',   tipo: 'select' },
  ];

  contenedor.innerHTML = campos.map(campo => {
    const el  = document.getElementById(campo.id);
    const val = el
      ? (el.options ? el.options[el.selectedIndex]?.text : el.value) || '—'
      : '—';
    return `
      <div class="summary-item">
        <span class="summary-label">${campo.label}</span>
        <span class="summary-value">${val}</span>
      </div>
    `;
  }).join('');

  // Fuente de recursos (radio + texto libre si aplica)
  const fuenteChecked = document.querySelector('input[name="fuente_recursos"]:checked');
  let fuenteVal = '—';
  if (fuenteChecked) {
    if (fuenteChecked.value === 'otro') {
      const otroTexto = document.getElementById('otro-fuente-texto');
      fuenteVal = `Otro: ${otroTexto?.value?.trim() || '—'}`;
    } else {
      fuenteVal = 'Salario';
    }
  }

  // Residencia fiscal
  const residenciaChecked = document.querySelector('input[name="residencia_fiscal"]:checked');
  let residenciaVal = '—';
  if (residenciaChecked) {
    if (residenciaChecked.value === 'si') {
      const pais = document.getElementById('residencia-fiscal-pais');
      residenciaVal = `Sí — ${pais?.value?.trim() || '—'}`;
    } else {
      residenciaVal = 'No';
    }
  }

  // Declarante de renta y PEP (radios)
  const decRenta = document.querySelector('input[name="declarante_renta"]:checked');
  const pep      = document.querySelector('input[name="pep"]:checked');

  contenedor.innerHTML += `
    <div class="summary-item">
      <span class="summary-label">Fuente de recursos</span>
      <span class="summary-value">${fuenteVal}</span>
    </div>
    <div class="summary-item">
      <span class="summary-label">Residencia fiscal otro país</span>
      <span class="summary-value">${residenciaVal}</span>
    </div>
    <div class="summary-item">
      <span class="summary-label">Declarante de renta</span>
      <span class="summary-value">${decRenta ? (decRenta.value === 'si' ? 'Sí' : 'No') : '—'}</span>
    </div>
    <div class="summary-item">
      <span class="summary-label">PEP</span>
      <span class="summary-value">${pep ? (pep.value === 'si' ? 'Sí' : 'No') : '—'}</span>
    </div>
    <div class="summary-item">
      <span class="summary-label">Autorizaciones aceptadas</span>
      <span class="summary-value" style="color:var(--success,#16a34a);font-weight:600;">
        <i class="fas fa-circle-check"></i> Sí
      </span>
    </div>
  `;
}


// ═══════════════════════════════════════════════════════
//  ENVÍO DEL FORMULARIO VÍA FETCH
// ═══════════════════════════════════════════════════════

document.addEventListener('DOMContentLoaded', () => {

  const form      = document.getElementById('update-form');
  const submitBtn = document.getElementById('submit-btn');

  if (!form) return;

  // ── Mostrar/ocultar campo "Otro" en fuente de recursos
  document.querySelectorAll('input[name="fuente_recursos"]').forEach(function(radio) {
    radio.addEventListener('change', function() {
      const wrapper   = document.getElementById('otro-fuente-wrapper');
      const textInput = document.getElementById('otro-fuente-texto');
      if (!wrapper || !textInput) return;
      if (this.value === 'otro') {
        wrapper.style.display = 'block';
        textInput.setAttribute('required', 'required');
      } else {
        wrapper.style.display = 'none';
        textInput.removeAttribute('required');
        textInput.value = '';
        clearError(textInput);
      }
    });
  });

  // ── Mostrar/ocultar campo de país en residencia fiscal
  document.querySelectorAll('input[name="residencia_fiscal"]').forEach(function(radio) {
    radio.addEventListener('change', function() {
      const wrapper   = document.getElementById('residencia-fiscal-pais-wrapper');
      const paisInput = document.getElementById('residencia-fiscal-pais');
      if (!wrapper || !paisInput) return;
      if (this.value === 'si') {
        wrapper.style.display = 'block';
        paisInput.setAttribute('required', 'required');
      } else {
        wrapper.style.display = 'none';
        paisInput.removeAttribute('required');
        paisInput.value = '';
        clearError(paisInput);
      }
    });
  });

  // ── Menú hamburguesa
  const navToggle = document.getElementById('nav-toggle');
  const navMenu   = document.getElementById('nav-menu');

  if (navToggle && navMenu) {
    navToggle.addEventListener('click', () => {
      navMenu.classList.toggle('nav__menu--open');
      navToggle.classList.toggle('nav__toggle--open');
    });
  }

  // ── Envío del formulario
  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    if (!validateStep5()) return;

    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Enviando…';

    try {
      const formData = new FormData(form);

      const response = await fetch(form.action || window.location.href, {
        method: 'POST',
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
        body: formData,
      });

      const data = await response.json();

      if (data.ok) {
        document.getElementById(`panel-${currentStep}`).classList.remove('active');
        document.getElementById('panel-success').classList.add('active');
        document.getElementById('radicado-num').textContent = data.radicado;

        const lastIndicator = document.getElementById(`step-indicator-${currentStep}`);
        if (lastIndicator) {
          lastIndicator.classList.remove('active');
          lastIndicator.classList.add('completed');
        }

      } else {
        if (data.errores) {
          if (data.errores.__all__) {
            showPanelError(`panel-${currentStep}`, data.errores.__all__);
          }

          const campoMap = {
            tipo_documento:       'tipo-doc',
            numero_documento:     'num-doc',
            correo_registrado:    'correo-reg',
            p_nombre:             'p-nombre',
            s_nombre:             's-nombre',
            p_apellido:           'p-apellido',
            s_apellido:           's-apellido',
            fecha_nacimiento:     'fecha-nac',
            genero:               'genero',
            celular:              'tel-cel',
            correo_nuevo:         'email-nuevo',
            departamento:         'departamento',
            ciudad:               'ciudad',
            direccion:            'direccion',
            patrimonio:           'patrimonio',
            fuente_recursos:      'fuente-recursos-group',
            fuente_recursos_otro: 'otro-fuente-texto',
            residencia_fiscal:    'residencia-fiscal-group',
            residencia_fiscal_pais: 'residencia-fiscal-pais',
            año:                  'año',
          };

          const campoPaso = {
            tipo_documento: 1, numero_documento: 1, correo_registrado: 1,
            p_nombre: 2, s_nombre: 2, p_apellido: 2, s_apellido: 2,
            fecha_nacimiento: 2, genero: 2, celular: 2, correo_nuevo: 2,
            departamento: 2, ciudad: 2, direccion: 2,
            patrimonio: 3, fuente_recursos: 3, fuente_recursos_otro: 3,
            residencia_fiscal: 3, residencia_fiscal_pais: 3,
            declarante_renta: 3, pep: 3,
            acepta_autorizaciones: 4,
            año: 1,
          };

          let primerPasoConError = null;

          for (const [campo, mensaje] of Object.entries(data.errores)) {
            if (campo === '__all__') continue;

            const htmlId = campoMap[campo];
            const paso   = campoPaso[campo];

            if (paso && (!primerPasoConError || paso < primerPasoConError)) {
              primerPasoConError = paso;
            }

            if (htmlId) {
              const el = document.getElementById(htmlId);
              if (el) markError(el, mensaje);
            }
          }

          if (primerPasoConError && primerPasoConError !== currentStep) {
            document.getElementById(`panel-${currentStep}`).classList.remove('active');
            document.getElementById(`step-indicator-${currentStep}`).classList.remove('active');
            currentStep = primerPasoConError;
            document.getElementById(`panel-${currentStep}`).classList.add('active');
            document.getElementById(`step-indicator-${currentStep}`).classList.add('active');
          }
        }

        submitBtn.disabled = false;
        submitBtn.innerHTML = '<span>Enviar solicitud de actualización</span> <i class="fas fa-paper-plane"></i>';
      }

    } catch (err) {
      console.error('[FAMYM] Error de red:', err);
      showPanelError(`panel-${currentStep}`, 'Ocurrió un error de conexión. Por favor intenta de nuevo.');
      submitBtn.disabled = false;
      submitBtn.innerHTML = '<span>Enviar solicitud de actualización</span> <i class="fas fa-paper-plane"></i>';
    }
  });

  // ── Adjuntar archivos con previsualización y eliminación ──
(function () {
  const input    = document.getElementById('archivo-doc');
  const dropZone = document.getElementById('file-drop');
  const fileList = document.getElementById('file-list');
  if (!input || !dropZone || !fileList) return;

  // Array propio porque FileList es inmutable
  let archivos = [];

  // Renderiza las tarjetas de vista previa
  function renderFiles() {
    fileList.innerHTML = '';

    archivos.forEach((file, index) => {
      const item = document.createElement('div');
      item.className = 'file-item';

      const esImagen = file.type.startsWith('image/');

      if (esImagen) {
        const img = document.createElement('img');
        img.className = 'file-item__preview';
        img.alt = file.name;
        img.src = URL.createObjectURL(file);
        img.onload = () => URL.revokeObjectURL(img.src); // libera memoria
        item.appendChild(img);
      } else {
        const icon = document.createElement('div');
        icon.className = 'file-item__icon';
        icon.innerHTML = '<i class="fas fa-file-pdf"></i>';
        item.appendChild(icon);
      }

      const name = document.createElement('div');
      name.className = 'file-item__name';
      name.title = file.name;
      name.textContent = file.name;
      item.appendChild(name);

      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'file-item__remove';
      btn.title = 'Eliminar archivo';
      btn.innerHTML = '<i class="fas fa-xmark"></i>';
      btn.addEventListener('click', () => {
        archivos.splice(index, 1);
        sincronizarInput();
        renderFiles();
      });
      item.appendChild(btn);

      fileList.appendChild(item);
    });
  }

  // Sincroniza el <input type="file"> con nuestro array
  // (necesario para que FormData lo envíe correctamente)
  function sincronizarInput() {
    const dt = new DataTransfer();
    archivos.forEach(f => dt.items.add(f));
    input.files = dt.files;
  }

  // Agrega archivos validando tamaño y duplicados
  function agregarArchivos(nuevos) {
    Array.from(nuevos).forEach(file => {
      if (file.size > 5 * 1024 * 1024) {
        alert(`"${file.name}" supera los 5 MB y no fue agregado.`);
        return;
      }
      const yaExiste = archivos.some(
        f => f.name === file.name && f.size === file.size
      );
      if (!yaExiste) archivos.push(file);
    });
    sincronizarInput();
    renderFiles();
  }

  // Evento: selección normal
  input.addEventListener('change', () => {
    agregarArchivos(input.files);
  });

  // Eventos: drag & drop
  dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('file-drop--over');
  });

  dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('file-drop--over');
  });

  dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('file-drop--over');
    agregarArchivos(e.dataTransfer.files);
  });
})();


});


// ═══════════════════════════════════════════════════════
//  RESET DEL FORMULARIO
// ═══════════════════════════════════════════════════════

function resetForm() {
  document.getElementById('update-form').reset();
  clearAllErrors();

  // Ocultar campo "Otro" de fuente de recursos
  const otroWrapper = document.getElementById('otro-fuente-wrapper');
  if (otroWrapper) otroWrapper.style.display = 'none';

  // Ocultar campo país residencia fiscal
  const paisWrapper = document.getElementById('residencia-fiscal-pais-wrapper');
  if (paisWrapper) paisWrapper.style.display = 'none';

  // Ocultar panel de éxito
  document.getElementById('panel-success').classList.remove('active');

  // Resetear indicadores
  document.querySelectorAll('.form-step').forEach(s => {
    s.classList.remove('active', 'completed');
  });

  currentStep = 1;
  document.getElementById('panel-1').classList.add('active');
  document.getElementById('step-indicator-1').classList.add('active');

  document.querySelector('.portal-hero')?.scrollIntoView({ behavior: 'smooth' });
}


// ═══════════════════════════════════════════════════════
//  UTILIDAD: leer cookie CSRF
// ═══════════════════════════════════════════════════════

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
  return null;
}