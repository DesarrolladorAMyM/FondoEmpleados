import re
import traceback
from datetime import datetime, date
from django.shortcuts import render
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.http import JsonResponse
from .models import SolicitudActualizacion
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt  # maneja el token 
from django.utils import timezone


#validdacion que se hace para hacer una llamada al ajax cuando va en el paso 1 y 2 del formulario 
@require_POST
def verificar_paso1(request):
    tipo_documento = request.POST.get('tipo_documento', '').strip()
    numero_documento = request.POST.get('numero_documento', '').strip()
    correo_registrado = request.POST.get('correo_registrado', '').strip()
    año = request.POST.get('año', '').strip()

    errores = {}
    

    try:
        año_int = int(año)
    except (ValueError, TypeError):
        return JsonResponse({'ok': False, 'errores': {'año': 'Año inválido.'}})
    
    año_actual = timezone.now().year
    if año_int != año_actual:
        return JsonResponse({
            'ok': False,
            'errores': {'año': f'Debes ingresar el año actual ({año_actual}).'}
        })

    # Busca si ya existe una actualización este año para este asociado
    ya_actualizo = SolicitudActualizacion.objects.filter(
        Tipo_documento=tipo_documento,
        Numero_documento=numero_documento,
        Correo_registrado=correo_registrado,
        Fecha_envio__year=año_int, 
    ).first()

    if ya_actualizo:
        errores['año'] = (
            f'Ya realizaste una actualización en el año {año_int} '
            f'(Radicado: {ya_actualizo.Numero_radicado}). '
            f'Solo se permite una actualización por año.'
        )
        return JsonResponse({'ok': False, 'errores': errores})

    return JsonResponse({'ok': True})




# HELPERS DE VALIDACIÓN


