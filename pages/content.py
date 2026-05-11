"""Content for the project."""

from dataclasses import dataclass


SITE_NAME = "Above Board"
TAGLINE = "Built on reputation"


@dataclass(frozen=True)
class HeroContent:
    headline: str
    subhead: str
    primary_cta_label: str
    primary_cta_href: str
    secondary_cta_label: str
    secondary_cta_href: str


@dataclass(frozen=True)
class Feature:
    icon: str
    title: str
    description: str


@dataclass(frozen=True)
class PricingTier:
    name: str
    price: str
    audience: str
    highlights: tuple[str, ...]


@dataclass(frozen=True)
class NavItem:
    label: str
    url_name: str
    fragment: str = ""


@dataclass(frozen=True)
class FooterLink:
    label: str
    href: str


HERO = HeroContent(
    headline="Built on reputation",
    subhead=(
        "Above Board is reputation and hiring infrastructure for the 17 million workers "
        "who keep hospitality moving, giving talent, peers, and employers a cleaner way "
        "to understand who is trusted before the first shift."
    ),
    primary_cta_label="Join the waitlist",
    primary_cta_href="mailto:hello@joinaboveboard.com?subject=Join%20the%20waitlist",
    secondary_cta_label="For employers",
    secondary_cta_href="#pricing",
)

FEATURES = [
    Feature(
        icon="message-circle",
        title="Anonymous Peer Reviews",
        description="Reputation signals from people who have actually shared a floor, line, bar, or service station.",
    ),
    Feature(
        icon="badge-check",
        title="Verified Identity",
        description="Members build trust from a real professional identity while keeping sensitive details private.",
    ),
    Feature(
        icon="briefcase-business",
        title="Curated Jobs Board",
        description="Hospitality roles filtered for serious teams, sharper expectations, and stronger candidate context.",
    ),
    Feature(
        icon="messages-square",
        title="Community Forums",
        description="Invite-only discussions where operators and workers can compare notes without public noise.",
    ),
    Feature(
        icon="building-2",
        title="Employer Reputation Profiles",
        description="Employer pages show culture, consistency, and team feedback before anyone commits to an interview.",
    ),
    Feature(
        icon="key-round",
        title="Invite-Only Access",
        description="A controlled network model keeps the early community focused, credible, and above the usual churn.",
    ),
]

PRICING_TIERS = [
    PricingTier(
        name="For Workers",
        price="Free during beta",
        audience="Line cooks, bartenders, servers, hosts, managers, and hospitality pros.",
        highlights=(
            "Claim a verified profile",
            "Request peer reviews",
            "Browse curated roles",
        ),
    ),
    PricingTier(
        name="For Employers",
        price="Pilot access",
        audience="Independent restaurants, groups, hotels, and venue operators hiring for trust.",
        highlights=(
            "Create an employer reputation profile",
            "Reach verified hospitality talent",
            "Invite trusted team references",
        ),
    ),
]

NAV_ITEMS = [
    NavItem("Home", "pages:home"),
    NavItem("Features", "pages:home", "features"),
    NavItem("Pricing", "pages:home", "pricing"),
    NavItem("Contact", "pages:home", "contact"),
]

FOOTER_LINKS = {
    "Product": (
        FooterLink("Features", "#features"),
        FooterLink("Pricing", "#pricing"),
        FooterLink("Waitlist", "mailto:hello@joinaboveboard.com?subject=Join%20the%20waitlist"),
    ),
    "Company": (
        FooterLink("About", "#"),
        FooterLink("Employers", "#pricing"),
        FooterLink("Contact", "mailto:hello@joinaboveboard.com"),
    ),
    "Legal": (
        FooterLink("Privacy", "#"),
        FooterLink("Terms", "#"),
    ),
}

