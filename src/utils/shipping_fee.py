

def get_shipping_fee(total, shipping_method):
    if shipping_method == "regular":
        if total < 200:
            return total * 0.15
        else:
            return total * 0.2
    elif shipping_method == "next Day":
        if total < 300:
            return total * 0.2
        else:
            return total * 0.25
