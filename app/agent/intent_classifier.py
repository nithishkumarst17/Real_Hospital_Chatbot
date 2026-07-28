DOCTOR_KEYWORDS = [
    "doctor","dr.","physician","specialist","cardiologist","orthopedic",
    "pediatric","pediatrician","surgeon","dermatologist","neurologist",
    "gynecologist","psychiatrist","oncologist","urologist","nephrologist",
    "which doctor","which specialist","find doctor","show doctor",
    "who is available","who can i see","doctor available","clinic",
    "மருத்துவர்","டாக்டர்","நிபுணர்","இதய","எலும்பு","குழந்தை",
    "மகளிர்","தோல்","மூளை",
]

BOOK_KEYWORDS = [
    "book","appointment","schedule","reserve","fix","slot","want to see",
    "need to see","i want","set up","நேரம்","அப்பாயின்ட்மென்ட்","பதிவு",
]

CANCEL_KEYWORDS = [
    "cancel","cancellation","remove appointment","delete appointment",
    "ரத்து","நீக்கு",
]

RESCHEDULE_KEYWORDS = [
    "reschedule","change appointment","move appointment","postpone",
    "மாற்று","நேரம் மாற்று",
]

GREETING_KEYWORDS = [
    "hello","hi ","hey ","good morning","good afternoon","good evening",
    "வணக்கம்","நமஸ்தே","ஹலோ",
]

ENTITY_SPECIALIZATIONS = {
    "cardiology":       ["cardio","heart","இதய","cardiac","cardiologist","chest pain"],
    "orthopedics":      ["ortho","bone","joint","எலும்பு","orthopedic","fracture","knee","spine"],
    "pediatrics":       ["pediatric","child","children","baby","குழந்தை","pedia","infant"],
    "general medicine": ["general medicine","fever","cold","family doctor","gp","flu","cough"],
    "dermatology":      ["skin","derma","தோல்","rash","allergy","hair loss"],
    "neurology":        ["neuro","brain","nerve","மூளை","headache","migraine","seizure"],
    "gynecology":       ["gynec","women","obstet","மகளிர்","pregnancy","maternity"],
}


def _match(text: str, keywords: list) -> bool:
    t = text.lower()
    return any(k in t for k in keywords)


def _extract_specialization(text: str):
    t = text.lower()
    for spec, clues in ENTITY_SPECIALIZATIONS.items():
        if any(c in t for c in clues):
            return spec
    return None


def classify_intent(english_text: str) -> dict:
    t = english_text.lower()
    entities = {
        "specialization": _extract_specialization(english_text),
        "doctor_name": None, "date": None, "time": None
    }

    if _match(t, CANCEL_KEYWORDS):
        return {"intent": "cancel_appointment", "entities": entities}
    if _match(t, RESCHEDULE_KEYWORDS):
        return {"intent": "reschedule_appointment", "entities": entities}
    if _match(t, BOOK_KEYWORDS) and not _match(t, ["insurance","policy"]):
        return {"intent": "book_appointment", "entities": entities}
    if _match(t, DOCTOR_KEYWORDS):
        return {"intent": "check_doctor_availability", "entities": entities}
    if _match(t, GREETING_KEYWORDS):
        return {"intent": "general_greeting", "entities": entities}

    return {"intent": "hospital_policy_query", "entities": entities}
