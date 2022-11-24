

def get_shipping_fee(total, shipping_method) -> float:
    if shipping_method == "regular":
        if total < 200000:
            return total * 0.15
        else:
            return total * 0.2
    elif shipping_method == "next day":
        if total < 300000:
            return total * 0.2
        else:
            return total * 0.25

    return 0
