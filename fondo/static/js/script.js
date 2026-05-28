/*FAMYM SCRIPT */

document.addEventListener('DOMContentLoaded', () => {

  /*HEADER — scroll shadow */
  const header = document.getElementById('header');

  const onScroll = () => {
    header.classList.toggle('scrolled', window.scrollY > 20);
  };
  window.addEventListener('scroll', onScroll, { passive: true });


  /*  MOBILE NAV TOGGLE */
  const navToggle = document.getElementById('nav-toggle');
  const navMenu   = document.getElementById('nav-menu');

  navToggle?.addEventListener('click', () => {
    const isOpen = navMenu.classList.toggle('open');
    navToggle.setAttribute('aria-expanded', isOpen);
  });

  navMenu?.querySelectorAll('.nav__link').forEach(link => {
    link.addEventListener('click', () => {
      navMenu.classList.remove('open');
      navToggle.setAttribute('aria-expanded', false);
    });
  });


  /*HERO STATS — contador animado */
  const statNums = document.querySelectorAll('[data-target]');

  const animateCounter = (el) => {
    const target   = +el.dataset.target;
    const duration = 1800;
    const step     = 16;
    const steps    = duration / step;
    const increment = target / steps;
    let current = 0;

    const timer = setInterval(() => {
      current += increment;
      if (current >= target) {
        el.textContent = target;
        clearInterval(timer);
      } else {
        el.textContent = Math.floor(current);
      }
    }, step);
  };

  const statsObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        statNums.forEach(animateCounter);
        statsObserver.disconnect();
      }
    });
  }, { threshold: 0.5 });

  const heroStats = document.querySelector('.hero__stats');
  if (heroStats) statsObserver.observe(heroStats);


  /*  BANNER SLIDER */
  const slides    = document.querySelectorAll('.banner-slide');
  const dots      = document.querySelectorAll('.banner-indicator');
  const btnPrev   = document.getElementById('banner-prev');
  const btnNext   = document.getElementById('banner-next');
  let current     = 0;
  let autoplay;

  const goTo = (index) => {
    slides[current].classList.remove('active');
    dots[current].classList.remove('active');
    current = (index + slides.length) % slides.length;
    slides[current].classList.add('active');
    dots[current].classList.add('active');
  };

  const startAutoplay = () => {
    autoplay = setInterval(() => goTo(current + 1), 4500);
  };

  const resetAutoplay = () => {
    clearInterval(autoplay);
    startAutoplay();
  };

  btnPrev?.addEventListener('click', () => { goTo(current - 1); resetAutoplay(); });
  btnNext?.addEventListener('click', () => { goTo(current + 1); resetAutoplay(); });

  dots.forEach(dot => {
    dot.addEventListener('click', () => {
      goTo(+dot.dataset.slide);
      resetAutoplay();
    });
  });

  if (slides.length > 0) startAutoplay();


  /* TABS — Servicios */
  const tabBtns     = document.querySelectorAll('.tab-btn');
  const tabContents = document.querySelectorAll('.tab-content');

  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const target = btn.dataset.tab;

      tabBtns.forEach(b => b.classList.remove('active'));
      tabContents.forEach(c => c.classList.remove('active'));

      btn.classList.add('active');
      document.getElementById(`tab-${target}`)?.classList.add('active');
    });
  });




  /*CONVENIOS — ZONAS + MODAL*/

  // Navegación por zonas
  document.querySelectorAll('.zona-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const zona = btn.dataset.zona;
      document.querySelectorAll('.zona-btn').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.zona-panel').forEach(p => p.classList.remove('active'));
      btn.classList.add('active');
      document.getElementById('zona-' + zona)?.classList.add('active');
    });
  });

  // Modal de convenios
  const modal          = document.getElementById("convenio-modal");
  const modalLogo      = document.getElementById("modal-logo");
  const modalCategoria = document.getElementById("modal-categoria");
  const modalTitle     = document.getElementById("modal-title");
  const modalBeneficio = document.getElementById("modal-beneficio");
  const modalInfo      = document.getElementById("modal-info");
  const modalAsesor    = document.getElementById("modal-asesor");
  const modalCelular   = document.getElementById("modal-celular");
  const modalTipo      = document.getElementById("modal-tipo");
  const modalVigencia  = document.getElementById("modal-vigencia");
  const modalLink      = document.getElementById("modal-link");
  const closeBtn       = document.getElementById("modal-close");
  const overlay        = document.getElementById("modal-overlay");

  document.querySelectorAll(".convenio-card").forEach(card => {
    card.addEventListener("click", () => {
      const logoImg = card.querySelector(".convenio-card__logo img");

      // ── Logo ──
      if (logoImg && logoImg.src) {
        modalLogo.src           = logoImg.src;
        modalLogo.style.display = "block";
      } else {
        modalLogo.src           = "";
        modalLogo.style.display = "none";
      }

      modalLogo.alt              = card.dataset.nombre    || "";
      modalCategoria.textContent = card.dataset.categoria || "";
      modalTitle.textContent     = card.dataset.nombre    || "";
      modalBeneficio.textContent = card.dataset.beneficio || "";
      modalInfo.textContent      = card.dataset.info      || "";
      modalAsesor.textContent    = card.dataset.asesor    || "";
      modalCelular.textContent   = card.dataset.celular   || "";
      const numero = (card.dataset.celular || "").replace(/[\s\-()+]/g, "");
      const nombre = card.dataset.nombre || "";
     modalLink.href = `https://api.whatsapp.com/send?phone=57${numero}&text=Hola%2C%20me%20interesa%20información%20sobre%20el%20convenio%20con%20*${encodeURIComponent(nombre)}*`;
      modalTipo.textContent      = card.dataset.tipo      || card.dataset.categoria || "";
      modalVigencia.textContent  = card.dataset.vigencia  || "Consultar con FAMYM";
      modal.classList.add("active");
    });
  });

  const closeModal = () => modal.classList.remove("active");

  closeBtn.onclick = closeModal;
  overlay.onclick  = closeModal;

 modalLink.onclick = () => closeModal();



  document.addEventListener("keydown", e => {
    if (e.key === "Escape") closeModal();
  });



  /* SCROLL SUAVE — anclas internas */
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', (e) => {
      const id = anchor.getAttribute('href');
      if (id === '#') return;
      const target = document.querySelector(id);
      if (target) {
        e.preventDefault();
        const offset = 80;
        const top = target.getBoundingClientRect().top + window.scrollY - offset;
        window.scrollTo({ top, behavior: 'smooth' });
      }
    });
  });


  /* FADE-IN — elementos al hacer scroll */
  const fadeTargets = document.querySelectorAll(
    '.ahorro-card, .credito-card, .auxilio-card, .convenio-card, ' +
    '.ubicacion__info-card, .about__card, .contact__info-item'
  );

  const fadeObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('fade-in');
        fadeObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

  fadeTargets.forEach(el => fadeObserver.observe(el));

});

/*  FORMULARIO DE CONTACTO */
const formContacto = document.getElementById('contact-form');

formContacto?.addEventListener('submit', (e) => {
    e.preventDefault()  // ← evita que navegue a la respuesta JSON

    const btn = formContacto.querySelector('button[type="submit"]')
    btn.disabled = true
    btn.textContent = 'Enviando...'

    const formData = new FormData(formContacto)

    fetch(formContacto.action, {
        method: 'POST',
        body: formData,
    })
    .then(res => res.json())
    .then(data => {
        if (data.ok) {
            // Muestra mensaje de éxito
            formContacto.reset()
            btn.textContent = '¡Mensaje enviado!'
            btn.style.background = '#00c6b8'

            setTimeout(() => {
                btn.disabled = false
                btn.textContent = 'Enviar'
                btn.style.background = ''
            }, 4000)
        }
    })
    .catch(() => {
        btn.disabled = false
        btn.textContent = 'Enviar'
        alert('Ocurrió un error, intenta de nuevo.')
    })
})