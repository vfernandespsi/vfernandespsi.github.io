"""Shared HTML snippets for cookie consent (imported by render_pages.py)."""

CONSENT_HEAD = """    <script src="/assets/js/consent.js?v=3"></script>"""

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
