from src.cs_bot.policies import FAQ, RETURN_POLICY, SHIPPING_POLICY, get_all_policies


def test_shipping_policy_contains_key_info():
    assert "Processing Time" in SHIPPING_POLICY
    assert "United States" in SHIPPING_POLICY
    assert "tracking" in SHIPPING_POLICY.lower()


def test_return_policy_contains_key_info():
    assert "30 days" in RETURN_POLICY
    assert "refund" in RETURN_POLICY.lower()
    assert "exchange" in RETURN_POLICY.lower()


def test_faq_contains_key_info():
    assert "Sanrio" in FAQ
    assert "size" in FAQ.lower()


def test_get_all_policies_combines_sections():
    combined = get_all_policies()
    assert "Shipping" in combined
    assert "Return" in combined
    assert "Frequently Asked Questions" in combined
