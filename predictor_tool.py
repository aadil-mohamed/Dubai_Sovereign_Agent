import os, joblib, numpy as np
from functools import lru_cache

NON_DUBAI = [
    "abu dhabi","sharjah","ajman",
    "fujairah","ras al khaimah","rak","umm al quwain"
]

FALLBACK_MAP = {
    "ras al khaimah": "Jumeirah Village Circle",
    "rak":            "Jumeirah Village Circle",
    "abu dhabi":      "Dubai Marina",
    "sharjah":        "Deira",
    "ajman":          "Deira",
    "fujairah":       "Deira",
    "umm al quwain":  "Deira",
}

PRICE_FLOOR = 800_000

@lru_cache(maxsize=1)
def load_model():
    model   = joblib.load("/tmp/propiq_xgboost_model.pkl")
    columns = joblib.load("/tmp/propiq_model_columns.pkl")
    return model, columns

def predict_property_price(
    location_name: str,
    bedrooms: int,
    sqft: float,
    is_offplan: bool
) -> dict:
    print(f"[PREDICTOR v3.0] input: {location_name} {bedrooms}BR {sqft}sqft offplan={is_offplan}")

    area_raw = str(location_name or "Dubai Marina").strip()
    area_lower = area_raw.lower()

    out_of_market = any(k in area_lower for k in NON_DUBAI)

    if out_of_market:
        area_mapped = next(
            (v for k,v in FALLBACK_MAP.items() if k in area_lower),
            "Jumeirah Village Circle"
        )
        market_warning = (
            f"'{area_raw}' is outside Dubai. "
            f"Mapped to '{area_mapped}' for indicative valuation. "
            f"Treat with caution — non-Dubai pricing applies."
        )
    else:
        area_mapped = area_raw
        market_warning = None

    try:
        model, columns = load_model()

        row = {col: 0 for col in columns}

        area_col = f"area_{area_mapped}"
        if area_col in row:
            row[area_col] = 1
        else:
            fallback_col = "area_Jumeirah Village Circle"
            if fallback_col in row:
                row[fallback_col] = 1

        if "bedrooms" in row:
            row["bedrooms"] = int(bedrooms)
        if "size_sqft" in row:
            row["size_sqft"] = float(sqft)
        if "is_offplan" in row:
            row["is_offplan"] = int(is_offplan)

        X = np.array([[row[col] for col in columns]])
        price = float(model.predict(X)[0])

    except Exception as e:
        print(f"[PREDICTOR] model failed: {e} — using floor")
        price = PRICE_FLOOR

    if price < PRICE_FLOOR:
        price = PRICE_FLOOR

    print(f"[PREDICTOR v3.0] output: AED {price:,.0f} OOD={out_of_market}")

    return {
        "price":          price,
        "out_of_market":  out_of_market,
        "market_warning": market_warning,
    }