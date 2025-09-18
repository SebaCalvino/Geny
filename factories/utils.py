import re
import random
from urllib.parse import quote

try:
    from faker import Faker
except ImportError:
    Faker = None

GENERIC_DOMAINS = {'gmail.com', 'hotmail.com', 'yahoo.com'}

def _fake():
    return Faker() if Faker else None

def sanitize_email(raw_email, first_name=None, last_name=None, preferred_domains=None):
    preferred_domains = preferred_domains or ["example.com","studio.com","designco.io","techhub.dev","makerstudio.ai"]
    invalid = (
        not raw_email
        or re.match(r"^(hola|user|admin)@", raw_email or "", re.I)
        or (raw_email and raw_email.split("@")[-1].lower() in GENERIC_DOMAINS)
        or ("@" not in raw_email)
    )
    if invalid:
        fk = _fake()
        first = (first_name or (fk.first_name() if fk else "alex")).lower()
        last  = (last_name  or (fk.last_name()  if fk else "ramos")).lower()
        domain = random.choice(preferred_domains)
        return f"{first}.{last}@{domain}"
    return raw_email

def avatar_for(name, provider="dicebear"):
    seed = quote((name or "tektra_user").replace(" ", "_"))
    if provider == "ui-avatars":
        return f"https://ui-avatars.com/api/?name={seed}&size=256&background=random"
    # por defecto dicebear identicon
    return f"https://avatars.dicebear.com/api/identicon/{seed}.svg"

def picsum(width=1200, height=800, seed=None):
    s = f"?random={seed}" if seed else ""
    return f"https://picsum.photos/{width}/{height}{s}"
