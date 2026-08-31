"""Campaign URL templates for Instagram, Google Ads, and organic tracking.

Usage:
    python campaign_urls.py

GA4 reports: Acquisition > Traffic acquisition (session source / medium / campaign).
Custom events from funnel.js appear under Engagement > Events.
"""

from __future__ import annotations

SITE = "https://verafernandes.com"

# utm_source: platform (instagram, google, facebook, newsletter)
# utm_medium: channel (social, cpc, organic, email, bio)
# utm_campaign: campaign name (slug, no spaces)
# utm_content: ad variant (story_a, reel_memoria, post_sono)

CAMPAIGNS = [
    {
        "label": "Instagram — link na bio (hub)",
        "path": "/",
        "utm_source": "instagram",
        "utm_medium": "social",
        "utm_campaign": "bio_link",
        "utm_content": "bio",
    },
    {
        "label": "Instagram — bio neuropsicologia",
        "path": "/neuropsicologia/",
        "utm_source": "instagram",
        "utm_medium": "social",
        "utm_campaign": "bio_link",
        "utm_content": "neuro",
    },
    {
        "label": "Instagram — bio psicologia do sono",
        "path": "/psicologia-do-sono/",
        "utm_source": "instagram",
        "utm_medium": "social",
        "utm_campaign": "bio_link",
        "utm_content": "sono",
    },
    {
        "label": "Instagram — story/reel memória",
        "path": "/neuropsicologia/",
        "utm_source": "instagram",
        "utm_medium": "social",
        "utm_campaign": "story_memoria_2026",
        "utm_content": "story",
    },
    {
        "label": "Instagram — story sono",
        "path": "/psicologia-do-sono/",
        "utm_source": "instagram",
        "utm_medium": "social",
        "utm_campaign": "story_sono_2026",
        "utm_content": "story",
    },
    {
        "label": "Google Ads — avaliação Braga",
        "path": "/avaliacao-neuropsicologica/braga/",
        "utm_source": "google",
        "utm_medium": "cpc",
        "utm_campaign": "search_neuro_braga",
        "utm_content": "ad_braga",
    },
    {
        "label": "Google Ads — neuropsicologia geral",
        "path": "/neuropsicologia/",
        "utm_source": "google",
        "utm_medium": "cpc",
        "utm_campaign": "search_neuro_norte",
        "utm_content": "ad_generic",
    },
    {
        "label": "Google Search — orgânico (referência, sem UTM)",
        "path": "/",
        "note": "Não usar UTM. GA4 classifica via referrer google / gclid.",
    },
]


def build_url(path: str, source: str, medium: str, campaign: str, content: str = "") -> str:
    base = SITE + path
    params = [
        f"utm_source={source}",
        f"utm_medium={medium}",
        f"utm_campaign={campaign}",
    ]
    if content:
        params.append(f"utm_content={content}")
    return base + "?" + "&".join(params)


def main() -> None:
    print("Campaign URLs for verafernandes.com\n")
    for item in CAMPAIGNS:
        print(item["label"])
        if "note" in item:
            print(f"  {SITE}{item['path']}")
            print(f"  ({item['note']})")
        else:
            print(f"  {build_url(item['path'], item['utm_source'], item['utm_medium'], item['utm_campaign'], item.get('utm_content', ''))}")
        print()


if __name__ == "__main__":
    main()
