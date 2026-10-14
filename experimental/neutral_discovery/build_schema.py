"""Build the closed reference contract; not a universal theory schema."""
import json
from pathlib import Path


def obj(properties):
    return {"type": "object", "additionalProperties": False,
            "required": list(properties), "properties": properties}


def constant(value):
    return {"const": value}


fraction = {"type": "string", "pattern": "^(0|[1-9][0-9]*)(/[1-9][0-9]*)?$", "maxLength": 32}
probabilities = obj({e: fraction for e in ("observe", "do_x_1", "do_y_1")})
from discovery import make_contract
example = make_contract()
properties = {k: constant(v) for k, v in example.items() if k != "classes"}
properties["classes"] = {"type": "array", "minItems": 2, "maxItems": 16,
    "items": obj({"id": {"type": "string", "pattern": "^C-[0-9a-f]{12}$"},
                  "p_one": probabilities, "prior": fraction})}
schema = {"$schema": "https://json-schema.org/draft/2020-12/schema",
          "$id": "urn:x6:neutral-discovery:contract:0.1.0", **obj(properties)}
Path(__file__).with_name("contract.schema.json").write_text(json.dumps(schema, indent=2)+"\n")
