"""Shared HTML snippets for cookie consent (imported by render_pages.py)."""

CONSENT_HEAD = """    <script src="/assets/js/consent.js?v=3"></script>"""

HEAD_STYLES = """  <link rel="preload" href="/assets/fonts/Inter-latin.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/assets/fonts/Inter-latin-ext.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/assets/css/fonts.css">
  <link rel="stylesheet" href="/assets/css/bootstrap.min.css">
  <link rel="stylesheet" href="/assets/css/main.css">
  <link rel="stylesheet" href="/assets/css/funnel.css">
  <link rel="stylesheet" href="/assets/css/LineIcons.2.0.css" media="print" onload="this.media='all'">
  <link rel="stylesheet" href="/assets/css/consent.css" media="print" onload="this.media='all'">
  <link rel="stylesheet" href="/assets/css/animate.css" media="print" onload="this.media='all'">
  <noscript>
    <link rel="stylesheet" href="/assets/css/LineIcons.2.0.css">
    <link rel="stylesheet" href="/assets/css/consent.css">
    <link rel="stylesheet" href="/assets/css/animate.css">
  </noscript>"""

HEAD_LCP_PRELOAD = """  <link rel="preload" as="image" href="/assets/images/vera1-380w.webp" fetchpriority="high"
    imagesrcset="/assets/images/vera1-260w.webp 260w, /assets/images/vera1-380w.webp 380w, /assets/images/vera1-760w.webp 760w"
    imagesizes="(min-width: 992px) 380px, 32vw">
"""

CONSENT_BANNER = """
<div id="vf-consent" class="vf-consent" role="dialog" aria-labelledby="vf-consent-title" aria-live="polite" hidden>
    <div class="vf-consent__inner">
        <p id="vf-consent-title" class="vf-consent__text">Utilizamos cookies para perceber como o site é usado e melhorar a experiência de quem visita. Pode aceitar ou recusar. <a href="/privacy/">Política de privacidade</a></p>
        <div class="vf-consent__actions">
            <button type="button" id="vf-consent-accept" class="vf-consent__btn vf-consent__btn--accept" data-vf-consent-accept>Aceitar</button>
            <button type="button" id="vf-consent-reject" class="vf-consent__btn vf-consent__btn--reject" data-vf-consent-reject>Recusar</button>
        </div>
    </div>
</div>
<!-- /vf-consent -->
"""
