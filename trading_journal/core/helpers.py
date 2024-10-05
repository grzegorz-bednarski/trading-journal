def get_joined_m2m_names(obj, attr: str, sub_attr: str = "name") -> str:
    return (
        ""
        if not hasattr(obj, attr)
        else ", ".join(obj.markets.values_list(sub_attr, flat=True))
    )
