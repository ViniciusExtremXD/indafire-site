#!/usr/bin/env python3
"""Gera o JSON de importação do contêiner GTM-WTKSN3VL (Inda Fire).

Tag do Google (GA4 G-RBGKBY9PJR) + eventos de contato (vindos do medicao.js) + vinculador de
conversões. Todas as tags só disparam no domínio oficial (indafire.com.br), para o site de
teste não sujar os dados.

Uso: python scripts/build_gtm_container.py docs/medicao/gtm-indafire.json
"""
import json
import sys

ACCOUNT = "6382803167"
CONTAINER = "267282788"
PUBLIC_ID = "GTM-WTKSN3VL"
GA4_ID = "G-RBGKBY9PJR"
HOST_REGEX = r"(^|\.)indafire\.com\.br$"
EVENTOS = [
    ("contato_whatsapp", "WhatsApp"),
    ("contato_telefone", "Telefone"),
    ("contato_email", "E-mail"),
]


def base(**kw):
    d = {"accountId": ACCOUNT, "containerId": CONTAINER}
    d.update(kw)
    return d


def tpl(key, value):
    return {"type": "TEMPLATE", "key": key, "value": value}


def host_filter():
    return [
        {
            "type": "MATCH_REGEX",
            "parameter": [tpl("arg0", "{{Page Hostname}}"), tpl("arg1", HOST_REGEX)],
        }
    ]


variables = [
    base(variableId="1", name="GA4 – ID de medição", type="c", parameter=[tpl("value", GA4_ID)]),
]
for i, nome in enumerate(["origem", "produto", "link_url"], start=2):
    variables.append(
        base(
            variableId=str(i),
            name="DLV – %s" % nome,
            type="v",
            parameter=[
                {"type": "INTEGER", "key": "dataLayerVersion", "value": "2"},
                {"type": "BOOLEAN", "key": "setDefaultValue", "value": "false"},
                tpl("name", nome),
            ],
        )
    )

triggers = [
    base(triggerId="10", name="Inicialização – site oficial", type="INIT", filter=host_filter()),
    base(triggerId="11", name="Todas as páginas – site oficial", type="PAGEVIEW", filter=host_filter()),
]
tags = [
    base(
        tagId="20",
        name="Tag do Google – GA4",
        type="googtag",
        parameter=[tpl("tagId", "{{GA4 – ID de medição}}")],
        firingTriggerId=["10"],
        tagFiringOption="ONCE_PER_EVENT",
    ),
    base(
        tagId="21",
        name="Vinculador de conversões (Google Ads)",
        type="gclidw",
        parameter=[
            {"type": "BOOLEAN", "key": "enableCrossDomain", "value": "false"},
            {"type": "BOOLEAN", "key": "enableUrlPassthrough", "value": "false"},
            {"type": "BOOLEAN", "key": "enableCookieOverrides", "value": "false"},
        ],
        firingTriggerId=["11"],
        tagFiringOption="ONCE_PER_EVENT",
    ),
]
for n, (evento, rotulo) in enumerate(EVENTOS):
    trig_id = str(12 + n)
    triggers.append(
        base(
            triggerId=trig_id,
            name="Contato – %s" % rotulo,
            type="CUSTOM_EVENT",
            customEventFilter=[
                {"type": "EQUALS", "parameter": [tpl("arg0", "{{_event}}"), tpl("arg1", evento)]}
            ],
            filter=host_filter(),
        )
    )
    params = []
    for p in ["origem", "produto", "link_url"]:
        params.append(
            {"type": "MAP", "map": [tpl("parameter", p), tpl("parameterValue", "{{DLV – %s}}" % p)]}
        )
    tags.append(
        base(
            tagId=str(30 + n),
            name="GA4 – %s" % evento,
            type="gaawe",
            parameter=[
                tpl("eventName", evento),
                tpl("measurementIdOverride", "{{GA4 – ID de medição}}"),
                {"type": "BOOLEAN", "key": "sendEcommerceData", "value": "false"},
                {"type": "LIST", "key": "eventSettingsTable", "list": params},
            ],
            firingTriggerId=[trig_id],
            tagFiringOption="ONCE_PER_EVENT",
        )
    )

builtins = [
    base(type=t, name=n)
    for t, n in [
        ("PAGE_URL", "Page URL"),
        ("PAGE_HOSTNAME", "Page Hostname"),
        ("PAGE_PATH", "Page Path"),
        ("REFERRER", "Referrer"),
        ("EVENT", "Event"),
        ("CLICK_URL", "Click URL"),
        ("CLICK_TEXT", "Click Text"),
    ]
]

export = {
    "exportFormatVersion": 2,
    "exportTime": "2026-10-15 18:00:00",
    "containerVersion": base(
        path="accounts/%s/containers/%s/versions/0" % (ACCOUNT, CONTAINER),
        containerVersionId="0",
        container=base(
            path="accounts/%s/containers/%s" % (ACCOUNT, CONTAINER),
            name="indafire.com.br",
            publicId=PUBLIC_ID,
            usageContext=["WEB"],
        ),
        tag=tags,
        trigger=triggers,
        variable=variables,
        builtInVariable=builtins,
    ),
}

out = sys.argv[1] if len(sys.argv) > 1 else "gtm-indafire.json"
with open(out, "w", encoding="utf-8") as fh:
    json.dump(export, fh, ensure_ascii=False, indent=2)
print(out, "tags=%d triggers=%d variables=%d" % (len(tags), len(triggers), len(variables)))
