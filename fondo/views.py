from django.shortcuts import render
from django.core.mail import EmailMultiAlternatives  # PERMITE ENVIAR CORREOS EN HTML O TEXTO PLANO
from django.conf import settings                     # ACCESO A LA CONFIGURACIÓN DE settings.py
from django.http import JsonResponse                 # RESPONDE CON JSON AL fetch() DEL JS
from .models import MensajeContacto,Banner                # IMPORTAMOS EL MODELO


# ══════════════════════════════════════════════════
#   VIEW PRINCIPAL — FORMULARIO DE CONTACTO
# ══════════════════════════════════════════════════
def FONDO(request):

    if request.method == 'POST':

        
        logo_url = "https://i.postimg.cc/wv42Tz9x/logo-F.jpg"
       

        # EXTRAER DATOS DEL FORMULARIO
        Nombre=request.POST.get('nombre',   '').strip()
        Empresa=request.POST.get('empresa',  '').strip()
        Correo=request.POST.get('correo',   '').strip()
        Telefono=request.POST.get('telefono', '').strip()
        Servicio=request.POST.get('servicio', '').strip()
        Mensaje=request.POST.get('mensaje',  '').strip()

        #GUARDAR EN BASE DE DATOS
        MensajeContacto.objects.create(
            Nombre   = Nombre,
            Empresa  = Empresa,
            Correo   = Correo,
            Telefono = Telefono,
            Servicio = Servicio,
            Mensaje  = Mensaje,
        )

        #CORREO AL ADMINISTRADOR DE FAMYM
        asunto_admin = "Nueva consulta recibida | FAMYM"

        texto_plano = f"""
Nueva consulta desde el sitio web de FAMYM

Nombre:   {Nombre}
Área:     {Empresa}
Correo:   {Correo}
Teléfono: {Telefono}
Servicio: {Servicio}

Mensaje:
{Mensaje}
        """

        html_admin = f"""
        <html>
        <body style="margin:0;padding:30px;background:#f1f5f9;font-family:Arial,sans-serif;">
            <div style="max-width:680px;margin:auto;background:#fff;border-radius:14px;overflow:hidden;box-shadow:0 0 20px rgba(0,0,0,.08);">

                <!-- HEADER CON LOGO -->
                <div style="background:linear-gradient(135deg,#0a1628,#1a56db);padding:32px;text-align:center;">
                    <img src="{logo_url}"
                         alt="FAMYM Logo"
                         width="110"
                         style="margin-bottom:14px;display:block;margin-left:auto;margin-right:auto;" />
                    <h1 style="color:#fff;margin:0;font-size:24px;letter-spacing:-0.5px;">FAMYM</h1>
                    <p style="color:rgba(255,255,255,0.7);margin:6px 0 0;">Fondo de Empleados AMYM</p>
                    <p style="color:#00c6b8;margin:8px 0 0;font-weight:bold;">Nueva consulta recibida</p>
                </div>

                <!-- CUERPO -->
                <div style="padding:36px;">
                    <h2 style="color:#0f172a;margin-top:0;">Datos del solicitante</h2>
                    <table style="width:100%;border-collapse:collapse;font-size:15px;">
                        <tr>
                            <td style="padding:11px 10px;border-bottom:1px solid #e2e8f0;color:#64748b;width:140px;"><b>Nombre</b></td>
                            <td style="padding:11px 10px;border-bottom:1px solid #e2e8f0;color:#0f172a;">{Nombre}</td>
                        </tr>
                        <tr>
                            <td style="padding:11px 10px;border-bottom:1px solid #e2e8f0;color:#64748b;"><b>Área</b></td>
                            <td style="padding:11px 10px;border-bottom:1px solid #e2e8f0;color:#0f172a;">{Empresa or '—'}</td>
                        </tr>
                        <tr>
                            <td style="padding:11px 10px;border-bottom:1px solid #e2e8f0;color:#64748b;"><b>Correo</b></td>
                            <td style="padding:11px 10px;border-bottom:1px solid #e2e8f0;color:#0f172a;">{Correo}</td>
                        </tr>
                        <tr>
                            <td style="padding:11px 10px;border-bottom:1px solid #e2e8f0;color:#64748b;"><b>Teléfono</b></td>
                            <td style="padding:11px 10px;border-bottom:1px solid #e2e8f0;color:#0f172a;">{Telefono or '—'}</td>
                        </tr>
                        <tr>
                            <td style="padding:11px 10px;border-bottom:1px solid #e2e8f0;color:#64748b;"><b>Servicio</b></td>
                            <td style="padding:11px 10px;border-bottom:1px solid #e2e8f0;color:#1a56db;font-weight:bold;">{Servicio}</td>
                        </tr>
                    </table>

                    <h3 style="color:#1a56db;margin-top:28px;">Mensaje</h3>
                    <div style="background:#f8fafc;padding:18px;border-left:4px solid #1a56db;border-radius:8px;color:#334155;line-height:1.7;">
                        {Mensaje}
                    </div>
                </div>

                <!-- FOOTER -->
                <div style="background:#f8fafc;padding:16px;text-align:center;font-size:12px;color:#94a3b8;">
                    Mensaje generado automáticamente desde famym.com.co
                </div>

            </div>
        </body>
        </html>
        """

        # CORREO DE CONFIRMACIÓN AL USUARIO
        asunto_usuario = "Recibimos tu mensaje | FAMYM"

        html_usuario = f"""
        <html>
        <body style="margin:0;padding:30px;background:#f1f5f9;font-family:Arial,sans-serif;">
            <div style="max-width:680px;margin:auto;background:#fff;border-radius:14px;overflow:hidden;box-shadow:0 0 20px rgba(0,0,0,.08);">

                <!-- HEADER CON LOGO -->
                <div style="background:linear-gradient(135deg,#0a1628,#1a56db);padding:32px;text-align:center;">
                    <img src="{logo_url}"
                         alt="FAMYM Logo"
                         width="110"
                         style="margin-bottom:14px;display:block;margin-left:auto;margin-right:auto;" />
                    <h1 style="color:#fff;margin:0;font-size:24px;">FAMYM</h1>
                    <p style="color:rgba(255,255,255,0.7);margin:6px 0 0;">Fondo de Empleados AMYM</p>
                </div>

                <!-- CUERPO -->
                <div style="padding:40px;text-align:center;">
                    <div style="font-size:52px;margin-bottom:16px;"></div>
                    <h2 style="color:#0f172a;margin:0 0 12px;">Hola {Nombre},</h2>
                    <p style="font-size:16px;color:#475569;line-height:1.75;max-width:420px;margin:0 auto 28px;">
                        Recibimos tu consulta correctamente.<br/>
                        Un asesor de <strong style="color:#1a56db;">FAMYM</strong> se comunicará
                        contigo en las próximas <strong>24 horas hábiles</strong>.
                    </p>

                    <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;padding:18px;display:inline-block;min-width:260px;">
                        <p style="margin:0 0 6px;color:#94a3b8;font-size:12px;text-transform:uppercase;letter-spacing:0.05em;">Servicio solicitado</p>
                        <p style="margin:0;font-weight:bold;color:#1a56db;font-size:16px;">{Servicio}</p>
                    </div>

                    <p style="margin-top:32px;color:#00c6b8;font-weight:bold;font-size:17px;">
                        ¡Gracias por confiar en FAMYM!
                    </p>
                </div>

                <!-- FOOTER -->
                <div style="background:#f8fafc;padding:16px;text-align:center;font-size:12px;color:#94a3b8;">
                    Fondo de Empleados AMYM — Vigilados por la Supersolidaria<br/>
                    Este correo fue generado automáticamente, por favor no respondas.
                </div>

            </div>
        </body>
        </html>
        """

        #ENVIAR CORREOS
        try:
            # Correo al administrador
            correo_admin = EmailMultiAlternatives(
                asunto_admin,
                texto_plano,
                settings.EMAIL_HOST_USER,
                ['practdesarrollo@montacargasamym.com']  
            )
            correo_admin.attach_alternative(html_admin, "text/html")
            correo_admin.send()

            # Correo de confirmación al usuario
            correo_usuario = EmailMultiAlternatives(
                asunto_usuario,
                f"Hola {Nombre}, recibimos tu consulta. Te contactaremos pronto.",
                settings.EMAIL_HOST_USER,
                [Correo]
            )
            correo_usuario.attach_alternative(html_usuario, "text/html")
            correo_usuario.send()

        except Exception as e:
            print(f"[FAMYM] Error al enviar correo: {e}")

        return JsonResponse({'ok': True})

    banners = Banner.objects.filter(activo=True).order_by('orden')
    return render(request, "fondo/index.html", {
        'banners': banners,
    })