def solo_letras(valor):
    return bool(re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s\-']+$", valor))

def correo_valido(correo):
    return bool(re.match(r'^[\w\.\+\-]+@[\w\-]+\.[a-zA-Z]{2,}$', correo))

def celular_valido(cel):
    cel_limpio = cel.replace(' ', '').replace('-', '').replace('+57', '')
    return bool(re.match(r'^3\d{9}$', cel_limpio))

def validar_archivos(archivos):
    TIPOS_PERMITIDOS = ['application/pdf', 'image/jpeg', 'image/png']
    TAMANIO_MAX = 5 * 1024 * 1024  # 5 MB
    for archivo in archivos:
        if archivo.content_type not in TIPOS_PERMITIDOS:
            return f'Tipo de archivo no permitido: "{archivo.name}". Solo PDF, JPG y PNG.'
        if archivo.size > TAMANIO_MAX:
            return f'El archivo "{archivo.name}" supera los 5 MB permitidos.'
    return None


# ─────────────────────────────────────────
#  GENERADOR DE RADICADO
# ─────────────────────────────────────────

def generar_radicado():
    fecha = datetime.now().strftime("%Y%m%d")
    total = SolicitudActualizacion.objects.count()
    consecutivo = str(total + 1).zfill(5)
    return f"RAD-{fecha}-{consecutivo}"


# ─────────────────────────────────────────
#  VISTA PRINCIPAL
# ─────────────────────────────────────────

def Asociados(request):

    if request.method != 'POST':
        return render(request, "PortalAsociados/portalAsociados.html")

    try:

        # ── EXTRACCIÓN DE DATOS ──────────────────────────────────────
        Tipo_documento         = request.POST.get('tipo_documento',         '').strip()
        Numero_documento       = request.POST.get('numero_documento',       '').strip()
        Correo_registrado      = request.POST.get('correo_registrado',      '').strip().lower()
        P_nombre               = request.POST.get('p_nombre',               '').strip()
        S_nombre               = request.POST.get('s_nombre',               '').strip()
        P_apellido             = request.POST.get('p_apellido',             '').strip()
        S_apellido             = request.POST.get('s_apellido',             '').strip()
        Fecha_nacimiento       = request.POST.get('fecha_nacimiento',       '').strip()
        Genero                 = request.POST.get('genero',                 '').strip()
        Celular                = request.POST.get('celular',                '').strip()
        Telefono_fijo          = request.POST.get('telefono_fijo',          '').strip()
        Departamento           = request.POST.get('departamento',           '').strip()
        Ciudad                 = request.POST.get('ciudad',                 '').strip()
        Direccion              = request.POST.get('direccion',              '').strip()
        Fuentes_recursos       = request.POST.get('fuente_recursos',        '').strip()
        Fuentes_recursos_otro  = request.POST.get('fuente_recursos_otro',   '').strip()

        Año = (
            request.POST.get('año', '') or
            request.POST.get('ano', '') or
            request.POST.get('a\xf1o', '')
        ).strip()

        Residencia_fiscal      = request.POST.get('residencia_fiscal',      '').strip()
        Residencia_fiscal_pais = request.POST.get('residencia_fiscal_pais', '').strip()
        Patrimonio             = request.POST.get('patrimonio',             '').strip()
        Declarante_renta       = request.POST.get('declarante_renta',       '').strip()
        PeP                    = request.POST.get('pep',                    '').strip()
        Observaciones          = request.POST.get('observaciones',          '').strip()
        archivos               = request.FILES.getlist('archivo-doc')

        errores = {}

        # ════════════════════════════════════════════════════════════
        # PASO 1 — Identificación del Asociado
        # ════════════════════════════════════════════════════════════
        TIPOS_VALIDOS = ['CC', 'CE', 'PA', 'NIT']
        if not Tipo_documento:
            errores['tipo_documento'] = 'Selecciona el tipo de documento.'
        elif Tipo_documento not in TIPOS_VALIDOS:
            errores['tipo_documento'] = 'Tipo de documento no válido.'

        if not Numero_documento:
            errores['numero_documento'] = 'El número de documento es obligatorio.'
        elif not Numero_documento.isdigit():
            errores['numero_documento'] = 'El número de documento solo puede contener dígitos.'
        else:
            longitudes = {'CC': (6, 10), 'CE': (6, 12), 'PA': (5, 20), 'NIT': (9, 10)}
            if Tipo_documento in longitudes:
                min_len, max_len = longitudes[Tipo_documento]
                if not (min_len <= len(Numero_documento) <= max_len):
                    errores['numero_documento'] = (
                        f'Para {Tipo_documento} el documento debe tener '
                        f'entre {min_len} y {max_len} dígitos.'
                    )

        if not Correo_registrado:
            errores['correo_registrado'] = 'El correo registrado es obligatorio.'
        elif not correo_valido(Correo_registrado):
            errores['correo_registrado'] = 'Ingresa un correo electrónico válido.'

        #  Validación de año duplicado movida aquí — Paso 1
        # Solo se ejecuta si documento y año llegan sin errores previos
        año_int_valido = Año.isdigit() and len(Año) == 4 and int(Año) <= datetime.now().year
        if (
            'numero_documento' not in errores
            and Numero_documento
            and año_int_valido
        ):
            ya_actualizo = SolicitudActualizacion.objects.filter(
                Numero_documento=Numero_documento,
                Año=Año,
            ).first()
            if ya_actualizo:
                errores['año'] = (
                    f'Ya realizaste una actualización en el año {Año} '
                    f'(Radicado: {ya_actualizo.Numero_radicado}). '
                    f'Solo se permite una actualización por año.'
                )

        # ════════════════════════════════════════════════════════════
        # PASO 2 — Datos Personales
        # ════════════════════════════════════════════════════════════
        if not P_nombre:
            errores['p_nombre'] = 'El primer nombre es obligatorio.'
        elif not solo_letras(P_nombre):
            errores['p_nombre'] = 'El nombre solo puede contener letras.'
        elif len(P_nombre) < 2:
            errores['p_nombre'] = 'El nombre debe tener al menos 2 caracteres.'

        if S_nombre and not solo_letras(S_nombre):
            errores['s_nombre'] = 'El segundo nombre solo puede contener letras.'

        if not P_apellido:
            errores['p_apellido'] = 'El primer apellido es obligatorio.'
        elif not solo_letras(P_apellido):
            errores['p_apellido'] = 'El apellido solo puede contener letras.'
        elif len(P_apellido) < 2:
            errores['p_apellido'] = 'El apellido debe tener al menos 2 caracteres.'

        if S_apellido and not solo_letras(S_apellido):
            errores['s_apellido'] = 'El segundo apellido solo puede contener letras.'

        if not Fecha_nacimiento:
            errores['fecha_nacimiento'] = 'La fecha de nacimiento es obligatoria.'
        else:
            try:
                fecha_nac = date.fromisoformat(Fecha_nacimiento)
                hoy  = date.today()
                edad = (hoy - fecha_nac).days // 365
                if fecha_nac > hoy:
                    errores['fecha_nacimiento'] = 'La fecha de nacimiento no puede ser futura.'
                elif edad < 18:
                    errores['fecha_nacimiento'] = 'Debes ser mayor de 18 años para usar este portal.'
                elif edad > 100:
                    errores['fecha_nacimiento'] = 'Verifica la fecha de nacimiento ingresada.'
            except ValueError:
                errores['fecha_nacimiento'] = 'Formato de fecha inválido.'

        GENEROS_VALIDOS = ['M', 'F', 'NB', 'ND']
        if not Genero:
            errores['genero'] = 'Selecciona el género.'
        elif Genero not in GENEROS_VALIDOS:
            errores['genero'] = 'Opción de género no válida.'

        if not Celular:
            errores['celular'] = 'El número de celular es obligatorio.'
        elif not celular_valido(Celular):
            errores['celular'] = 'Ingresa un celular colombiano válido (10 dígitos, empieza por 3).'


        if not Departamento:
            errores['departamento'] = 'El departamento es obligatorio.'

        if not Ciudad:
            errores['ciudad'] = 'La ciudad es obligatoria.'
        elif len(Ciudad) < 3:
            errores['ciudad'] = 'Ingresa el nombre completo de tu ciudad.'

        if not Direccion:
            errores['direccion'] = 'La dirección de residencia es obligatoria.'
        elif len(Direccion) < 8:
            errores['direccion'] = 'Ingresa una dirección más completa.'

        
        # PASO 3 — Información Financiera
        
        if not Fuentes_recursos:
            errores['fuente_recursos'] = 'Indica la fuente de tus recursos.'
        elif Fuentes_recursos not in ['salario', 'otro']:
            errores['fuente_recursos'] = 'Valor no válido para este campo.'
        elif Fuentes_recursos == 'otro' and not Fuentes_recursos_otro:
            errores['fuente_recursos_otro'] = 'Debes especificar la fuente de tus recursos.'
        elif Fuentes_recursos == 'otro' and len(Fuentes_recursos_otro) < 3:
            errores['fuente_recursos_otro'] = 'La descripción es demasiado corta.'

        if not Año:
            errores['año'] = 'El año de actualización es obligatorio.'
        elif not Año.isdigit() or len(Año) != 4:
            errores['año'] = 'El año ingresado no es válido.'
        elif int(Año) > datetime.now().year:
            errores['año'] = 'El año no puede ser mayor al año actual.'

        if not Residencia_fiscal:
            errores['residencia_fiscal'] = 'Indica si tienes residencia fiscal en otro país.'
        elif Residencia_fiscal not in ['si', 'no']:
            errores['residencia_fiscal'] = 'Valor no válido para este campo.'
        elif Residencia_fiscal == 'si' and not Residencia_fiscal_pais:
            errores['residencia_fiscal_pais'] = 'Indica el país de residencia fiscal.'
        elif Residencia_fiscal == 'si' and len(Residencia_fiscal_pais) < 3:
            errores['residencia_fiscal_pais'] = 'El nombre del país es demasiado corto.'

        if not Patrimonio:
            errores['patrimonio'] = 'Selecciona el rango de patrimonio.'

        if not Declarante_renta:
            errores['declarante_renta'] = 'Indica si eres declarante de renta.'
        elif Declarante_renta not in ['si', 'no']:
            errores['declarante_renta'] = 'Valor no válido para este campo.'

        if not PeP:
            errores['pep'] = 'Indica si eres Persona Expuesta Políticamente.'
        elif PeP not in ['si', 'no']:
            errores['pep'] = 'Valor no válido para este campo.'

        if archivos:
            error_archivo = validar_archivos(archivos)
            if error_archivo:
                errores['archivo'] = error_archivo

        # ── RETORNAR ERRORES 
        if errores:
            return JsonResponse({'ok': False, 'errores': errores}, status=400)

        #  GENERAR RADICADO Y GUARDAR 
        numero_radicado = generar_radicado()

        SolicitudActualizacion.objects.create(
            Tipo_documento         = Tipo_documento,
            Numero_documento       = Numero_documento,
            Correo_registrado      = Correo_registrado,
            P_nombre               = P_nombre,
            S_nombre               = S_nombre,
            P_apellido             = P_apellido,
            S_apellido             = S_apellido,
            Fecha_nacimiento       = Fecha_nacimiento,
            Genero                 = Genero,
            Celular                = Celular,
            Telefono_fijo          = Telefono_fijo,
            Departamento           = Departamento,
            Ciudad                 = Ciudad,
            Direccion              = Direccion,
            Fuentes_recursos       = Fuentes_recursos,
            Fuentes_recursos_otro  = Fuentes_recursos_otro,
            Año                    = Año,
            Residencia_fiscal      = Residencia_fiscal,
            Residencia_fiscal_pais = Residencia_fiscal_pais,
            Patrimonio             = Patrimonio,
            Declarante_renta       = Declarante_renta,
            PeP                    = PeP,
            Observaciones          = Observaciones,
            Numero_radicado        = numero_radicado,
        )

        nombre_completo = f"{P_nombre} {S_nombre} {P_apellido} {S_apellido}".strip()

        # ── CORREOS 
        logo_url = "https://i.postimg.cc/wv42Tz9x/logo-F.jpg"

        asunto_admin = f"Nueva solicitud de actualización | {nombre_completo} | {numero_radicado}"

        texto_plano_admin = f"""
Nueva solicitud de actualización de datos — FAMYM
Radicado: {numero_radicado}

IDENTIFICACIÓN
Tipo documento:    {Tipo_documento}
Número documento:  {Numero_documento}
Correo registrado: {Correo_registrado}

DATOS PERSONALES
Nombre completo:  {nombre_completo}
Fecha nacimiento: {Fecha_nacimiento}
Género:           {Genero}
Celular:          {Celular}
Teléfono fijo:    {Telefono_fijo or '—'}

UBICACIÓN
Departamento: {Departamento}
Ciudad:       {Ciudad}
Dirección:    {Direccion}

INFORMACIÓN ECONÓMICA
Fuente recursos:      {Fuentes_recursos}
Fuente recursos otro: {Fuentes_recursos_otro or '—'}
Año actualización:    {Año}
Residencia fiscal:    {'Sí — ' + Residencia_fiscal_pais if Residencia_fiscal == 'si' else 'No'}
Patrimonio:           {Patrimonio}
Declarante de renta:  {Declarante_renta}
PEP:                  {PeP}

OBSERVACIONES
{Observaciones or 'Sin observaciones'}
        """

        html_admin = f"""
        <html>
        <body style="margin:0;padding:30px;background:#f1f5f9;font-family:Arial,sans-serif;">
            <div style="max-width:720px;margin:auto;background:#fff;border-radius:14px;overflow:hidden;box-shadow:0 0 20px rgba(0,0,0,.08);">
                <div style="background:linear-gradient(135deg,#0a1628,#1a56db);padding:32px;text-align:center;">
                    <img src="{logo_url}" alt="FAMYM Logo" width="110" style="display:block;margin:0 auto 14px;" />
                    <h1 style="color:#fff;margin:0;font-size:24px;">FAMYM</h1>
                    <p style="color:rgba(255,255,255,0.7);margin:6px 0 0;">Fondo de Empleados AMYM</p>
                    <p style="color:#00c6b8;margin:8px 0 0;font-weight:bold;">Solicitud de Actualización de Datos</p>
                    <div style="display:inline-block;background:rgba(255,255,255,0.15);border-radius:8px;padding:6px 18px;margin-top:10px;">
                        <span style="color:#fff;font-size:13px;">Radicado: <strong>{numero_radicado}</strong></span>
                    </div>
                </div>
                <div style="padding:36px;">
                    <h3 style="color:#1a56db;border-bottom:2px solid #e2e8f0;padding-bottom:8px;margin-top:0;">Identificación</h3>
                    <table style="width:100%;border-collapse:collapse;font-size:14px;margin-bottom:24px;">
                        <tr><td style="padding:9px 10px;border-bottom:1px solid #e2e8f0;color:#64748b;width:200px;"><b>Tipo de documento</b></td><td style="padding:9px 10px;border-bottom:1px solid #e2e8f0;">{Tipo_documento}</td></tr>
                        <tr><td style="padding:9px 10px;border-bottom:1px solid #e2e8f0;color:#64748b;"><b>Número de documento</b></td><td style="padding:9px 10px;border-bottom:1px solid #e2e8f0;">{Numero_documento}</td></tr>
                        <tr><td style="padding:9px 10px;border-bottom:1px solid #e2e8f0;color:#64748b;"><b>Correo registrado</b></td><td style="padding:9px 10px;border-bottom:1px solid #e2e8f0;">{Correo_registrado}</td></tr>
                    </table>

                    <h3 style="color:#1a56db;border-bottom:2px solid #e2e8f0;padding-bottom:8px;">Datos Personales</h3>
                    <table style="width:100%;border-collapse:collapse;font-size:14px;margin-bottom:24px;">
                        <tr><td style="padding:9px 10px;border-bottom:1px solid #e2e8f0;color:#64748b;width:200px;"><b>Nombre completo</b></td><td style="padding:9px 10px;border-bottom:1px solid #e2e8f0;font-weight:bold;">{nombre_completo}</td></tr>
                        <tr><td style="padding:9px 10px;border-bottom:1px solid #e2e8f0;color:#64748b;"><b>Fecha de nacimiento</b></td><td style="padding:9px 10px;border-bottom:1px solid #e2e8f0;">{Fecha_nacimiento}</td></tr>
                        <tr><td style="padding:9px 10px;border-bottom:1px solid #e2e8f0;color:#64748b;"><b>Género</b></td><td style="padding:9px 10px;border-bottom:1px solid #e2e8f0;">{Genero}</td></tr>
                        <tr><td style="padding:9px 10px;border-bottom:1px solid #e2e8f0;color:#64748b;"><b>Celular</b></td><td style="padding:9px 10px;border-bottom:1px solid #e2e8f0;">{Celular}</td></tr>
                        <tr><td style="padding:9px 10px;border-bottom:1px solid #e2e8f0;color:#64748b;"><b>Teléfono fijo</b></td><td style="padding:9px 10px;border-bottom:1px solid #e2e8f0;">{Telefono_fijo or '—'}</td></tr>
                    </table>

                    <h3 style="color:#1a56db;border-bottom:2px solid #e2e8f0;padding-bottom:8px;">Ubicación</h3>
                    <table style="width:100%;border-collapse:collapse;font-size:14px;margin-bottom:24px;">
                        <tr><td style="padding:9px 10px;border-bottom:1px solid #e2e8f0;color:#64748b;width:200px;"><b>Departamento</b></td><td style="padding:9px 10px;border-bottom:1px solid #e2e8f0;">{Departamento}</td></tr>
                        <tr><td style="padding:9px 10px;border-bottom:1px solid #e2e8f0;color:#64748b;"><b>Ciudad</b></td><td style="padding:9px 10px;border-bottom:1px solid #e2e8f0;">{Ciudad}</td></tr>
                        <tr><td style="padding:9px 10px;border-bottom:1px solid #e2e8f0;color:#64748b;"><b>Dirección</b></td><td style="padding:9px 10px;border-bottom:1px solid #e2e8f0;">{Direccion}</td></tr>
                    </table>

                    <h3 style="color:#1a56db;border-bottom:2px solid #e2e8f0;padding-bottom:8px;">Información Económica</h3>
                    <table style="width:100%;border-collapse:collapse;font-size:14px;margin-bottom:24px;">
                        <tr><td style="padding:9px 10px;border-bottom:1px solid #e2e8f0;color:#64748b;width:200px;"><b>Fuente de recursos</b></td><td style="padding:9px 10px;border-bottom:1px solid #e2e8f0;">{Fuentes_recursos}</td></tr>
                        <tr><td style="padding:9px 10px;border-bottom:1px solid #e2e8f0;color:#64748b;"><b>Fuente otros</b></td><td style="padding:9px 10px;border-bottom:1px solid #e2e8f0;">{Fuentes_recursos_otro or '—'}</td></tr>
                        <tr><td style="padding:9px 10px;border-bottom:1px solid #e2e8f0;color:#64748b;"><b>Año actualización</b></td><td style="padding:9px 10px;border-bottom:1px solid #e2e8f0;">{Año}</td></tr>
                        <tr><td style="padding:9px 10px;border-bottom:1px solid #e2e8f0;color:#64748b;"><b>Residencia fiscal otro país</b></td><td style="padding:9px 10px;border-bottom:1px solid #e2e8f0;">{ Residencia_fiscal_pais if Residencia_fiscal == 'si' else 'No'}</td></tr>
                        <tr><td style="padding:9px 10px;border-bottom:1px solid #e2e8f0;color:#64748b;"><b>Patrimonio</b></td><td style="padding:9px 10px;border-bottom:1px solid #e2e8f0;">{Patrimonio}</td></tr>
                        <tr><td style="padding:9px 10px;border-bottom:1px solid #e2e8f0;color:#64748b;"><b>Declarante de renta</b></td><td style="padding:9px 10px;border-bottom:1px solid #e2e8f0;">{Declarante_renta}</td></tr>
                        <tr><td style="padding:9px 10px;border-bottom:1px solid #e2e8f0;color:#64748b;"><b>PEP</b></td><td style="padding:9px 10px;border-bottom:1px solid #e2e8f0;">{PeP}</td></tr>
                    </table>

                    <h3 style="color:#1a56db;margin-top:0;">Observaciones</h3>
                    <div style="background:#f8fafc;padding:18px;border-left:4px solid #1a56db;border-radius:8px;color:#334155;line-height:1.7;">
                        {Observaciones or '<em style="color:#94a3b8;">Sin observaciones</em>'}
                    </div>
                </div>
                <div style="background:#f8fafc;padding:16px;text-align:center;font-size:12px;color:#94a3b8;">
                    Mensaje generado automáticamente desde famym.com.co
                </div>
            </div>
        </body>
        </html>
        """

        asunto_usuario = f"Solicitud recibida | Radicado {numero_radicado} | FAMYM"

        html_usuario = f"""
        <html>
        <body style="margin:0;padding:30px;background:#f1f5f9;font-family:Arial,sans-serif;">
            <div style="max-width:680px;margin:auto;background:#fff;border-radius:14px;overflow:hidden;box-shadow:0 0 20px rgba(0,0,0,.08);">
                <div style="background:linear-gradient(135deg,#0a1628,#1a56db);padding:32px;text-align:center;">
                    <img src="{logo_url}" alt="FAMYM Logo" width="110" style="display:block;margin:0 auto 14px;" />
                    <h1 style="color:#fff;margin:0;font-size:24px;">FAMYM</h1>
                    <p style="color:rgba(255,255,255,0.7);margin:6px 0 0;">Fondo de Empleados AMYM</p>
                </div>
                <div style="padding:40px;text-align:center;">
                    <h2 style="color:#0f172a;margin:0 0 12px;">Hola {P_nombre},</h2>
                    <p style="font-size:16px;color:#475569;line-height:1.75;max-width:460px;margin:0 auto 28px;">
                        Tu solicitud de <strong>actualización de datos</strong> fue recibida correctamente.
                        Un asesor de <strong style="color:#1a56db;">FAMYM</strong> la procesará en los
                        próximos <strong>3 días hábiles</strong>.
                    </p>
                    <div style="background:#f0f9ff;border:1px solid #bae6fd;border-radius:10px;padding:20px;display:inline-block;min-width:280px;margin-bottom:16px;">
                        <p style="margin:0 0 6px;color:#94a3b8;font-size:12px;text-transform:uppercase;letter-spacing:0.05em;">Número de radicado</p>
                        <p style="margin:0;font-weight:bold;color:#1a56db;font-size:20px;">{numero_radicado}</p>
                    </div>
                    <p style="color:#64748b;font-size:13px;max-width:400px;margin:0 auto 24px;">
                        Guarda este número como referencia para consultar el estado de tu solicitud.
                    </p>
                    <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;padding:18px;text-align:left;max-width:380px;margin:0 auto 28px;">
                        <p style="margin:0 0 10px;color:#64748b;font-size:12px;text-transform:uppercase;">Resumen</p>
                        <table style="width:100%;font-size:14px;color:#334155;">
                            <tr><td style="padding:5px 0;color:#94a3b8;">Nombre</td><td style="padding:5px 0;font-weight:bold;text-align:right;">{nombre_completo}</td></tr>
                            <tr><td style="padding:5px 0;color:#94a3b8;">Documento</td><td style="padding:5px 0;text-align:right;">{Tipo_documento} {Numero_documento}</td></tr>
                            <tr><td style="padding:5px 0;color:#94a3b8;">Correo</td><td style="padding:5px 0;color:#1a56db;text-align:right;">{Correo_registrado}</td></tr>
                        </table>
                    </div>
                    <p style="margin-top:8px;color:#00c6b8;font-weight:bold;font-size:17px;">¡Gracias por confiar en FAMYM!</p>
                </div>
                <div style="background:#f8fafc;padding:16px;text-align:center;font-size:12px;color:#94a3b8;">
                    Fondo de Empleados AMYM — Vigilados por la Supersolidaria<br/>
                    Este correo fue generado automáticamente, por favor no respondas.
                </div>
            </div>
        </body>
        </html>
        """

        #  ENVÍO DE CORREOS 
        try:
            correo_admin = EmailMultiAlternatives(
                asunto_admin,
                texto_plano_admin,
                settings.EMAIL_HOST_USER,
                ['practdesarrollo@montacargasamym.com']
            )
            correo_admin.attach_alternative(html_admin, "text/html")
            for archivo in archivos:
                correo_admin.attach(archivo.name, archivo.read(), archivo.content_type)
            correo_admin.send()

            correo_usuario = EmailMultiAlternatives(
                asunto_usuario,
                f"Hola {P_nombre}, tu solicitud fue radicada con el número {numero_radicado}. Te contactaremos pronto.",
                settings.EMAIL_HOST_USER,
                [Correo_registrado]   # ← solo un destinatario ahora
            )
            correo_usuario.attach_alternative(html_usuario, "text/html")
            correo_usuario.send()

        except Exception:
            traceback.print_exc()

        return JsonResponse({'ok': True, 'radicado': numero_radicado})

    except Exception:
        traceback.print_exc()
        return JsonResponse(
            {'ok': False, 'errores': {'__all__': 'Error interno del servidor. Por favor intenta de nuevo o contacta al administrador.'}},
            status=500
        )